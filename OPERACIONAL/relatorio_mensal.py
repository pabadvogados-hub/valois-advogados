"""
Relatorio mensal de situacao processual - Welington Valois Advogados Associados.

POP do escritorio: ate o 5o dia util de cada mes, todo cliente recebe um relatorio
do seu processo (resumo do caso, fase atual e proximo passo) e um AUDIO explicando
a mesma coisa em linguagem simples. Ver docs/POPs/POP_05_RELATORIO_MENSAL.md.

O que este script faz, em lote:
  1. puxa os processos ativos do ADVBOX (opcionalmente so de uma area/responsavel)
  2. le as movimentacoes do periodo de cada processo
  3. escreve o texto em linguagem do dia a dia (IA, com queda para modelo fixo)
  4. gera o audio (edge-tts)
  5. deixa tudo em SAIDA/relatorios/AAAA-MM/ e monta um indice .csv para revisao

NAO ENVIA NADA SOZINHO. O advogado responsavel revisa e so entao roda com --enviar.
Essa e a regra de ouro do escritorio: a IA prepara, o humano confere e assina.

Uso:
    python OPERACIONAL/relatorio_mensal.py                      # gera tudo do mes corrente
    python OPERACIONAL/relatorio_mensal.py --mes 09/2026
    python OPERACIONAL/relatorio_mensal.py --responsavel PRISCILA
    python OPERACIONAL/relatorio_mensal.py --sem-audio
    python OPERACIONAL/relatorio_mensal.py --exemplo            # demonstracao, sem ADVBOX
    python OPERACIONAL/relatorio_mensal.py --enviar             # dispara o que ja foi revisado
    python OPERACIONAL/relatorio_mensal.py --enviar --so CLIENTE
"""
import argparse
import csv
import os
import re
import sys
import unicodedata
from datetime import datetime, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(ROOT, 'config', '.env'))
except ImportError:
    pass

from INTEGRACOES import tts  # noqa: E402

SAIDA = os.path.join(ROOT, 'SAIDA', 'relatorios')

ESCRITORIO = os.getenv('ESCRITORIO_NOME', 'Welington Valois Advogados Associados')
TELEFONE_ESCRITORIO = os.getenv('ESCRITORIO_TELEFONE', '')

FASES_EM_PORTUGUES = {
    'INICIAL': 'a acao foi protocolada e aguarda a primeira analise do juiz',
    'CITACAO': 'a parte contraria esta sendo formalmente avisada da acao',
    'CONTESTACAO': 'a parte contraria apresentou a defesa dela',
    'REPLICA': 'estamos respondendo aos argumentos da defesa',
    'INSTRUCAO': 'estao sendo colhidas as provas (documentos, depoimentos, pericia)',
    'PERICIA': 'foi marcada a pericia medica',
    'AUDIENCIA': 'ha audiencia marcada',
    'SENTENCA': 'o processo esta concluso para o juiz decidir',
    'RECURSO': 'a decisao foi questionada e sera reanalisada pelo tribunal',
    'EXECUCAO': 'ja ha decisao favoravel e estamos cobrando o pagamento',
    'ADMINISTRATIVO': 'o pedido esta em analise no INSS, antes de qualquer acao judicial',
}

# O que costuma vir depois de cada fase. E um rascunho para o advogado confirmar:
# o relatorio so sai com o passo do caso concreto, conferido na revisao.
PROXIMO_PASSO = {
    'INICIAL': 'o juiz vai analisar o pedido e mandar avisar a outra parte',
    'CITACAO': 'a outra parte tera prazo para apresentar a defesa dela',
    'CONTESTACAO': 'vamos responder a defesa, ponto a ponto',
    'REPLICA': 'o juiz decide quais provas serao produzidas',
    'INSTRUCAO': 'depois das provas, o processo vai para o juiz decidir',
    'PERICIA': 'no dia marcado o senhor(a) passa pelo medico perito. '
               'Depois disso o laudo vem para o processo e nos vamos nos manifestar',
    'AUDIENCIA': 'no dia da audiencia o senhor(a) sera ouvido pelo juiz. '
                 'Nos avisamos com antecedencia o dia, a hora e o lugar',
    'SENTENCA': 'aguardamos a decisao do juiz. Assim que sair, explicamos o que ela significa',
    'RECURSO': 'o tribunal vai reanalisar o caso. Isso costuma demorar mais que a primeira fase',
    'EXECUCAO': 'seguimos cobrando o pagamento do valor reconhecido',
    'ADMINISTRATIVO': 'aguardamos a resposta do INSS. Se for negado, conversamos sobre entrar na Justica',
}


