# ✅ API de rastreamento com rota /leituras disponível

from flask import Flask, request, render_template, jsonify
from datetime import datetime
import sqlite3
import os
from src.telegram import enviar_telegram  # ou from telegram import enviar_telegram, se estiver fora da pasta 'src'

app = Flask(__name__)

# 📌 Caminho absoluto para o banco de dados
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'registro.db')
print(f"📁 Caminho do banco de dados em uso: {DB_PATH}")

# 🔐 Função para registrar a confirmação de leitura
def registrar_confirmacao(cnpj, ip):
    conn = None
    try:
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
        if conn:
            conn.close()

# 🏠 Rota raiz para evitar erro 404
@app.route('/')
def home():
    return '✅ API de rastreamento ativa. Acesse /leituras para ver os dados.'

# 🌐 Rota de confirmação de leitura
@app.route('/confirmar/<cnpj>')
def confirmar(cnpj):
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    registrar_confirmacao(cnpj, ip)

    ano = datetime.now().year
    horario = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    return render_template('confirmacao.html', cnpj=cnpj, horario=horario, ano=ano)

# 🧪 Rota de teste de Telegram
@app.route('/ping')
def ping():
    try:
        enviar_telegram("📡 Teste de notificação manual direto do servidor!")
        return "✅ Notificação enviada com sucesso!"
    except Exception as e:
        return f"❌ Erro ao testar Telegram: {e}"

# 📊 Rota de leitura dos registros
@app.route('/leituras')
def listar_leituras():
    try:
        print("📡 Rota /leituras acessada.")
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT cnpj, ip, data_hora FROM leitura_confirmada ORDER BY id DESC")
        registros = c.fetchall()
        conn.close()

        print(f"📊 Registros encontrados: {len(registros)}")
        dados = [{"cnpj": cnpj, "ip": ip, "data_hora": data_hora} for cnpj, ip, data_hora in registros]
        return jsonify(dados)
    except Exception as e:
        print(f"❌ Erro ao acessar rota /leituras: {e}")
        return jsonify({"erro": f"Falha ao acessar leituras: {e}"}), 500

# ▶️ Executa localmente ou no Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
