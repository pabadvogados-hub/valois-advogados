# Guia de instalacao - Agentes Valois no Claude.ai

Cada arquivo `valois-*.md` desta pasta e um agente independente. Instale um **Project** por agente.

## Passo a passo (Claude.ai)
1. Claude.ai > Projects > New project. Nome: "Valois - <Area>" (ex.: "Valois - Previdenciario").
2. Abra o arquivo `valois-<area>.md`, remova o bloco de frontmatter (as linhas entre `---`) e cole o
   restante em **Custom instructions**.
3. Em **Project knowledge**, suba as pecas-modelo do escritorio (1-2 por tipo), o timbrado e as leis/sumulas de referencia.
4. Teste com um caso real anonimizado e confira se a saida termina com a marca "PRONTA PARA REVISAO".

## Regras
- A IA nunca protocola.
- Envie arquivos por link do Drive, nao cole processos inteiros no chat.
- Ela ajuda no trabalho; modelos simples (procuracao, declaracao, contrato) usam o modelo do escritorio.
- Depois de pronta a peca, peca ao agente uma versao "parte contraria" rebatendo os pontos e ajuste.

## Claude Code (opcional)
Copie o `.md` para `.claude/agents/` do repositorio; o frontmatter e mantido.

## Manutencao
Edite o `.md`, cole novamente nas Custom instructions e atualize a knowledge base ao receber novas pecas.