def _slug(texto):
    t = unicodedata.normalize('NFKD', str(texto or '')).encode('ascii', 'ignore').decode()
    t = re.sub(r'[^A-Za-z0-9]+', '_', t).strip('_').upper()
    return t[:60] or 'SEM_NOME'


def _primeiro_nome(nome):
    partes = [p for p in str(nome or '').split() if len(p) > 2]
    return partes[0].capitalize() if partes else 'Cliente'


def _competencia(mes_arg):
    if mes_arg:
        mes, ano = mes_arg.split('/')
        return int(ano), int(mes)
    hoje = datetime.now()
    return hoje.year, hoje.month


def _intervalo(ano, mes):
    inicio = datetime(ano, mes, 1)
    fim = datetime(ano + (mes == 12), (mes % 12) + 1, 1) - timedelta(days=1)
    return inicio.strftime('%Y-%m-%d'), fim.strftime('%Y-%m-%d')


def _fase_legivel(stage):
    s = (stage or '').upper()
    for chave, texto in FASES_EM_PORTUGUES.items():
        if chave in s:
            return texto
    return None


def _proximo_passo(stage):
    s = (stage or '').upper()
    for chave, texto in PROXIMO_PASSO.items():
        if chave in s:
            return texto
    return None


# ============================================================
# ORIGEM DOS DADOS
# ============================================================

def processos_do_advbox(responsavel=None, area=None):
    from INTEGRACOES import advbox_integration as advbox
    data = advbox._request('GET', '/lawsuits', params={'limit': 1000}) or {}
    todos = data.get('data', [])
    ativos = []
    for p in todos:
        fase = (p.get('stage') or '').upper()
        if 'ARQUIV' in fase or 'RENUNCI' in fase or 'ENCERR' in fase:
            continue
        if responsavel and responsavel.upper() not in (p.get('responsible') or '').upper():
            continue
        if area and area.upper() not in (p.get('type_lawsuit') or p.get('action') or '').upper():
            continue
        ativos.append(p)
    return ativos


def movimentacoes_do_mes(lawsuit_id, inicio, fim):
    from INTEGRACOES import advbox_integration as advbox
    try:
        movs = advbox.listar_ultimas_movimentacoes(
            lawsuit_id=lawsuit_id, date_start=inicio, date_end=fim) or []
    except Exception:
        return []
    return [m.get('description') or m.get('name') or '' for m in movs if m][:8]


def processos_de_exemplo():
    """Dados ficticios, so para demonstrar o formato sem tocar no ADVBOX."""
    return [
        {'id': 1, 'name': 'Maria Aparecida dos Santos', 'phone': '(28) 99999-0001',
         'process_number': '0001234-56.2026.8.08.0024', 'stage': 'PERICIA',
         'responsible': 'PRISCILA', 'action': 'Aposentadoria rural por idade',
         '_movs': ['Designada pericia medica para 14/10/2026',
                   'Juntada de contestacao do INSS']},
        {'id': 2, 'name': 'Joao Batista Ferreira', 'phone': '(28) 99999-0002',
         'process_number': '0004321-98.2026.8.08.0024', 'stage': 'SENTENCA',
         'responsible': 'PRISCILA', 'action': 'Beneficio por incapacidade',
         '_movs': ['Encerrada a instrucao', 'Autos conclusos para sentenca']},
        {'id': 3, 'name': 'Ana Lucia Pereira', 'phone': '(28) 99999-0003',
         'process_number': '', 'stage': 'ADMINISTRATIVO',
         'responsible': 'PRISCILA', 'action': 'Salario-maternidade (segurada especial)',
         '_movs': ['Requerimento protocolado no INSS em 02/09/2026']},
    ]


