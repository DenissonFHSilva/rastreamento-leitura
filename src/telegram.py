import requests
from src.config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID  # Garante que as credenciais vêm do config.py

def enviar_mensagem(texto):
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
        print("📨 [Telegram] Mensagem enviada com sucesso!")
    except requests.exceptions.HTTPError as e:
        print(f"⚠️ [Telegram] Erro HTTP: {e.response.status_code} → {e.response.text}")
    except requests.exceptions.RequestException as e:
        print(f"⚠️ [Telegram] Erro na requisição: {e}")
