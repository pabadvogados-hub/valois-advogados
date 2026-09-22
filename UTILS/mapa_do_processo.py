# -*- coding: utf-8 -*-
"""
Mapa do Processo - Welington Valois Advogados Associados.

Gera o mapa das fases do processo em HTML pronto para imprimir (A4 retrato),
para ser entregue impresso ao cliente que fecha contrato (POP 02).

Uso:
    python UTILS/mapa_do_processo.py previdenciario
    python UTILS/mapa_do_processo.py criminal
    python UTILS/mapa_do_processo.py familia
    python UTILS/mapa_do_processo.py bancario
    python UTILS/mapa_do_processo.py civel
    python UTILS/mapa_do_processo.py --todas

Saida: SAIDA/mapa_processo_<area>.html
"""
import argparse
import html
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAIDA = os.path.join(RAIZ, 'SAIDA')

ESCRITORIO = 'Welington Valois Advogados Associados'
ENDERECO = 'Rua Galaor Rios, 289, Centro - Iuna/ES  |  Ibatiba/ES  |  Irupi/ES'
CONTATO = 'WhatsApp e telefone: (28) 99981-5672  |  welingtonvaloisadv@gmail.com'

AVISO_INTIMACAO = (
    'Durante todo o processo o juiz vai dando ordens (os despachos) e o cartorio vai avisando '
    'o advogado de cada passo (as intimacoes). Isso acontece do comeco ao fim, entre uma fase '
    'e outra. Voce nao precisa acompanhar nada disso: quem acompanha e o seu advogado, e todo '
    'mes voce recebe o relatorio dizendo em que fase o seu processo esta.'
)