# ============================================================
# TEXTO DO RELATORIO
# ============================================================

def _modelo_fixo(processo, movs, mes_nome):
    nome = _primeiro_nome(processo.get('name'))
    acao = processo.get('action') or processo.get('type_lawsuit') or 'seu processo'
    fase = _fase_legivel(processo.get('stage')) or 'o processo segue em andamento'
    numero = processo.get('process_number') or ''

    linhas = [f'Ola, {nome}! Tudo bem?', '',
              f'Passando para contar como esta o seu caso de {acao.lower()} em {mes_nome}.', '']
    if numero:
        linhas += [f'Numero do processo: {numero}', '']
    linhas += ['COMO ESTA HOJE', f'Hoje {fase}.', '']
    if movs:
        linhas += ['O QUE ACONTECEU NESTE MES']
        linhas += [f'- {m}' for m in movs]
        linhas.append('')
    passo = _proximo_passo(processo.get('stage'))
    linhas += ['O QUE ACONTECE AGORA',
               f'Agora {passo}.' if passo else '[PREENCHER: proximo passo]', '',
               'Nao precisa fazer nada agora. Qualquer novidade, a gente avisa.',
               'Se tiver duvida, e so chamar aqui.', '',
               ESCRITORIO]
    if TELEFONE_ESCRITORIO:
        linhas.append(TELEFONE_ESCRITORIO)
    return '\n'.join(linhas)


def _por_ia(processo, movs, mes_nome):
    """Escreve o relatorio com a IA. Retorna None se nao houver chave/API."""
    if not os.getenv('ANTHROPIC_API_KEY'):
        return None
    try:
        from OPERACIONAL.agente_operacional import llm_client
    except Exception:
        return None

    system = (
        'Voce escreve relatorios mensais que um escritorio de advocacia do interior do '
        'Espirito Santo envia aos clientes pelo WhatsApp. Boa parte do publico e rural, '
        'idosa e com pouca escolaridade.\n'
        'REGRAS:\n'
        '- Linguagem do dia a dia. Nada de latim, "consectarios", "exordial", "autos".\n'
        '- Explique o que cada etapa significa na pratica.\n'
        '- Nunca prometa resultado, prazo exato de decisao nem valor a receber.\n'
        '- Nunca invente andamento: use SO o que estiver nos dados.\n'
        '- Se o proximo passo nao estiver claro nos dados, escreva literalmente '
        '"[PREENCHER: proximo passo]" para o advogado completar.\n'
        '- Maximo 200 palavras, tom cordial e tranquilizador, sem emoji.\n'
        f'- Assine como {ESCRITORIO}.'
    )
    dados = (
        f"Cliente: {processo.get('name')}\n"
        f"Acao: {processo.get('action') or processo.get('type_lawsuit') or '(nao informado)'}\n"
        f"Numero: {processo.get('process_number') or '(ainda sem numero - fase administrativa)'}\n"
        f"Fase atual no sistema: {processo.get('stage') or '(nao informada)'}\n"
        f"Movimentacoes do mes: {'; '.join(movs) if movs else '(nenhuma movimentacao no periodo)'}\n"
        f"Mes de referencia: {mes_nome}"
    )
    try:
        return llm_client.gerar_peca(system, '', dados, max_tokens=900).strip()
    except Exception as e:
        print(f'   AVISO: IA indisponivel ({str(e)[:60]}) - usando modelo fixo')
        return None


def montar_texto(processo, movs, mes_nome):
    """Retorna (texto, origem). origem: 'ia' ou 'modelo'."""
    texto = _por_ia(processo, movs, mes_nome)
    if texto:
        return texto, 'ia'
    return _modelo_fixo(processo, movs, mes_nome), 'modelo'


# ============================================================
# GERACAO
# ============================================================

MESES = ['janeiro', 'fevereiro', 'marco', 'abril', 'maio', 'junho', 'julho',
         'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']


