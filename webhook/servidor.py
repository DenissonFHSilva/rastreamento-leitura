from flask import Flask, request
import pandas as pd
import os
from datetime import datetime
from src.config import CALLMEBOT_NUMERO, CALLMEBOT_APIKEY

app = Flask(__name__)
LOG_PATH = 'webhook/aberturas_log.xlsx'

def enviar_whatsapp(mensagem, numero, apikey):
    import requests
    url = f"https://api.callmebot.com/whatsapp.php?phone={numero}&text={mensagem}&apikey={apikey}"
    requests.get(url)

@app.route('/webhook-abertura', methods=['POST'])
def registrar_abertura():
    dados = request.form
    email = dados.get('recipient')
    timestamp = dados.get('timestamp')
    evento = dados.get('event')

    if evento == 'opened':
        momento = datetime.fromtimestamp(float(timestamp))
        registro = {'email': email, 'aberto_em': momento}

        if os.path.exists(LOG_PATH):
            df = pd.read_excel(LOG_PATH)
            df = pd.concat([df, pd.DataFrame([registro])], ignore_index=True)
        else:
            df = pd.DataFrame([registro])
        df.to_excel(LOG_PATH, index=False)

        msg = f"*📬 Cliente abriu o e-mail!*\nEmail: {email}\nHora: {momento.strftime('%d/%m %H:%M')}"
        enviar_whatsapp(msg, CALLMEBOT_NUMERO, CALLMEBOT_APIKEY)

    return 'OK'
