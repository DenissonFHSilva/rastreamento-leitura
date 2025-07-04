from flask import Flask, request, render_template
from datetime import datetime
import sqlite3
import os
from src.telegram import enviar_telegram  # ou from telegram import enviar_telegram, se estiver fora da pasta 'src'

app = Flask(__name__)
DB_PATH = 'registro.db'

def registrar_confirmacao(cnpj, ip):
    try:
        # Garante que a pasta do banco existe, se aplicável
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True) if os.path.dirname(DB_PATH) else None

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS leitura_confirmada (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cnpj TEXT NOT NULL,
                ip TEXT NOT NULL,
                data_hora TEXT NOT NULL
            )
        ''')

        data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        c.execute(
            'INSERT INTO leitura_confirmada (cnpj, ip, data_hora) VALUES (?, ?, ?)',
            (cnpj, ip, data_hora)
        )
        conn.commit()

        print(f'✅ CNPJ {cnpj} confirmou leitura às {data_hora} (IP: {ip})')

        # 🔔 Notifica via Telegram
        mensagem = (
            f"✅ *Confirmação de leitura recebida*\n"
            f"📌 CNPJ: *{cnpj}*\n"
            f"🕒 {data_hora}\n"
            f"🌐 IP: `{ip}`"
        )
        enviar_telegram(mensagem)

    except Exception as e:
        print(f'❌ Erro ao registrar confirmação ou enviar Telegram: {e}')

    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/confirmar/<cnpj>')
def confirmar(cnpj):
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    registrar_confirmacao(cnpj, ip)

    ano = datetime.now().year
    horario = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    return render_template('confirmacao.html', cnpj=cnpj, horario=horario, ano=ano)

# 🔧 Rota de teste opcional para validar envio manual do Telegram
@app.route('/ping')
def ping():
    try:
        enviar_telegram("📡 Teste de notificação manual direto do servidor!")
        return "✅ Notificação enviada com sucesso!"
    except Exception as e:
        return f"❌ Erro ao testar Telegram: {e}"

# ▶️ Executa localmente ou no Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
