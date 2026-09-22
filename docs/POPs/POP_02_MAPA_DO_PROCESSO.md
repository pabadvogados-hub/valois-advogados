# POP 02 — Mapa do Processo entregue ao cliente

**Escritório:** Welington Valois Advogados Associados
**Aplica-se a:** todos os advogados (cada um pela sua área), estagiários e secretaria
**Responsável pelo POP:** Dr. Welington Dias Valois (OAB/ES 34.912)
**Origem:** reunião interna de alinhamento (item 2 da pauta)

---

## 1. O que é e para que serve

Todo cliente que **fecha contrato** recebe, impresso, um **mapa do processo**: um desenho simples com
todas as fases do processo, para ele **levar para casa**. Junto com o mapa vai **um chocolate**.

O mapa é desenhado mesmo — é para o cliente **entender**, não para impressionar. Boa parte do público
do escritório é do interior, rural, com pouca familiaridade com termo jurídico. Se o cliente não entende
o mapa sozinho em casa, o mapa está errado.

Efeito esperado: cliente que sabe onde está e o que vem depois liga menos, cobra menos e fica menos
ansioso. Isso conversa direto com o relatório mensal (POP 05).

---

## 2. Quem faz o quê

| Etapa | Quem |
|---|---|
| Modelo padrão do mapa | Dr. Welington + equipe (uma vez só) |
| Versão do mapa da área | **advogado responsável pela área** |
| Imprimir e montar o kit (mapa + chocolate) | secretaria (Kesia Reder) |
| Entregar ao cliente e explicar | advogado ou estagiário que fechou o contrato |
| Marcar no mapa onde o processo está | advogado, à mão, na entrega e nas revisões |

Áreas e responsáveis pela versão do mapa:

- Previdenciário — Dra. Priscila Araujo de Matos (OAB/ES 39.600)
- Criminal — Dr. Welington Dias Valois (OAB/ES 34.912) e Dr. Guilherme Mota Lopes Costa (OAB/ES 44.599)
- Família e sucessões — Dra. Derlira Garcia Pimentel Soares (OAB/ES 27.296)
- Bancário — Dr. Heliézer de Medeiros Pontes (OAB/ES 38.904)
- Cível / consumidor — Dra. Gisele Teófilo de Avila (OAB/ES 23.868)

---

## 3. O que o mapa precisa conter

O mapa deve conter **todas as fases do processo**, incluindo:

- Petição inicial
- Contestação
- Réplica
- Audiência de instrução e julgamento
- Alegações finais
- Despachos
- Intimações
- Sentença
- E as demais fases próprias da área

Regras de linguagem:

1. Cada fase tem um **nome técnico** e, embaixo, uma **explicação do dia a dia**.
   Exemplo: *Réplica — é a nossa resposta ao que o outro lado alegou.*
2. Nada de sigla solta, latim ou artigo de lei no mapa do cliente.
3. Fases numeradas, em ordem, de cima para baixo.
4. **Não colocar prazo em dia/mês que não seja certo.** Onde o tempo varia, escrever que varia.
   Se for preciso prazo e não houver certeza, escrever **[CONFERIR]** e resolver com o advogado da área
   antes de imprimir.
5. Rodapé com o nome e a OAB do advogado responsável pela área e o contato do escritório.

---

## 4. Passo a passo — criar a versão da área

**Quem faz:** advogado responsável pela área.

1. Parta do **modelo padrão** do escritório.
2. Liste as fases reais do seu tipo de processo, na ordem em que acontecem de verdade na comarca em que
   o escritório atua.
   - No **previdenciário**, lembre que existe a **fase administrativa no INSS antes da judicial** e que o
     ajuizamento é na **comarca local (competência delegada)**, não na Justiça Federal — a Federal só entra
     em grau de recurso. Incluir perícia médica e estudo social onde couber.
3. Escreva a explicação em linguagem simples de cada fase.
4. Gere o mapa com o script do escritório:
   ```
   python UTILS/mapa_do_processo.py previdenciario
   ```
   Áreas disponíveis: `previdenciario`, `criminal`, `familia`, `bancario`, `civel`.
   O arquivo sai em `SAIDA/mapa_processo_<area>.html`, em A4 retrato, pronto para imprimir.
5. Abra o HTML, confira, e ajuste o que estiver fora da realidade da sua área.
6. Mostre a versão ao Dr. Welington antes de virar a versão oficial da área.

---

## 5. Passo a passo — entregar ao cliente

**Quem faz:** advogado ou estagiário que fechou o contrato, com apoio da secretaria.

1. Fechado o contrato, imprimir o mapa da área do cliente.
2. Montar o kit: **mapa impresso + chocolate**.
3. Marcar **à mão**, na caixa "onde seu processo está hoje", a fase atual.
4. Entregar ao cliente e **explicar o mapa com ele na frente**, do começo ao fim, apontando onde ele está
   e qual é a próxima etapa.
5. Dizer ao cliente que ele leva o mapa para casa e que, todo mês, vai receber o relatório com a fase
   atualizada (POP 05).

**O que NÃO fazer:**

- Não entregar o mapa sem explicar. Papel entregue calado não reduz ansiedade nem ligação.
- Não entregar mapa de outra área só porque "é parecido".
- Não prometer data de sentença, data de audiência ou data de pagamento que não esteja marcada.

---

## 6. Validação com psicólogo — PENDENTE

Depois do modelo pronto, o mapa será apresentado a um psicólogo para **análise sob a ótica da neurociência
e da psicologia**, avaliando se o desenho realmente reduz a ansiedade do cliente e se a sequência é
compreendida por quem tem pouca escolaridade.

Status: **pendente**. Enquanto não houver essa análise, o mapa roda na versão atual.

- **[DEFINIR com o Dr. Welington]** qual profissional fará a análise e em que prazo.
- **[DEFINIR com o Dr. Welington]** o que exatamente será submetido: só o modelo padrão ou as versões de
  todas as áreas.

---

## 7. POP por etapa do mapa

Ficou definido que, ao fazer o mapa, o escritório faz também **o POP de cada etapa** — ou seja, para cada
fase do mapa existe um procedimento interno dizendo o que o escritório faz naquela fase.

Status: **pendente**, depende do modelo padrão fechado.

- **[DEFINIR com o Dr. Welington]** se o POP de etapa é único para todas as áreas ou um por área.
- **[DEFINIR com o Dr. Welington]** prazo para cada advogado entregar o POP das etapas da sua área.

---

## 8. Entregáveis deste POP

| Entregável | Quem | Quando |
|---|---|---|
| Modelo padrão do mapa | Dr. Welington + equipe | uma vez |
| Mapa da área (HTML + impresso) | advogado da área | uma vez, e sempre que a prática mudar |
| Kit mapa + chocolate entregue | quem fechou o contrato | no fechamento do contrato |
| Análise do psicólogo | Dr. Welington | pendente |
| POP de cada etapa do mapa | advogado da área | pendente |
