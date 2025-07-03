from flask import Flask, request, render_template
from datetime import datetime
import sqlite3
import os
from src.telegram import enviar_telegram  # Notificador via Telegram

# 🔧 Configurações iniciais
app = Flask(__name__)
DB_PATH = 'registro.db'

# 🔐 Cria banco de dados e registra confirmação
def registrar_confirmacao(cnpj, ip):
    try:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)  # Se necessário
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
        print(f'✅ Leitura registrada: {cnpj} às {data_hora} (IP: {ip})')
    except Exception as e:
        print(f'❌ Erro ao registrar no banco: {e}')
    finally:
        conn.close()

    # 📲 Envia notificação via Telegram
    mensagem = (
        f"✅ *Confirmação de leitura recebida*\n"
        f"📌 CNPJ: *{cnpj}*\n"
        f"🕒 {data_hora}\n"
        f"🌐 IP: `{ip}`"
    )
    enviar_telegram(mensagem)

# 🌐 Rota principal de confirmação
@app.route('/confirmar/<cnpj>')
def confirmar(cnpj):
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    registrar_confirmacao(cnpj, ip)

    ano = datetime.now().year
    horario = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    return render_template('confirmacao.html', cnpj=cnpj, horario=horario, ano=ano)

# ▶️ Execução local
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