AREAS = {
    'previdenciario': {
        'titulo': 'Aposentadoria e beneficios do INSS',
        'subtitulo': 'O caminho do seu pedido, do comeco ao fim',
        'responsavel': 'Dra. Priscila Araujo de Matos - OAB/ES 39.600',
        'fases': [
            ('Conversa e documentos',
             'Voce conta a sua historia e nos separamos os documentos: identidade, CPF, '
             'comprovante de residencia, documentos do trabalho e, se for o caso, os laudos '
             'e receitas do medico.'),
            ('Pedido no INSS',
             'Primeiro o pedido e feito no proprio INSS. Essa e a fase administrativa. '
             'Sem passar por aqui, na maioria dos casos nao da para entrar na Justica.'),
            ('Pericia medica do INSS',
             'Se o seu beneficio depende de doenca ou incapacidade, o INSS marca uma pericia. '
             'Um medico do INSS examina voce e diz se concorda que voce esta incapacitado. '
             'E obrigatorio comparecer no dia marcado.'),
            ('Avaliacao social do INSS',
             'Em alguns beneficios, alem do medico, uma assistente social do INSS avalia como '
             'voce vive e quanto a sua familia ganha.'),
            ('Resposta do INSS',
             'O INSS responde: aceita o pedido e comeca a pagar, ou nega. Se negar, ou se demorar '
             'demais, nos levamos o caso para a Justica.'),
            ('Entrada da acao na Justica',
             'Escrevemos a peticao inicial, que e o documento em que contamos o seu caso ao juiz '
             'e pedimos o beneficio. A acao entra aqui mesmo, no forum da comarca da regiao - '
             'voce nao precisa viajar para a Justica Federal.'),
            ('O INSS se defende',
             'O INSS apresenta a contestacao, que e a defesa dele. Ele diz ao juiz por que acha '
             'que voce nao tem direito.'),
            ('Nossa resposta',
             'A replica e a nossa resposta a defesa do INSS. Aqui nos derrubamos, um por um, os '
             'argumentos que o INSS usou contra voce.'),
            ('Pericia medica do juiz',
             'Se o caso envolve doenca, o juiz escolhe um medico de confianca dele para examinar '
             'voce de novo. Esse medico nao trabalha para o INSS nem para nos. O dia e o lugar sao '
             'avisados com antecedencia.'),
            ('Estudo social',
             'Uma assistente social escolhida pelo juiz vai ate a sua casa ou propriedade para ver '
             'como a familia vive e trabalha. Muito comum nos casos de trabalhador rural e de '
             'beneficio para quem tem pouca renda.'),
            ('Audiencia',
             'E o dia em que voce e as suas testemunhas falam com o juiz. Na audiencia de instrucao '
             'e julgamento as testemunhas contam o que sabem do seu trabalho e da sua vida. '
             'Voce sera avisado com antecedencia e nos preparamos tudo com voce antes.'),
            ('Ultimas palavras das partes',
             'As alegacoes finais sao o resumo que cada lado escreve no fim, juntando tudo o que '
             'ficou provado. E a nossa ultima palavra antes da decisao.'),
            ('Sentenca',
             'E a decisao do juiz. Ele diz se voce tem direito ao beneficio e a partir de quando.'),
            ('Recurso',
             'Se qualquer um dos lados nao concordar com a decisao, o caso sobe para a Justica '
             'Federal, que revisa a sentenca. Essa etapa nem sempre acontece.'),
            ('Beneficio pago',
             'Ganhando em definitivo, o INSS e obrigado a comecar a pagar o beneficio e a pagar '
             'tambem o que ficou atrasado desde a data reconhecida pelo juiz.'),
        ],
    },
    'criminal': {
        'titulo': 'Processo criminal',
        'subtitulo': 'O caminho da sua defesa, do comeco ao fim',
        'responsavel': 'Dr. Welington Dias Valois - OAB/ES 34.912  |  '
                       'Dr. Guilherme Mota Lopes Costa - OAB/ES 44.599',
        'fases': [
            ('Conversa e documentos',
             'Voce conta o que aconteceu e nos reunimos tudo o que ajuda a sua defesa: documentos, '
             'mensagens, nomes de pessoas que podem servir de testemunha.'),
            ('Investigacao',
             'A policia investiga e reune o que encontrou no inquerito policial. Nesta fase ainda '
             'nao ha acusacao formal. Se voce for chamado para depor, nos vamos junto.'),
            ('Acusacao',
             'O Ministerio Publico analisa a investigacao e decide: arquiva o caso ou apresenta a '
             'denuncia, que e a acusacao formal contra voce.'),
            ('O juiz decide se aceita a acusacao',
             'O juiz le a denuncia e decide se o processo comeca ou nao.'),
            ('Nossa defesa escrita',
             'Apresentamos a resposta a acusacao: e o documento em que mostramos ao juiz o outro '
             'lado da historia e indicamos as nossas testemunhas.'),
            ('Audiencia',
             'E o dia principal. Na audiencia de instrucao e julgamento as testemunhas sao ouvidas '
             'e, no fim, o juiz ouve voce. Nos preparamos tudo com voce antes.'),
            ('Ultimas palavras das partes',
             'Nas alegacoes finais cada lado escreve o resumo do que ficou provado. E a nossa ultima '
             'palavra antes da decisao.'),
            ('Sentenca',
             'E a decisao do juiz: absolvicao ou condenacao. Estando condenado, a sentenca diz qual '
             'e a pena e como ela sera cumprida.'),
            ('Recurso',
             'Se a decisao nao for favoravel, recorremos ao tribunal, que revisa a sentenca. '
             'A acusacao tambem pode recorrer.'),
            ('Fim do processo',
             'Quando nao cabe mais recurso, o processo termina. Havendo condenacao, comeca a fase '
             'de cumprimento da pena, que continua sendo acompanhada por nos.'),
        ],
    },
    'familia': {
        'titulo': 'Familia e heranca',
        'subtitulo': 'O caminho do seu processo, do comeco ao fim',
        'responsavel': 'Dra. Derlira Garcia Pimentel Soares - OAB/ES 27.296',
        'fases': [
            ('Conversa e documentos',
             'Voce conta a sua situacao e nos separamos os documentos: certidoes, documentos dos '
             'bens, comprovantes de despesa e de renda.'),
            ('Tentativa de acordo',
             'Sempre que for possivel e seguro para voce, tentamos resolver por acordo. Acordo e '
             'mais rapido, mais barato e menos desgastante.'),
            ('Entrada da acao',
             'Nao havendo acordo, escrevemos a peticao inicial, que e o documento em que contamos '
             'o seu caso ao juiz e dizemos o que voce esta pedindo.'),
            ('Audiencia de conciliacao',
             'O juiz chama os dois lados para uma nova tentativa de acordo, com a ajuda de uma '
             'pessoa preparada para isso. Se houver acordo aqui, o processo termina cedo.'),
            ('O outro lado se defende',
             'A outra parte apresenta a contestacao, que e a defesa dela, dizendo ao juiz por que '
             'discorda do seu pedido.'),
            ('Nossa resposta',
             'A replica e a nossa resposta a defesa da outra parte. Rebatemos ponto a ponto o que '
             'foi alegado contra voce.'),
            ('Producao de provas',
             'Juntamos os documentos e, quando o caso pede, o juiz determina estudo social, '
             'avaliacao psicologica ou avaliacao dos bens.'),
            ('Audiencia',
             'Na audiencia de instrucao e julgamento voce e as suas testemunhas falam com o juiz. '
             'Voce e avisado com antecedencia e nos preparamos tudo com voce antes.'),
            ('Ultimas palavras das partes',
             'Nas alegacoes finais cada lado escreve o resumo do que ficou provado. E a nossa ultima '
             'palavra antes da decisao.'),
            ('Sentenca',
             'E a decisao do juiz sobre o que foi pedido: divorcio, guarda, pensao, partilha, '
             'heranca.'),
            ('Recurso',
             'Se algum dos lados nao concordar, o caso sobe para o tribunal, que revisa a decisao. '
             'Essa etapa nem sempre acontece.'),
            ('Cumprimento da decisao',
             'Com a decisao definitiva, cuidamos de fazer valer o que foi decidido: averbacao no '
             'cartorio, transferencia dos bens, pagamento da pensao.'),
        ],
    },
    'bancario': {
        'titulo': 'Problema com banco ou financiamento',
        'subtitulo': 'O caminho do seu processo, do comeco ao fim',
        'responsavel': 'Dr. Heliezer de Medeiros Pontes - OAB/ES 38.904',
        'fases': [
            ('Conversa e documentos',
             'Voce conta o que esta acontecendo e nos separamos os documentos: contrato, carne, '
             'extratos, comprovantes de pagamento e as cobrancas que voce recebeu.'),
            ('Analise do contrato',
             'Estudamos o seu contrato e as contas para descobrir o que esta sendo cobrado a mais '
             'e o que da para discutir na Justica. Aqui nos dizemos com sinceridade se vale a pena.'),
            ('Tentativa de solucao direta',
             'Quando for o caso, procuramos o banco antes de processar, para tentar resolver sem '
             'acao judicial.'),
            ('Entrada da acao',
             'Nao havendo solucao, escrevemos a peticao inicial, que e o documento em que contamos '
             'o seu caso ao juiz e dizemos o que voce esta pedindo.'),
            ('O banco se defende',
             'O banco apresenta a contestacao, que e a defesa dele, com os motivos pelos quais '
             'acha que a cobranca esta correta.'),
            ('Nossa resposta',
             'A replica e a nossa resposta a defesa do banco. Rebatemos ponto a ponto o que ele '
             'alegou contra voce.'),
            ('Pericia nas contas',
             'Quando o caso exige, o juiz nomeia um perito - um profissional que entende de '
             'calculo - para refazer as contas do contrato e dizer quanto foi cobrado a mais.'),
            ('Audiencia',
             'Nem todo processo de banco tem audiencia. Quando houver, voce e avisado com '
             'antecedencia e nos preparamos tudo com voce antes.'),
            ('Sentenca',
             'E a decisao do juiz: ele diz se a cobranca do banco estava errada e o que precisa '
             'ser corrigido ou devolvido.'),
            ('Recurso',
             'Bancos costumam recorrer. Nesse caso o processo sobe para o tribunal, que revisa a '
             'decisao.'),
            ('Cumprimento da decisao',
             'Com a decisao definitiva, cuidamos de fazer valer o resultado: correcao da divida, '
             'devolucao do que foi pago a mais, retirada do seu nome dos cadastros.'),
        ],
    },
    'civel': {
        'titulo': 'Direito do consumidor e causas civeis',
        'subtitulo': 'O caminho do seu processo, do comeco ao fim',
        'responsavel': 'Dra. Gisele Teofilo de Avila - OAB/ES 23.868',
        'fases': [
            ('Conversa e documentos',
             'Voce conta o que aconteceu e nos separamos as provas: nota fiscal, contrato, fotos, '
             'mensagens, protocolos de atendimento e comprovantes de pagamento.'),
            ('Reclamacao antes da acao',
             'Quando for o caso, registramos reclamacao na empresa, no orgao de defesa do consumidor '
             'ou enviamos uma notificacao, para tentar resolver sem processo.'),
            ('Entrada da acao',
             'Nao resolvendo, escrevemos a peticao inicial, que e o documento em que contamos o seu '
             'caso ao juiz e dizemos o que voce esta pedindo.'),
            ('Audiencia de conciliacao',
             'O juiz chama os dois lados para tentar um acordo. Se houver acordo aqui, o processo '
             'termina cedo e voce recebe mais rapido.'),
            ('A outra parte se defende',
             'A empresa ou a pessoa processada apresenta a contestacao, que e a defesa dela.'),
            ('Nossa resposta',
             'A replica e a nossa resposta a defesa do outro lado. Rebatemos ponto a ponto o que '
             'foi alegado contra voce.'),
            ('Producao de provas',
             'Juntamos os documentos e, quando o caso pede, o juiz determina pericia ou vistoria.'),
            ('Audiencia',
             'Na audiencia de instrucao e julgamento voce e as suas testemunhas falam com o juiz. '
             'Voce e avisado com antecedencia e nos preparamos tudo com voce antes.'),
            ('Sentenca',
             'E a decisao do juiz sobre o que foi pedido: devolucao do dinheiro, conserto, '
             'cancelamento da cobranca, indenizacao.'),
            ('Recurso',
             'Se algum dos lados nao concordar, o caso sobe para o tribunal, que revisa a decisao. '
             'Essa etapa nem sempre acontece.'),
            ('Recebimento',
             'Com a decisao definitiva, cobramos o cumprimento: o pagamento a voce ou a obrigacao '
             'que foi determinada.'),
        ],
    },
}

