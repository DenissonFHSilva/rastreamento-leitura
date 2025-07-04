# src/telegram.py

import requests
from src.config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

def enviar_telegram(mensagem: str) -> None:
    """
    Envia uma mensagem formatada via Telegram para o chat definido no config.py.
    """

    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ [Telegram] TOKEN ou CHAT_ID ausentes no config.py. Mensagem não enviada.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensagem,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }

    try:
        resposta = requests.post(url, json=payload, timeout=10)
        resposta.raise_for_status()
        print("✅ [Telegram] Mensagem enviada com sucesso!")
    except requests.exceptions.HTTPError as e:
        print(f"❌ [Telegram] Erro HTTP {e.response.status_code}: {e.response.text}")
    except requests.exceptions.Timeout:
        print("⏱️ [Telegram] Tempo de resposta excedido (timeout).")
    except requests.exceptions.RequestException as e:
        print(f"❌ [Telegram] Falha na requisição: {e}")