def gerar(args):
    ano, mes = _competencia(args.mes)
    inicio, fim = _intervalo(ano, mes)
    mes_nome = f'{MESES[mes - 1]} de {ano}'
    pasta_mes = os.path.join(SAIDA, f'{ano}-{mes:02d}')
    os.makedirs(pasta_mes, exist_ok=True)

    print('=' * 70)
    print(f'  RELATORIO MENSAL AO CLIENTE - {mes_nome.upper()}')
    print(f'  {ESCRITORIO}')
    print('=' * 70)

    if args.exemplo:
        processos = processos_de_exemplo()
        print('\n  MODO EXEMPLO - dados ficticios, o ADVBOX nao foi consultado')
    else:
        print('\n  Consultando processos ativos no ADVBOX...')
        try:
            processos = processos_do_advbox(args.responsavel, args.area)
        except Exception as e:
            print(f'\n  ERRO ao falar com o ADVBOX: {str(e)[:120]}')
            print('  Confira ADVBOX_API_TOKEN em config/.env.')
            print('  Para ver o formato do relatorio sem credencial: --exemplo')
            return 1

    if not processos:
        print('\n  Nenhum processo ativo encontrado com esse filtro.')
        return 0

    print(f'  {len(processos)} processo(s) ativo(s).\n')

    indice = []
    for i, p in enumerate(processos, 1):
        nome = p.get('name') or p.get('customer') or 'SEM NOME'
        print(f'  [{i}/{len(processos)}] {nome}')

        movs = p.get('_movs') if args.exemplo else movimentacoes_do_mes(p.get('id'), inicio, fim)
        texto, origem = montar_texto(p, movs, mes_nome)

        pasta_cliente = os.path.join(pasta_mes, _slug(nome))
        os.makedirs(pasta_cliente, exist_ok=True)
        caminho_txt = os.path.join(pasta_cliente, 'relatorio.txt')
        with open(caminho_txt, 'w', encoding='utf-8') as f:
            f.write(texto)

        caminho_mp3 = ''
        if not args.sem_audio:
            destino = os.path.join(pasta_cliente, 'audio.mp3')
            if tts.gerar_audio(tts.texto_para_fala(texto), destino):
                caminho_mp3 = destino
                print('        texto + audio')
            else:
                print('        texto (sem audio)')
        else:
            print('        texto')

        pendente = 'SIM' if '[PREENCHER' in texto else 'nao'
        if pendente == 'SIM':
            print('        ATENCAO: ficou [PREENCHER] no texto - completar antes de enviar')

        indice.append({
            'cliente': nome,
            'telefone': p.get('phone') or p.get('cellphone') or '',
            'processo': p.get('process_number') or '',
            'fase': p.get('stage') or '',
            'responsavel': p.get('responsible') or '',
            'pasta': pasta_cliente,
            'texto': caminho_txt,
            'audio': caminho_mp3,
            'precisa_preencher': pendente,
            'origem_texto': origem,
            'revisado_por': '',
            'enviar': '',
        })

    caminho_indice = os.path.join(pasta_mes, 'INDICE_PARA_REVISAO.csv')
    with open(caminho_indice, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(indice[0].keys()), delimiter=';')
        w.writeheader()
        w.writerows(indice)

    pend = sum(1 for r in indice if r['precisa_preencher'] == 'SIM')
    print('\n' + '=' * 70)
    print(f'  Gerados: {len(indice)} relatorio(s) em {pasta_mes}')
    if pend:
        print(f'  {pend} com [PREENCHER] - completar o proximo passo antes de enviar')
    print(f'  Indice para revisao: {caminho_indice}')
    print()
    print('  PROXIMO PASSO (humano): o advogado responsavel le cada relatorio,')
    print('  confere se o proximo passo bate com o caso concreto (o texto sem IA usa')
    print('  o passo tipico da fase), escreve o nome dele na coluna "revisado_por"')
    print('  e marca "enviar" com SIM. Depois disso:')
    print('      python OPERACIONAL/relatorio_mensal.py --enviar')
    print('=' * 70)
    return 0