CSS = """
@page { size: A4 portrait; margin: 14mm 13mm 12mm 13mm; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body {
  font-family: Arial, "Helvetica Neue", Helvetica, sans-serif;
  color: #1b1b1b;
  background: #ffffff;
  font-size: 12pt;
  line-height: 1.45;
}
.folha { max-width: 184mm; margin: 0 auto; padding: 6mm 0; }
.cabecalho { border-bottom: 3px solid #1b3a5c; padding-bottom: 5mm; margin-bottom: 6mm; }
.escritorio { font-size: 10pt; letter-spacing: 1.2px; text-transform: uppercase; color: #1b3a5c; font-weight: bold; }
h1 { font-size: 21pt; margin: 3mm 0 1mm 0; color: #1b3a5c; line-height: 1.15; }
.subtitulo { font-size: 12.5pt; color: #444444; margin: 0; }
.abertura {
  border: 1.5px solid #c9c9c9; border-left: 6px solid #1b3a5c;
  padding: 4mm 5mm; margin-bottom: 6mm; font-size: 11.5pt; background: #f7f8fa;
}
.abertura strong { color: #1b3a5c; }
.hoje { border: 2.5px solid #1b3a5c; padding: 4mm 5mm; margin-bottom: 7mm; }
.hoje-titulo { font-size: 13.5pt; font-weight: bold; color: #1b3a5c; text-transform: uppercase; letter-spacing: .5px; }
.hoje-texto { font-size: 10.5pt; color: #555555; margin: 1mm 0 4mm 0; }
.linha-preencher { display: flex; gap: 6mm; margin-top: 3mm; }
.campo { flex: 1; }
.campo .rotulo { font-size: 9.5pt; color: #555555; text-transform: uppercase; letter-spacing: .5px; }
.campo .traco { border-bottom: 1.5px solid #1b1b1b; height: 8mm; }
ol.fases { list-style: none; margin: 0; padding: 0; }
ol.fases li {
  position: relative; padding: 0 0 6mm 20mm; break-inside: avoid; page-break-inside: avoid;
}
ol.fases li::before {
  content: attr(data-n);
  position: absolute; left: 0; top: 0;
  width: 13mm; height: 13mm; line-height: 13mm; text-align: center;
  border: 2.5px solid #1b3a5c; border-radius: 50%;
  font-size: 14pt; font-weight: bold; color: #1b3a5c; background: #ffffff;
}
ol.fases li::after {
  content: ""; position: absolute; left: 6.5mm; top: 13mm; bottom: 0;
  border-left: 2.5px dotted #9fb2c4;
}
ol.fases li:last-child::after { display: none; }
.fase-nome { font-size: 13.5pt; font-weight: bold; color: #1b3a5c; margin: 1mm 0 1mm 0; }
.fase-texto { font-size: 11.5pt; margin: 0; }
.marcador {
  position: absolute; right: 0; top: 2mm;
  width: 7mm; height: 7mm; border: 2px solid #1b3a5c;
}
.nota {
  border: 1.5px dashed #1b3a5c; padding: 4mm 5mm; margin: 5mm 0 6mm 0;
  font-size: 11pt; background: #f7f8fa; break-inside: avoid; page-break-inside: avoid;
}
.nota-titulo { font-weight: bold; color: #1b3a5c; display: block; margin-bottom: 1.5mm; }
.rodape {
  border-top: 3px solid #1b3a5c; margin-top: 4mm; padding-top: 4mm;
  font-size: 10.5pt; break-inside: avoid; page-break-inside: avoid;
}
.rodape .resp { font-weight: bold; font-size: 11.5pt; color: #1b3a5c; }
.rodape .linha { margin-top: 1.5mm; color: #333333; }
.rodape .aviso { margin-top: 3mm; font-size: 10pt; color: #555555; }
@media print { body { font-size: 11.5pt; } .folha { padding: 0; } }
"""


