# POPs — Welington Valois Advogados Associados

Procedimentos Operacionais Padrão do escritório. Origem: roteiros das reuniões internas do
Dr. Welington Dias Valois (OAB/ES 34.912).

| POP | Assunto | Principais responsáveis |
|---|---|---|
| [POP 01](POP_01_USO_DA_IA.md) | Uso da IA: link do Drive, modelo do escritório, revisão adversarial | todos |
| [POP 02](POP_02_MAPA_DO_PROCESSO.md) | Mapa do processo impresso entregue ao cliente (com chocolate) | advogado da área + secretaria |
| [POP 03](POP_03_AUDIENCIA.md) | Audiência, testemunhas, relatório e controle do processo pela área | advogado da área |
| [POP 04](POP_04_WHATSAPP.md) | WhatsApp: etiqueta por área, quem responde o quê, postura um passo à frente | secretaria + advogado da área |
| [POP 05](POP_05_RELATORIO_MENSAL.md) | Relatório mensal ao cliente até o 5º dia útil, com áudio | advogado da área + secretaria |

## Regras que atravessam todos os POPs

- **A IA nunca protocola e nunca envia sozinha.** Tudo passa pela revisão do advogado responsável pela área.
- **Cada advogado responde pelos processos da sua área**, mesmo que outro advogado tenha feito a inicial.
- **Linguagem simples com o cliente.** O público do escritório é do interior e boa parte é rural.
- **Nunca inventar dado, prazo ou jurisprudência.** Sem certeza, escreve-se **[CONFERIR]** e resolve-se antes.
- Onde o procedimento ainda não foi definido, o texto traz **[DEFINIR com o Dr. Welington]**.

## Ferramenta ligada aos POPs

- `UTILS/mapa_do_processo.py` — gera o mapa do processo em HTML pronto para imprimir (POP 02):
  `python UTILS/mapa_do_processo.py previdenciario` → `SAIDA/mapa_processo_previdenciario.html`
  Áreas: `previdenciario`, `criminal`, `familia`, `bancario`, `civel`.
