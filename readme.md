# 📦 DP_AUTOMACAO_MAILGUN

**Automatize o envio de documentos do Departamento Pessoal com segurança, rastreamento e notificações em tempo real.**  
Este sistema foi desenvolvido para facilitar o envio mensal de documentos (como holerites e informes) por e-mail, rastrear a confirmação de leitura via link personalizado, registrar todas as ações e emitir alertas via Telegram.

---

## ✨ Funcionalidades

- 📂 Leitura automática de PDFs na pasta `entrada_pdf/`
- 🔍 Extração do CNPJ do conteúdo do PDF (OCR textual)
- 📎 Agrupamento e envio de anexos por empresa
- ✉️ Corpo do e-mail personalizado com link de confirmação
- 🌐 Página de confirmação hospedada via Flask
- 💾 Registro de leitura em banco SQLite (`registro.db`)
- 📬 Notificação via Telegram quando a leitura é confirmada
- 📊 Log de todos os envios em Excel (`envios_log.xlsx`)
- 🧑‍💻 Interface gráfica (GUI) para cadastrar clientes via Tkinter
- 💻 Compatível com deploy em Render.com

---

## 🗂️ Estrutura do Projeto

```txt
DP_AUTOMACAO_MAILGUN/
├── dados/
│   ├── clientes.xlsx             # Lista de clientes
│   └── envios_log.xlsx          # Log dos e-mails enviados
├── entrada_pdf/                 # PDFs a enviar
├── enviados/                    # PDFs já processados
├── rastreamento_leitura/
│   ├── rastreador.py            # Servidor Flask
│   ├── registro.db              # Banco de confirmações
│   ├── requirements.txt         # Dependências
│   ├── Procfile                 # Deploy no Render
│   ├── static/logo.png
│   └── templates/confirmacao.html
├── src/
│   ├── config.py
│   ├── telegram.py
│   ├── smtp_envio.py
│   ├── agrupador.py
│   ├── extrair_cnpj.py
│   ├── log_envios.py
│   └── __init__.py
├── manual.py
├── clientes_gui.py
├── logo.png
├── build/
├── dist/
├── clientes_gui.spec
└── README.md
🧪 Como usar
1. Instale as dependências
bash
pip install -r rastreamento_leitura/requirements.txt
Requisitos: Python 3.10+, Flask, pandas, pdfplumber, PyPDF2, openpyxl, requests

2. Cadastre seus clientes
bash
python clientes_gui.py
Os dados são salvos em: dados/clientes.xlsx

3. Coloque os PDFs em entrada_pdf/
Os arquivos devem conter o CNPJ no conteúdo (OCR).

4. Dispare os envios
bash
python manual.py
5. Inicie o rastreamento
bash
cd rastreamento_leitura
python rastreador.py
Acesse no navegador:

http://localhost:5000/confirmar/<cnpj>
📲 Notificações via Telegram
Configure o arquivo src/config.py:

python
TELEGRAM_TOKEN = '...'
TELEGRAM_CHAT_ID = '...'
☁️ Deploy no Render
Suba o projeto no GitHub. Crie um Web Service no Render. Configure:

txt
Build command: pip install -r rastreamento_leitura/requirements.txt
Start command: gunicorn rastreador:app
No smtp_envio.py, altere:

python
link_confirmacao = f"http://localhost:5000/confirmar/{cnpj}"
Para:

python
link_confirmacao = f"https://seudominio.onrender.com/confirmar/{cnpj}"
🧊 Gerar o .exe da interface
bash
pip install pyinstaller
pyinstaller --onefile --windowed clientes_gui.py
Executável final em:

dist/clientes_gui.exe
🔒 .gitignore sugerido
venv/
.env
__pycache__/
*.pyc
*.pyo
build/
dist/
*.spec
registro.db
dados/envios_log.xlsx
✍️ Créditos
Desenvolvido por Denisson Documentado com auxílio do Copilot ✨