def _fase_html(indice, nome, texto):
    return (
        '      <li data-n="{n}">\n'
        '        <span class="marcador"></span>\n'
        '        <p class="fase-nome">{nome}</p>\n'
        '        <p class="fase-texto">{texto}</p>\n'
        '      </li>'
    ).format(n=indice, nome=html.escape(nome), texto=html.escape(texto))


def montar_html(chave, area):
    fases = '\n'.join(
        _fase_html(i, nome, texto) for i, (nome, texto) in enumerate(area['fases'], start=1)
    )
    return """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>Mapa do Processo - {titulo}</title>
<style>{css}</style>
</head>
<body>
  <div class="folha">
    <div class="cabecalho">
      <div class="escritorio">{escritorio}</div>
      <h1>Mapa do seu processo</h1>
      <p class="subtitulo">{titulo} - {subtitulo}</p>
    </div>

    <div class="abertura">
      Este papel e seu. <strong>Leve para casa e guarde.</strong> Ele mostra, em ordem, por onde o seu
      processo passa do comeco ao fim. Um processo demora, e isso e normal: cada etapa tem o seu tempo.
      Voce nao precisa acompanhar nada sozinho. <strong>Todo mes nos enviamos um relatorio e um audio</strong>
      dizendo em que fase o seu processo esta e qual e o proximo passo.
    </div>

    <div class="hoje">
      <div class="hoje-titulo">Onde o seu processo esta hoje</div>
      <p class="hoje-texto">Seu advogado marca abaixo, e tambem no quadradinho da fase, onde voce esta agora.</p>
      <div class="linha-preencher">
        <div class="campo">
          <div class="rotulo">Fase numero</div>
          <div class="traco"></div>
        </div>
        <div class="campo">
          <div class="rotulo">Data</div>
          <div class="traco"></div>
        </div>
      </div>
      <div class="linha-preencher">
        <div class="campo">
          <div class="rotulo">Proximo passo</div>
          <div class="traco"></div>
        </div>
      </div>
      <div class="linha-preencher">
        <div class="campo">
          <div class="rotulo">O que voce precisa providenciar</div>
          <div class="traco"></div>
        </div>
      </div>
    </div>

    <ol class="fases">
{fases}
    </ol>

    <div class="nota">
      <span class="nota-titulo">Uma coisa que acontece o tempo todo</span>
      {aviso}
    </div>

    <div class="rodape">
      <div class="resp">{responsavel}</div>
      <div class="linha">{escritorio}</div>
      <div class="linha">{endereco}</div>
      <div class="linha">{contato}</div>
      <div class="aviso">Ficou com duvida sobre alguma fase? Fale com a gente pelo WhatsApp do escritorio.</div>
    </div>
  </div>
</body>
</html>
""".format(
        css=CSS,
        escritorio=html.escape(ESCRITORIO),
        titulo=html.escape(area['titulo']),
        subtitulo=html.escape(area['subtitulo']),
        responsavel=html.escape(area['responsavel']),
        endereco=html.escape(ENDERECO),
        contato=html.escape(CONTATO),
        aviso=html.escape(AVISO_INTIMACAO),
        fases=fases,
    )


def gerar(chave):
    area = AREAS[chave]
    os.makedirs(SAIDA, exist_ok=True)
    destino = os.path.join(SAIDA, 'mapa_processo_{}.html'.format(chave))
    with open(destino, 'w', encoding='utf-8') as arquivo:
        arquivo.write(montar_html(chave, area))
    return destino


def main():
    parser = argparse.ArgumentParser(
        description='Gera o mapa do processo em HTML pronto para imprimir (A4 retrato).'
    )
    parser.add_argument('area', nargs='?', choices=sorted(AREAS), help='area do processo')
    parser.add_argument('--todas', action='store_true', help='gera o mapa de todas as areas')
    args = parser.parse_args()

    if not args.area and not args.todas:
        parser.error('informe a area ou use --todas. Areas: ' + ', '.join(sorted(AREAS)))

    chaves = sorted(AREAS) if args.todas else [args.area]
    for chave in chaves:
        caminho = gerar(chave)
        print('Mapa gerado: {} ({} fases)'.format(caminho, len(AREAS[chave]['fases'])))
    print('Imprima em A4 retrato. Marque a fase atual a mao antes de entregar ao cliente.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
