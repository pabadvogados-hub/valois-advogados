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
ENDERECO = 'Rua Galaor Rios, 289, Centro - Iúna/ES  |  Ibatiba/ES  |  Irupi/ES'
CONTATO = 'WhatsApp e telefone: (28) 99981-5672  |  welingtonvaloisadv@gmail.com'

AVISO_INTIMACAO = (
    'Durante todo o processo o juiz vai dando ordens (os despachos) e o cartório vai avisando '
    'o advogado de cada passo (as intimações). Isso acontece do começo ao fim, entre uma fase '
    'e outra. Você não precisa acompanhar nada disso: quem acompanha é o seu advogado, e todo '
    'mês você recebe o relatório dizendo em que fase o seu processo está.'
)

AREAS = {
    'previdenciario': {
        'titulo': 'Aposentadoria e benefícios do INSS',
        'subtitulo': 'O caminho do seu pedido, do começo ao fim',
        'responsavel': 'Dra. Priscila Araujo de Matos - OAB/ES 39.600',
        'fases': [
            ('Conversa e documentos',
             'Você conta a sua história e nós separamos os documentos: identidade, CPF, '
             'comprovante de residência, documentos do trabalho e, se for o caso, os laudos '
             'e receitas do médico.'),
            ('Pedido no INSS',
             'Primeiro o pedido é feito no próprio INSS. Essa é a fase administrativa. '
             'Sem passar por aqui, na maioria dos casos não dá para entrar na Justiça.'),
            ('Perícia médica do INSS',
             'Se o seu benefício depende de doença ou incapacidade, o INSS marca uma perícia. '
             'Um médico do INSS examina você e diz se concorda que você está incapacitado. '
             'É obrigatório comparecer no dia marcado.'),
            ('Avaliação social do INSS',
             'Em alguns benefícios, além do médico, uma assistente social do INSS avalia como '
             'você vive e quanto a sua família ganha.'),
            ('Resposta do INSS',
             'O INSS responde: aceita o pedido e começa a pagar, ou nega. Se negar, ou se demorar '
             'demais, nós levamos o caso para a Justiça.'),
            ('Entrada da ação na Justiça',
             'Escrevemos a petição inicial, que é o documento em que contamos o seu caso ao juiz '
             'e pedimos o benefício. A ação entra aqui mesmo, no fórum da comarca da região - '
             'você não precisa viajar para a Justiça Federal.'),
            ('O INSS se defende',
             'O INSS apresenta a contestação, que é a defesa dele. Ele diz ao juiz por que acha '
             'que você não tem direito.'),
            ('Nossa resposta',
             'A réplica é a nossa resposta à defesa do INSS. Aqui nós derrubamos, um por um, os '
             'argumentos que o INSS usou contra você.'),
            ('Perícia médica do juiz',
             'Se o caso envolve doença, o juiz escolhe um médico de confiança dele para examinar '
             'você de novo. Esse médico não trabalha para o INSS nem para nós. O dia e o lugar são '
             'avisados com antecedência.'),
            ('Estudo social',
             'Uma assistente social escolhida pelo juiz vai até a sua casa ou propriedade para ver '
             'como a família vive e trabalha. Muito comum nos casos de trabalhador rural e de '
             'benefício para quem tem pouca renda.'),
            ('Audiência',
             'É o dia em que você e as suas testemunhas falam com o juiz. Na audiência de instrução '
             'e julgamento as testemunhas contam o que sabem do seu trabalho e da sua vida. '
             'Você será avisado com antecedência e nós preparamos tudo com você antes.'),
            ('Últimas palavras das partes',
             'As alegações finais são o resumo que cada lado escreve no fim, juntando tudo o que '
             'ficou provado. É a nossa última palavra antes da decisão.'),
            ('Sentença',
             'É a decisão do juiz. Ele diz se você tem direito ao benefício e a partir de quando.'),
            ('Recurso',
             'Se qualquer um dos lados não concordar com a decisão, o caso sobe para a Justiça '
             'Federal, que revisa a sentença. Essa etapa nem sempre acontece.'),
            ('Benefício pago',
             'Ganhando em definitivo, o INSS é obrigado a começar a pagar o benefício e a pagar '
             'também o que ficou atrasado desde a data reconhecida pelo juiz.'),
        ],
    },
    'criminal': {
        'titulo': 'Processo criminal',
        'subtitulo': 'O caminho da sua defesa, do começo ao fim',
        'responsavel': 'Dr. Welington Dias Valois - OAB/ES 34.912  |  '
                       'Dr. Guilherme Mota Lopes Costa - OAB/ES 44.599',
        'fases': [
            ('Conversa e documentos',
             'Você conta o que aconteceu e nós reunimos tudo o que ajuda a sua defesa: documentos, '
             'mensagens, nomes de pessoas que podem servir de testemunha.'),
            ('Investigação',
             'A polícia investiga e reúne o que encontrou no inquérito policial. Nesta fase ainda '
             'não há acusação formal. Se você for chamado para depor, nós vamos junto.'),
            ('Acusação',
             'O Ministério Público analisa a investigação e decide: arquiva o caso ou apresenta a '
             'denúncia, que é a acusação formal contra você.'),
            ('O juiz decide se aceita a acusação',
             'O juiz lê a denúncia e decide se o processo começa ou não.'),
            ('Nossa defesa escrita',
             'Apresentamos a resposta à acusação: é o documento em que mostramos ao juiz o outro '
             'lado da história e indicamos as nossas testemunhas.'),
            ('Audiência',
             'É o dia principal. Na audiência de instrução e julgamento as testemunhas são ouvidas '
             'e, no fim, o juiz ouve você. Nós preparamos tudo com você antes.'),
            ('Últimas palavras das partes',
             'Nas alegações finais cada lado escreve o resumo do que ficou provado. É a nossa última '
             'palavra antes da decisão.'),
            ('Sentença',
             'É a decisão do juiz: absolvição ou condenação. Estando condenado, a sentença diz qual '
             'é a pena e como ela será cumprida.'),
            ('Recurso',
             'Se a decisão não for favorável, recorremos ao tribunal, que revisa a sentença. '
             'A acusação também pode recorrer.'),
            ('Fim do processo',
             'Quando não cabe mais recurso, o processo termina. Havendo condenação, começa a fase '
             'de cumprimento da pena, que continua sendo acompanhada por nós.'),
        ],
    },
    'familia': {
        'titulo': 'Família e herança',
        'subtitulo': 'O caminho do seu processo, do começo ao fim',
        'responsavel': 'Dra. Derlira Garcia Pimentel Soares - OAB/ES 27.296',
        'fases': [
            ('Conversa e documentos',
             'Você conta a sua situação e nós separamos os documentos: certidões, documentos dos '
             'bens, comprovantes de despesa e de renda.'),
            ('Tentativa de acordo',
             'Sempre que for possível e seguro para você, tentamos resolver por acordo. Acordo é '
             'mais rápido, mais barato e menos desgastante.'),
            ('Entrada da ação',
             'Não havendo acordo, escrevemos a petição inicial, que é o documento em que contamos '
             'o seu caso ao juiz e dizemos o que você está pedindo.'),
            ('Audiência de conciliação',
             'O juiz chama os dois lados para uma nova tentativa de acordo, com a ajuda de uma '
             'pessoa preparada para isso. Se houver acordo aqui, o processo termina cedo.'),
            ('O outro lado se defende',
             'A outra parte apresenta a contestação, que é a defesa dela, dizendo ao juiz por que '
             'discorda do seu pedido.'),
            ('Nossa resposta',
             'A réplica é a nossa resposta à defesa da outra parte. Rebatemos ponto a ponto o que '
             'foi alegado contra você.'),
            ('Produção de provas',
             'Juntamos os documentos e, quando o caso pede, o juiz determina estudo social, '
             'avaliação psicológica ou avaliação dos bens.'),
            ('Audiência',
             'Na audiência de instrução e julgamento você e as suas testemunhas falam com o juiz. '
             'Você é avisado com antecedência e nós preparamos tudo com você antes.'),
            ('Últimas palavras das partes',
             'Nas alegações finais cada lado escreve o resumo do que ficou provado. É a nossa última '
             'palavra antes da decisão.'),
            ('Sentença',
             'É a decisão do juiz sobre o que foi pedido: divórcio, guarda, pensão, partilha, '
             'herança.'),
            ('Recurso',
             'Se algum dos lados não concordar, o caso sobe para o tribunal, que revisa a decisão. '
             'Essa etapa nem sempre acontece.'),
            ('Cumprimento da decisão',
             'Com a decisão definitiva, cuidamos de fazer valer o que foi decidido: averbação no '
             'cartório, transferência dos bens, pagamento da pensão.'),
        ],
    },
    'bancario': {
        'titulo': 'Problema com banco ou financiamento',
        'subtitulo': 'O caminho do seu processo, do começo ao fim',
        'responsavel': 'Dr. Heliézer de Medeiros Pontes - OAB/ES 38.904',
        'fases': [
            ('Conversa e documentos',
             'Você conta o que está acontecendo e nós separamos os documentos: contrato, carnê, '
             'extratos, comprovantes de pagamento e as cobranças que você recebeu.'),
            ('Análise do contrato',
             'Estudamos o seu contrato e as contas para descobrir o que está sendo cobrado a mais '
             'e o que dá para discutir na Justiça. Aqui nós dizemos com sinceridade se vale a pena.'),
            ('Tentativa de solução direta',
             'Quando for o caso, procuramos o banco antes de processar, para tentar resolver sem '
             'ação judicial.'),
            ('Entrada da ação',
             'Não havendo solução, escrevemos a petição inicial, que é o documento em que contamos '
             'o seu caso ao juiz e dizemos o que você está pedindo.'),
            ('O banco se defende',
             'O banco apresenta a contestação, que é a defesa dele, com os motivos pelos quais '
             'acha que a cobrança está correta.'),
            ('Nossa resposta',
             'A réplica é a nossa resposta à defesa do banco. Rebatemos ponto a ponto o que ele '
             'alegou contra você.'),
            ('Perícia nas contas',
             'Quando o caso exige, o juiz nomeia um perito - um profissional que entende de '
             'cálculo - para refazer as contas do contrato e dizer quanto foi cobrado a mais.'),
            ('Audiência',
             'Nem todo processo de banco tem audiência. Quando houver, você é avisado com '
             'antecedência e nós preparamos tudo com você antes.'),
            ('Sentença',
             'É a decisão do juiz: ele diz se a cobrança do banco estava errada e o que precisa '
             'ser corrigido ou devolvido.'),
            ('Recurso',
             'Bancos costumam recorrer. Nesse caso o processo sobe para o tribunal, que revisa a '
             'decisão.'),
            ('Cumprimento da decisão',
             'Com a decisão definitiva, cuidamos de fazer valer o resultado: correção da dívida, '
             'devolução do que foi pago a mais, retirada do seu nome dos cadastros.'),
        ],
    },
    'civel': {
        'titulo': 'Direito do consumidor e causas cíveis',
        'subtitulo': 'O caminho do seu processo, do começo ao fim',
        'responsavel': 'Dra. Gisele Teófilo de Avila - OAB/ES 23.868',
        'fases': [
            ('Conversa e documentos',
             'Você conta o que aconteceu e nós separamos as provas: nota fiscal, contrato, fotos, '
             'mensagens, protocolos de atendimento e comprovantes de pagamento.'),
            ('Reclamação antes da ação',
             'Quando for o caso, registramos reclamação na empresa, no órgão de defesa do consumidor '
             'ou enviamos uma notificação, para tentar resolver sem processo.'),
            ('Entrada da ação',
             'Não resolvendo, escrevemos a petição inicial, que é o documento em que contamos o seu '
             'caso ao juiz e dizemos o que você está pedindo.'),
            ('Audiência de conciliação',
             'O juiz chama os dois lados para tentar um acordo. Se houver acordo aqui, o processo '
             'termina cedo e você recebe mais rápido.'),
            ('A outra parte se defende',
             'A empresa ou a pessoa processada apresenta a contestação, que é a defesa dela.'),
            ('Nossa resposta',
             'A réplica é a nossa resposta à defesa do outro lado. Rebatemos ponto a ponto o que '
             'foi alegado contra você.'),
            ('Produção de provas',
             'Juntamos os documentos e, quando o caso pede, o juiz determina perícia ou vistoria.'),
            ('Audiência',
             'Na audiência de instrução e julgamento você e as suas testemunhas falam com o juiz. '
             'Você é avisado com antecedência e nós preparamos tudo com você antes.'),
            ('Sentença',
             'É a decisão do juiz sobre o que foi pedido: devolução do dinheiro, conserto, '
             'cancelamento da cobrança, indenização.'),
            ('Recurso',
             'Se algum dos lados não concordar, o caso sobe para o tribunal, que revisa a decisão. '
             'Essa etapa nem sempre acontece.'),
            ('Recebimento',
             'Com a decisão definitiva, cobramos o cumprimento: o pagamento a você ou a obrigação '
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
  position: relative; padding: 0 12mm 6mm 20mm; break-inside: avoid; page-break-inside: avoid;
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

MODELO = """<!DOCTYPE html>
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
      Este papel &eacute; seu. <strong>Leve para casa e guarde.</strong> Ele mostra, em ordem, por onde o seu
      processo passa do come&ccedil;o ao fim. Um processo demora, e isso &eacute; normal: cada etapa tem o seu
      tempo. Voc&ecirc; n&atilde;o precisa acompanhar nada sozinho.
      <strong>Todo m&ecirc;s n&oacute;s enviamos um relat&oacute;rio e um &aacute;udio</strong> dizendo em que
      fase o seu processo est&aacute; e qual &eacute; o pr&oacute;ximo passo.
    </div>

    <div class="hoje">
      <div class="hoje-titulo">Onde o seu processo est&aacute; hoje</div>
      <p class="hoje-texto">Seu advogado marca abaixo, e tamb&eacute;m no quadradinho da fase, onde voc&ecirc; est&aacute; agora.</p>
      <div class="linha-preencher">
        <div class="campo">
          <div class="rotulo">Fase n&uacute;mero</div>
          <div class="traco"></div>
        </div>
        <div class="campo">
          <div class="rotulo">Data</div>
          <div class="traco"></div>
        </div>
      </div>
      <div class="linha-preencher">
        <div class="campo">
          <div class="rotulo">Pr&oacute;ximo passo</div>
          <div class="traco"></div>
        </div>
      </div>
      <div class="linha-preencher">
        <div class="campo">
          <div class="rotulo">O que voc&ecirc; precisa providenciar</div>
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
      <div class="aviso">Ficou com d&uacute;vida sobre alguma fase? Fale com a gente pelo WhatsApp do escrit&oacute;rio.</div>
    </div>
  </div>
</body>
</html>
"""


def _fase_html(indice, nome, texto):
    return (
        '      <li data-n="{n}">\n'
        '        <span class="marcador"></span>\n'
        '        <p class="fase-nome">{nome}</p>\n'
        '        <p class="fase-texto">{texto}</p>\n'
        '      </li>'
    ).format(n=indice, nome=html.escape(nome), texto=html.escape(texto))


def montar_html(area):
    fases = '\n'.join(
        _fase_html(i, nome, texto) for i, (nome, texto) in enumerate(area['fases'], start=1)
    )
    return MODELO.format(
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
    os.makedirs(SAIDA, exist_ok=True)
    destino = os.path.join(SAIDA, 'mapa_processo_{}.html'.format(chave))
    with open(destino, 'w', encoding='utf-8') as arquivo:
        arquivo.write(montar_html(AREAS[chave]))
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

    for chave in (sorted(AREAS) if args.todas else [args.area]):
        caminho = gerar(chave)
        print('Mapa gerado: {} ({} fases)'.format(caminho, len(AREAS[chave]['fases'])))
    print('Imprima em A4 retrato. Marque a fase atual a mao antes de entregar ao cliente.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
