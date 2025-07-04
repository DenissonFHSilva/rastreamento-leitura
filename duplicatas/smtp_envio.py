import os
import ssl
import smtplib
import time
import pandas as pd
from email.message import EmailMessage
from src.config import REMETENTE, PLANILHA_CLIENTES, SMTP_EMAIL, SMTP_SENHA
from src.log_envios import registrar_envio
from src.telegram import enviar_telegram

def buscar_dados_cliente(cnpj):
    df = pd.read_excel(PLANILHA_CLIENTES, dtype=str).fillna('')
    df['cnpj'] = df['cnpj'].str.replace(r'\D', '', regex=True)
    cliente = df[df['cnpj'] == cnpj]
    if cliente.empty:
        raise ValueError(f"CNPJ {cnpj} não encontrado na planilha.")
    cliente = cliente.iloc[0]
    return cliente['email'], cliente['responsavel'], cliente['empresa']

def enviar_email_smtp(cnpj, anexos):
    destino, responsavel, empresa = buscar_dados_cliente(cnpj)
    timestamp = int(time.time())

    # ✉️ Criação do e-mail
    msg = EmailMessage()
    msg['Subject'] = f"Documentos do Departamento Pessoal – {empresa}"
    msg['From'] = REMETENTE
    msg['To'] = destino

    # 🔗 Link de rastreamento (visível) e pixel (invisível)
    dominio_render = "https://rastreamento-leitura.onrender.com"  # ✅ Substitua pelo seu domínio real se necessário
    link_confirmacao = f"{dominio_render}/confirmar/{cnpj}"
    pixel = f'<img src="{dominio_render}/webhook-abertura?recipient={destino}&timestamp={timestamp}&event=opened" style="display:none;" />'

    corpo_html = f"""
    <html>
    <body style="font-family: sans-serif;">
        <p>Olá {responsavel},</p>
        <p>Segue em anexo os documentos do período referentes à empresa <strong>{empresa}</strong>.</p>
        <p style="margin-top: 20px;">
            📩 <a href="{link_confirmacao}" style="color: #00875a; font-weight: bold;">
                Clique aqui para confirmar o recebimento
            </a>
        </p>
        {pixel}  <!-- 🔍 Pixel de rastreamento invisível -->
        <p style="font-size: 12px; color: #888; margin-top: 30px;">DP Automação – Atendimento Automático</p>
    </body>
    </html>
    """

    # Texto alternativo
    corpo_texto = f"""Olá {responsavel},

Segue em anexo os documentos do período referentes à empresa {empresa}.

Para confirmar o recebimento, acesse:
{link_confirmacao}

Atenciosamente,
Departamento Pessoal
"""

    msg.set_content(corpo_texto)
    msg.add_alternative(corpo_html, subtype='html')

    # 📎 Anexos
    for caminho_anexo in anexos:
        try:
            with open(caminho_anexo, 'rb') as f:
                dados = f.read()
                nome = os.path.basename(f.name)
                msg.add_attachment(dados, maintype='application', subtype='pdf', filename=nome)
        except Exception as e:
            print(f"❌ Erro ao anexar {caminho_anexo}: {e}")

    # 📤 Envio com SMTP + SSL
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(SMTP_EMAIL, SMTP_SENHA)
        smtp.send_message(msg)

    print(f"[SMTP] ✅ E-mail enviado para {empresa} → {destino}")

    # 🔹 Log + Telegram
    registrar_envio(cnpj, destino, empresa, anexos)
    mensagem = f"📬 Documentos enviados para *{empresa}*\n📧 Email: {destino}"
    enviar_telegram(mensagem)
