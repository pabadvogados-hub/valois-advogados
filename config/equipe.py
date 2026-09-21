"""
Equipe / usuarios do escritorio - Welington Valois Advogados Associados.

Centraliza os IDs de usuario do ADVBOX e os papeis funcionais.
NUNCA hardcode IDs no codigo das automacoes: leia sempre deste arquivo.

TODO (onboarding): o escritorio usa ADVBOX (so lancamento de atividades, sem kanban),
mas ainda nao se confirmou se o plano tem API liberada. Enquanto os IDs estiverem None,
as automacoes que dependem deles ficam inativas/seguras.
"""
import os

# IDs de usuario no ADVBOX (painel ADVBOX > Usuarios). Podem vir do .env (recomendado).
USUARIOS_ADVBOX = {
    "RESPONSAVEL": os.getenv("ADVBOX_USER_RESPONSAVEL") or None,   # Dr. Welington Dias Valois (gestor principal)
    "OPERACIONAL": os.getenv("ADVBOX_USER_OPERACIONAL") or None,   # quem recebe tarefas operacionais
    "FINANCEIRO": os.getenv("ADVBOX_USER_FINANCEIRO") or None,     # quem lanca transacoes financeiras (secretaria)
}

# Papeis funcionais do escritorio (informados no briefing de 16/09/2026).
# Servem de referencia para roteamento de tarefas por area; IDs ADVBOX vem do .env.
EQUIPE = {
    "GESTOR_PRINCIPAL": "Welington Dias Valois (OAB/ES 34.912)",
    "GESTOR_IUNA": "Kauã Moreira Valois",
    "GESTORA_IBATIBA": "Gisele Teófilo de Avila (OAB/ES 23.868)",
    "GESTORA_PREVIDENCIARIO": "Priscila Araujo de Matos (OAB/ES 39.600)",
    "AREAS": {
        "PREVIDENCIARIO": "Priscila Araujo de Matos",
        "FAMILIA_SUCESSOES": "Derlira Garcia Pimentel Soares (OAB/ES 27.296)",
        "BANCARIO": "Heliézer de Medeiros Pontes (OAB/ES 38.904)",
        "CIVEL_CONSUMIDOR": "Gisele Teófilo de Avila (OAB/ES 23.868)",
        "CRIMINAL": "Welington Dias Valois e Guilherme Mota Lopes Costa (OAB/ES 44.599)",
    },
    "SECRETARIA": "Kesia Reder (agenda, WhatsApp e financeiro)",
}

# Papel usado no campo 'from' das tarefas (/posts).
USUARIO_PADRAO_TAREFAS = "RESPONSAVEL"


def id_usuario(papel):
    """Retorna o ID ADVBOX do papel informado (ou None se nao configurado)."""
    valor = USUARIOS_ADVBOX.get(papel)
    if valor in (None, ""):
        return None
    try:
        return int(valor)
    except (TypeError, ValueError):
        return valor
