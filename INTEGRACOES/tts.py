"""
Sintese de voz (texto -> audio) para os relatorios enviados ao cliente.

Backend padrao: edge-tts (voz neural pt-BR, sem chave de API).
    pip install edge-tts

O texto do relatorio sai da maquina para o servico de voz da Microsoft. Se o
escritorio nao quiser isso, basta rodar os relatorios com --sem-audio: o texto
continua sendo gerado normalmente e o advogado grava o audio a mao.

Vozes pt-BR disponiveis no edge-tts:
    pt-BR-AntonioNeural   (masculina)
    pt-BR-FranciscaNeural (feminina)
    pt-BR-ThalitaNeural   (feminina)
"""
import asyncio
import os

VOZ_PADRAO = os.getenv('TTS_VOZ', 'pt-BR-AntonioNeural')
RITMO_PADRAO = os.getenv('TTS_RITMO', '-8%')  # um pouco mais devagar: publico idoso/rural


def disponivel():
    try:
        import edge_tts  # noqa: F401
        return True
    except ImportError:
        return False


def gerar_audio(texto, caminho_saida, voz=None, ritmo=None):
    """
    Grava o texto como .mp3 em caminho_saida. Retorna True se gerou.

    Nao levanta excecao: se o TTS falhar, o relatorio de texto continua valendo
    e o advogado grava o audio a mao.
    """
    if not texto or not texto.strip():
        return False
    if not disponivel():
        print('   AVISO: edge-tts nao instalado (pip install edge-tts) - audio nao gerado')
        return False

    import edge_tts

    voz = voz or VOZ_PADRAO
    ritmo = ritmo or RITMO_PADRAO
    os.makedirs(os.path.dirname(os.path.abspath(caminho_saida)), exist_ok=True)

    async def _falar():
        com = edge_tts.Communicate(texto, voice=voz, rate=ritmo)
        await com.save(caminho_saida)

    try:
        asyncio.run(_falar())
    except Exception as e:
        print(f'   AVISO: falha ao gerar audio ({str(e)[:80]}) - siga so com o texto')
        return False
    return os.path.exists(caminho_saida) and os.path.getsize(caminho_saida) > 0


def texto_para_fala(texto):
    """
    Adapta o texto escrito para ser ouvido: tira marcacao, cabecalho e numero de
    processo (ninguem quer ouvir 20 digitos), e deixa as frases curtas.
    """
    import re
    linhas = []
    for linha in texto.splitlines():
        linha = linha.strip()
        if not linha:
            continue
        if linha.startswith('#') or set(linha) <= set('-=_'):
            continue
        if re.match(r'^\d{7}-\d{2}\.\d{4}', linha):
            continue
        linha = re.sub(r'\*\*(.+?)\*\*', r'\1', linha)
        linha = re.sub(r'^[-*]\s*', '', linha)
        linha = re.sub(r'\b\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}\b',
                       'o numero que consta no seu relatorio', linha)
        linhas.append(linha)
    return ' '.join(linhas)
