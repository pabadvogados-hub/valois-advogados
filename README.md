# Welington Valois Advogados Associados - Central de Automacoes

Plataforma de automacao juridica do escritorio **Welington Valois Advogados Associados**
(Dr. Welington Dias Valois - OAB/ES 34.912 e OAB/MG 249.303 - Iuna, Ibatiba e Irupi/ES).

Areas: **Previdenciario** (carro-chefe, ~65%), **Criminal** (~25%) e Familia/Sucessoes, Bancario e
Civel/Consumidor.

> **A IA nunca protocola.** Toda peca e para revisao humana do advogado responsavel antes de qualquer protocolo.

## Agentes juridicos de IA
Em `agentes_claude/` (Claude.ai Projects) e `.claude/agents/` (subagentes do Claude Code):

| Agente | Area | Status |
|---|---|---|
| `valois-previdenciario` | Previdenciario - generalista (INSS administrativo e judicial) | Base tecnica - calibrar com pecas reais |
| `valois-iniciais` | Previdenciario - peticoes iniciais | Base tecnica - calibrar |
| `valois-quesitos` | Quesitos de pericia medica e estudo social | Base tecnica - calibrar |
| `valois-criminal` | Criminal | Base generica - calibrar |
| `valois-familia-sucessoes` | Familia e sucessoes | Base generica - calibrar |
| `valois-bancario` | Bancario / juros abusivos / renegociacao | Base generica - calibrar |
| `valois-civel-consumidor` | Civel, indenizacoes, consumidor | Base generica - calibrar |

Ver `agentes_claude/GUIA_INSTALACAO_CLAUDE_AI.md`.

## Frentes de automacao
| Squad | O que faz | Comando |
|---|---|---|
| INTAKE | Ficha, contrato, procuracao, declaracao, ZapSign, cadastro ADVBOX | `python INTAKE/main.py ...` |
| FINANCEIRO | Fechamento, conciliacao Asaas x ADVBOX, cobranca com lembretes | `python FINANCEIRO/fechamento_mensal.py MM/YYYY` |
| OPERACIONAL | Tarefas, processos, prazos, pecas; agente VALOIS.IA (webhook) | `python OPERACIONAL/main.py tarefas` |
| SYNC | Docs assinados ZapSign -> Drive | `python SYNC/sync_assinados.py` |

> Credenciais (ADVBOX, Asaas, ZapSign, Google, WhatsApp) ainda NAO foram recebidas - chegam em canal seguro apos a
> assinatura do contrato. Ate la rodam apenas os agentes de IA sobre documentos soltos. Ver `docs/ONBOARDING.md`.

## Instalacao rapida
```bash
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp config/.env.example config/.env                # preencher com as credenciais do escritorio
```
Deploy 24/7 em VPS: `docs/DEPLOY_VPS.md`.
