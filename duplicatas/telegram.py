import requests
from src.config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID  # Credenciais vindas do config.py

def enviar_mensagem(texto):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ [Telegram] Token ou Chat ID não configurado. Mensagem não enviada.")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": texto,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }

    try:
        resposta = requests.post(url, json=payload, timeout=10)
        resposta.raise_for_status()
        print(f"📨 [Telegram] Mensagem enviada com sucesso! Status {resposta.status_code}")
        return True
    except requests.exceptions.HTTPError as e:
        print(f"❌ [Telegram] Erro HTTP {e.response.status_code}: {e.response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ [Telegram] Falha ao enviar mensagem: {e}")
    
    return False

# Alias de compatibilidade
enviar_telegram = enviar_mensagem
