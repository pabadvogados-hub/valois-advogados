# Padroes de Documentos - Welington Valois Advogados Associados

## Formatacao Obrigatoria (informada pelo escritorio em 16/09/2026)
- Fonte: Segoe UI
- Tamanho do corpo: 12pt
- Espacamento entre linhas: 1,15
- Linguagem: tecnica, formal e objetiva
- Alinhamento: Justificado
- Recuo da primeira linha: 1,25cm (PROVISORIO - confirmar com o escritorio)
- Titulos principais: maiusculo, negrito, justificado
- Subtitulos: negrito, justificado
- Citacoes: recuo 4cm esquerda, italico, 11pt, aspas
- Toda peca sai no timbrado do escritorio (`config/timbrado_modelo.docx`). Nunca em folha branca.
- O timbrado mudou em 09/2026: "Advocacia e Consultoria Juridica" virou "Advogados Associados". Usar SO o novo.

## Convencao de Nomes de Arquivos
- Ficha: `{Nome do Cliente} - Ficha Cliente - {Data}`
- Contrato: `{Nome do Cliente} - Contrato de Honorarios`
- Procuracao: `{Nome do Cliente} - Procuracao`
- Declaracao: `{Nome do Cliente} - Declaracao de Hipossuficiencia`

## Estrutura de Pastas (Cliente) - por area, depois cliente
```
{AREA}/
  {NOME DO CLIENTE (MAIUSCULO)}/
    ATOS INTERNOS/
    DOCUMENTOS DO CLIENTE/
    PASTA DO CLIENTE/
```
Areas: PREVIDENCIARIO, CRIMINAL, FAMILIA E SUCESSOES, BANCARIO, CIVEL E CONSUMIDOR.

## Assinatura
- Local: Iuna/ES, Ibatiba/ES ou Irupi/ES (conforme a comarca da peca)
- Escritorio: Welington Valois Advogados Associados
- Advogado responsavel pela area assina a peca (ver `config/equipe.py`); Dr. Welington Dias Valois - OAB/ES 34.912 assina criminal e o que ele pegar.

## Regra de ouro
A IA nunca protocola. Toda peca termina no Drive marcada "PRONTA PARA REVISAO" do advogado responsavel.
