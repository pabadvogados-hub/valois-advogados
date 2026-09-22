"""
Integracao com a Evolution API - WhatsApp do escritorio.

Usada para enviar ao cliente o relatorio mensal (texto + audio) e avisos.
A Evolution API e gratuita e roda no proprio servidor/maquina do escritorio.

.env:
    EVOLUTION_URL=http://localhost:8080
    EVOLUTION_API_KEY=...
    EVOLUTION_INSTANCIA=valois

Endpoints usados:
    POST /message/sendText/{instancia}
    POST /message/sendWhatsAppAudio/{instancia}   (audio como mensagem de voz)
    POST /message/sendMedia/{instancia}           (PDF/documento)
    GET  /instance/connectionState/{instancia}
"""
import base64
import logging
import os

import requests

log = logging.getLogger('integracoes.evolution')

TIMEOUT = 60


def _base():
    return (os.getenv('EVOLUTION_URL') or '').rstrip('/')


def _instancia():
    return os.getenv('EVOLUTION_INSTANCIA') or ''


def _headers():
    key = os.getenv('EVOLUTION_API_KEY')
    if not key:
        log.warning('EVOLUTION_API_KEY ausente no .env')
        return None
    return {'apikey': key, 'Content-Type': 'application/json'}


def configurado():
    return bool(_base() and _instancia() and os.getenv('EVOLUTION_API_KEY'))


def normalizar_numero(telefone):
    """(28) 99981-5672 -> 5528999815672. Retorna '' se nao parecer telefone."""
    d = ''.join(c for c in str(telefone or '') if c.isdigit())
    if d.startswith('55'):
        d = d[2:]
    if len(d) not in (10, 11):
        return ''
    return '55' + d


def conectado():
    """True se a instancia esta conectada ao WhatsApp."""
    if not configurado():
        return False
    try:
        r = requests.get(f'{_base()}/instance/connectionState/{_instancia()}',
                         headers=_headers(), timeout=TIMEOUT)
        if r.status_code != 200:
            return False
        estado = (r.json() or {}).get('instance', {}).get('state')
        return estado == 'open'
    except Exception as e:
        log.warning(f'connectionState: {e}')
        return False


def enviar_texto(telefone, mensagem):
    """Envia texto. Retorna True/False."""
    numero = normalizar_numero(telefone)
    if not numero:
        log.warning(f'telefone invalido: {telefone}')
        return False
    if not configurado():
        log.warning('Evolution API nao configurada no .env')
        return False
    payload = {'number': numero, 'text': mensagem}
    try:
        r = requests.post(f'{_base()}/message/sendText/{_instancia()}',
                          headers=_headers(), json=payload, timeout=TIMEOUT)
    except Exception as e:
        log.warning(f'sendText: {e}')
        return False
    if r.status_code in (200, 201):
        return True
    log.warning(f'sendText {r.status_code}: {r.text[:200]}')
    return False


def enviar_audio(telefone, caminho_mp3):
    """Envia um .mp3 como mensagem de voz do WhatsApp."""
    numero = normalizar_numero(telefone)
    if not numero or not configurado():
        return False
    if not os.path.exists(caminho_mp3):
        log.warning(f'audio nao encontrado: {caminho_mp3}')
        return False
    with open(caminho_mp3, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode()
    payload = {'number': numero, 'audio': b64, 'encoding': True}
    try:
        r = requests.post(f'{_base()}/message/sendWhatsAppAudio/{_instancia()}',
                          headers=_headers(), json=payload, timeout=TIMEOUT * 2)
    except Exception as e:
        log.warning(f'sendWhatsAppAudio: {e}')
        return False
    if r.status_code in (200, 201):
        return True
    log.warning(f'sendWhatsAppAudio {r.status_code}: {r.text[:200]}')
    return False


def enviar_documento(telefone, caminho_arquivo, legenda=''):
    """Envia PDF/DOCX como documento."""
    numero = normalizar_numero(telefone)
    if not numero or not configurado():
        return False
    if not os.path.exists(caminho_arquivo):
        return False
    with open(caminho_arquivo, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode()
    payload = {
        'number': numero,
        'mediatype': 'document',
        'fileName': os.path.basename(caminho_arquivo),
        'media': b64,
    }
    if legenda:
        payload['caption'] = legenda
    try:
        r = requests.post(f'{_base()}/message/sendMedia/{_instancia()}',
                          headers=_headers(), json=payload, timeout=TIMEOUT * 2)
    except Exception as e:
        log.warning(f'sendMedia: {e}')
        return False
    if r.status_code in (200, 201):
        return True
    log.warning(f'sendMedia {r.status_code}: {r.text[:200]}')
    return False
