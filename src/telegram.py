import requests
from src.config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

def enviar_telegram(texto: str) -> None:
    """
    Envia uma mensagem formatada via Telegram para o chat ID definido no config.py.
    """

    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ [Telegram] Token ou Chat ID ausentes no arquivo config.py.")
        return

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
        print("✅ [Telegram] Mensagem enviada com sucesso!")
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code
        detalhe = e.response.text
        print(f"❌ [Telegram] Erro HTTP {status}: {detalhe}")
    except requests.exceptions.Timeout:
        print("❌ [Telegram] Timeout na tentativa de envio.")
    except requests.exceptions.RequestException as e:
        print(f"❌ [Telegram] Erro na requisição: {e}")
