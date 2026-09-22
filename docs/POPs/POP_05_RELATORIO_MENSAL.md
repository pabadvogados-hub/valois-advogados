# POP 05 — Relatório mensal de situação processual ao cliente

**Escritório:** Welington Valois Advogados Associados
**Aplica-se a:** todos os advogados, com apoio de estagiários, secretaria e da automação
**Responsável pelo POP:** Dr. Welington Dias Valois (OAB/ES 34.912)
**Origem:** reunião interna de alinhamento (item 5 da pauta)

---

## 1. A regra

> **Até o 5º dia útil de cada mês**, cada cliente recebe o **relatório da situação processual** do seu
> processo, acompanhado de **um áudio** explicando em que fase o processo está e qual será a próxima etapa.

E, antes disso:

> **Os advogados precisam fazer relatório de TODOS os processos que acompanham.**

Objetivo declarado: ter um resumo do caso, saber qual será o próximo andamento e manter o cliente informado
de todo o processo. **Resultado esperado: menos mensagens e menos insatisfação do cliente.**

O relatório conversa com o **mapa do processo** (POP 02): o mapa mostra o caminho inteiro, o relatório diz
onde o cliente está nesse caminho hoje.

---

## 2. Quem faz o quê

| Etapa | Quem |
|---|---|
| Manter o processo atualizado para o relatório sair certo | advogado da área |
| Geração do texto e do áudio em lote | automação do escritório |
| **Revisão do texto e do áudio** | **advogado responsável pela área** |
| Envio ao cliente pelo WhatsApp | secretaria, após a liberação do advogado |
| Registro do envio | secretaria |

---

## 2.1 Como a automação entra

```bash
python OPERACIONAL/relatorio_mensal.py                 # gera tudo do mês corrente
python OPERACIONAL/relatorio_mensal.py --responsavel PRISCILA
python OPERACIONAL/relatorio_mensal.py --exemplo       # demonstração, sem tocar no ADVBOX
python OPERACIONAL/relatorio_mensal.py --enviar        # dispara SÓ o que já foi revisado
```

A automação lê os processos ativos do ADVBOX, escreve o texto, gera o áudio e deixa tudo em
`SAIDA/relatorios/AAAA-MM/`, com um `INDICE_PARA_REVISAO.csv`. O advogado abre o índice, confere
cada relatório, escreve o nome dele na coluna `revisado_por` e marca `enviar` com SIM. O envio se
recusa a rodar sem revisor identificado e se ainda houver `[PREENCHER]` no texto — a automação
prepara, o advogado assina.

## 3. O que vai em cada relatório

1. **Resumo do caso** — o que o cliente pediu e contra quem, em duas ou três frases, em linguagem simples.
2. **Fase atual** — onde o processo está hoje, com o nome da fase do mapa do processo.
3. **O que aconteceu desde o último relatório** — sem termo técnico solto.
4. **Próximo andamento** — o que vem depois e o que depende do cliente (documento, comparecimento, perícia).
5. **Áudio** do advogado (ou da automação, revisado) explicando a fase atual e a próxima etapa.

Regras de conteúdo:

- Linguagem do dia a dia. Se usar termo técnico, explique na mesma frase.
- **Não prometer data que não está marcada** (sentença, pagamento, resultado).
- Não afirmar resultado provável como se fosse certo.
- Se algum dado do processo não estiver confirmado, o relatório não sai com ele: corrige ou marca
  **[CONFERIR]** e o advogado resolve antes do envio.

---

## 4. Passo a passo do mês

**Quem faz:** advogado da área, automação e secretaria.

1. **Até o último dia útil do mês anterior** — cada advogado confere se os processos da sua área estão com
   andamento atualizado e com o próximo passo claro. Relatório de audiência (POP 03) já lançado.
2. **No 1º dia útil do mês** — a automação gera, **em lote**, o texto do relatório e o **áudio** de cada
   cliente, a partir dos andamentos e do que o advogado registrou. Sai tudo separado por área.
3. **Do 1º ao 4º dia útil** — o **advogado responsável pela área revisa** cada relatório e cada áudio:
   - confere se a fase está certa;
   - confere se o próximo andamento está certo;
   - corrige linguagem, corta promessa indevida, resolve qualquer **[CONFERIR]**;
   - regrava o áudio se o áudio gerado não estiver correto ou não estiver claro;
   - **libera** o material para envio.
4. **Até o 5º dia útil** — a secretaria envia ao cliente pelo WhatsApp, na conversa já etiquetada por área
   (POP 04), e registra o envio.
5. Dúvida do cliente depois do relatório segue o POP 04: operacional é secretaria, jurídico é o advogado
   da área.

---

## 5. Papel da automação — e o limite dela

A automação **gera o texto e o áudio em lote**, para todos os clientes de uma vez. Ela existe para tirar o
trabalho braçal do advogado, não para substituir o advogado.

> **A IA nunca envia sozinha.** Nenhum relatório e nenhum áudio vai ao cliente sem que o advogado
> responsável pela área tenha lido, ouvido e liberado.

O que a automação **não** faz:

- Não decide estratégia nem opina sobre o mérito do caso.
- Não inventa andamento que não está nos autos.
- Não envia ao cliente por conta própria.
- Não cria prazo processual. Onde não houver certeza, escreve **[CONFERIR]** para o advogado resolver.

---

## 6. Pendências

- **[DEFINIR com o Dr. Welington]** se o relatório vai como mensagem de texto, PDF ou os dois.
- **[DEFINIR com o Dr. Welington]** se o áudio é gravado pelo advogado ou gerado pela automação com voz
  sintetizada, e se essa escolha muda por área.
- **[DEFINIR com o Dr. Welington]** o que fazer com processo sem nenhuma movimentação no mês: manda
  relatório dizendo que não houve movimentação, ou não manda.
- **[DEFINIR com o Dr. Welington]** se o processo criminal e o processo em segredo de justiça entram no
  envio automático ou têm tratamento à parte.
- **[DEFINIR com o Dr. Welington]** onde fica arquivado o relatório enviado (pasta do processo no Drive
  ou lançamento no sistema).

---

## 7. Entregáveis deste POP

| Entregável | Quem | Quando |
|---|---|---|
| Processos da área atualizados | advogado da área | até o último dia útil do mês anterior |
| Relatórios + áudios gerados em lote | automação | 1º dia útil |
| Relatórios e áudios revisados e liberados | advogado da área | até o 4º dia útil |
| Relatório + áudio enviados e registrados | secretaria | **até o 5º dia útil** |
