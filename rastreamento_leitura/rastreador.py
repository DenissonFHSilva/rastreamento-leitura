from flask import Flask, request, render_template
from datetime import datetime
import sqlite3
from src.telegram import enviar_telegram  # ou from telegram import enviar_telegram, se estiver fora da pasta 'src'

app = Flask(__name__)
DB_PATH = 'registro.db'

def registrar_confirmacao(cnpj, ip):
    # Garante conexão e criação da tabela
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS leitura_confirmada (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cnpj TEXT,
            ip TEXT,
            data_hora TEXT
        )
    ''')

    # Registra a confirmação
    data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute('INSERT INTO leitura_confirmada (cnpj, ip, data_hora) VALUES (?, ?, ?)',
              (cnpj, ip, data_hora))
    conn.commit()
    conn.close()

    # Log local
    print(f'✅ CNPJ {cnpj} confirmou leitura às {data_hora} (IP: {ip})')

    # 🔔 Notifica no Telegram
    mensagem = f"✅ *Confirmação de leitura recebida*\n📌 CNPJ: *{cnpj}*\n🕒 {data_hora}\n🌐 IP: `{ip}`"
    enviar_telegram(mensagem)

@app.route('/confirmar/<cnpj>')
def confirmar(cnpj):
    ip = request.remote_addr
    registrar_confirmacao(cnpj, ip)

    # Dados para o template
    ano = datetime.now().year
    horario = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    return render_template('confirmacao.html', cnpj=cnpj, horario=horario, ano=ano)

# Para ambiente local apenas:
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
