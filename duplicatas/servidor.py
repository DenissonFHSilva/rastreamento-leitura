from flask import Flask, request
import pandas as pd
import os
from datetime import datetime
from src.telegram import enviar_mensagem  # ✅ Notificação via Telegram

app = Flask(__name__)
LOG_PATH = 'webhook/aberturas_log.xlsx'

@app.route('/webhook-abertura', methods=['POST'])
def registrar_abertura():
    dados = request.form
    print(f"[DEBUG] Webhook recebido: {dados}")  # 🔍 Log para Render

    email = dados.get('recipient')
    timestamp = dados.get('timestamp')
    evento = dados.get('event')

    if evento == 'opened' and email and timestamp:
        try:
            momento = datetime.fromtimestamp(float(timestamp))
        except Exception as e:
            print(f"[ERRO] Timestamp inválido: {timestamp} → {e}")
            return 'Erro no timestamp', 400

        registro = {'email': email, 'aberto_em': momento}

        try:
            if os.path.exists(LOG_PATH):
                df = pd.read_excel(LOG_PATH)
                df = pd.concat([df, pd.DataFrame([registro])], ignore_index=True)
            else:
                df = pd.DataFrame([registro])
            df.to_excel(LOG_PATH, index=False)
        except Exception as e:
            print(f"[ERRO] Falha ao salvar log: {e}")

        # ✅ Enviar notificação para o Telegram
        msg = (
            f"📬 *Cliente abriu o e-mail!*\n"
            f"📧 Email: `{email}`\n"
            f"🕒 Hora: {momento.strftime('%d/%m %H:%M')}"
        )
        try:
            enviar_mensagem(msg)
        except Exception as e:
            print(f"[ERRO] Falha ao enviar Telegram: {e}")

    return 'OK'