# ============================================================
# ENVIO
# ============================================================

def enviar(args):
    from INTEGRACOES import evolution_integration as evo

    ano, mes = _competencia(args.mes)
    pasta_mes = os.path.join(SAIDA, f'{ano}-{mes:02d}')
    caminho_indice = os.path.join(pasta_mes, 'INDICE_PARA_REVISAO.csv')
    if not os.path.exists(caminho_indice):
        print(f'ERRO: nao achei {caminho_indice}. Gere os relatorios primeiro.')
        return 1

    with open(caminho_indice, encoding='utf-8-sig') as f:
        linhas = list(csv.DictReader(f, delimiter=';'))

    fila = [r for r in linhas if (r.get('enviar') or '').strip().upper() in ('SIM', 'S', 'X')]
    if args.so:
        fila = [r for r in fila if args.so.upper() in r['cliente'].upper()]

    if not fila:
        print('Nenhuma linha marcada com SIM na coluna "enviar" do indice.')
        print(f'Marque quem ja foi revisado em: {caminho_indice}')
        return 0

    sem_revisor = [r for r in fila if not (r.get('revisado_por') or '').strip()]
    if sem_revisor:
        print(f'ERRO: {len(sem_revisor)} relatorio(s) marcados para envio sem "revisado_por".')
        print('O POP do escritorio exige revisao do advogado antes do envio. Preencha a coluna.')
        return 1

    pendentes = [r for r in fila if r.get('precisa_preencher') == 'SIM'
                 and '[PREENCHER' in open(r['texto'], encoding='utf-8').read()]
    if pendentes:
        print(f'ERRO: {len(pendentes)} relatorio(s) ainda tem [PREENCHER] no texto:')
        for r in pendentes[:5]:
            print(f'  - {r["cliente"]}')
        return 1

    if not evo.configurado():
        print('ERRO: Evolution API nao configurada (EVOLUTION_URL / _API_KEY / _INSTANCIA no .env).')
        return 1
    if not evo.conectado():
        print('ERRO: a instancia do WhatsApp nao esta conectada. Leia o QR Code na Evolution.')
        return 1

    print(f'\n  {len(fila)} relatorio(s) revisados e prontos para envio.')
    resp = input('  Confirma o disparo no WhatsApp? (digite SIM): ').strip().upper()
    if resp != 'SIM':
        print('  Cancelado.')
        return 0

    ok = falhou = 0
    for r in fila:
        tel = r.get('telefone')
        if not evo.normalizar_numero(tel):
            print(f'  [x] {r["cliente"]}: telefone ausente ou invalido')
            falhou += 1
            continue
        texto = open(r['texto'], encoding='utf-8').read()
        enviou = evo.enviar_texto(tel, texto)
        if enviou and r.get('audio') and os.path.exists(r['audio']):
            evo.enviar_audio(tel, r['audio'])
        if enviou:
            print(f'  [ok] {r["cliente"]}')
            ok += 1
        else:
            print(f'  [x] {r["cliente"]}: falha no envio')
            falhou += 1

    print(f'\n  Enviados: {ok} | Falhas: {falhou}')
    return 0


def main():
    ap = argparse.ArgumentParser(description='Relatorio mensal de situacao processual ao cliente')
    ap.add_argument('--mes', help='MM/AAAA (padrao: mes corrente)')
    ap.add_argument('--responsavel', help='filtra pelo advogado responsavel no ADVBOX')
    ap.add_argument('--area', help='filtra pelo tipo de acao')
    ap.add_argument('--sem-audio', action='store_true', help='gera so o texto')
    ap.add_argument('--exemplo', action='store_true', help='dados ficticios, sem consultar o ADVBOX')
    ap.add_argument('--enviar', action='store_true', help='envia o que ja foi revisado no indice')
    ap.add_argument('--so', help='com --enviar: manda so para esse cliente')
    args = ap.parse_args()

    if args.enviar:
        return enviar(args)
    return gerar(args)


if __name__ == '__main__':
    sys.exit(main())
