import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import os
import json
import requests
import sqlite3

# Configurações iniciais
COR_FUNDO = "#f2f2f2"
FONTE_TITULO = ("Segoe UI", 18, "bold")
FONTE_BOTAO = ("Segoe UI", 12)
ESPACAMENTO = 10
ARQUIVO_CONFIG = "config_gui.json"


def abrir_clientes_gui():
    try:
        subprocess.Popen(["python", "clientes_gui.py"])
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao abrir cadastro: {e}")


def enviar_documentos():
    try:
        subprocess.run(["python", "src/smtp_envio.py"], check=True)
        messagebox.showinfo("Sucesso", "📤 Documentos enviados com sucesso!")
    except subprocess.CalledProcessError:
        messagebox.showerror("Erro", "Erro ao enviar documentos.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro inesperado: {e}")


def abrir_pasta_entrada():
    try:
        caminho = os.path.join(os.getcwd(), "entrada_pdf")
        os.startfile(caminho)
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível abrir a pasta: {e}")


def testar_telegram():
    try:
        with open(ARQUIVO_CONFIG) as f:
            config = json.load(f)
            link = config.get("LINK_RASTREAMENTO", "").strip()
            if not link:
                raise Exception("Link de rastreamento não definido nas configurações.")
            resposta = requests.get(f"{link}/ping")
            if "✅" in resposta.text:
                messagebox.showinfo("Telegram OK", resposta.text)
            else:
                messagebox.showwarning("Resposta recebida", resposta.text)
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao testar Telegram:\n{e}")


def ver_leituras():
    try:
        with open(ARQUIVO_CONFIG) as f:
            config = json.load(f)
            link = config.get("LINK_RASTREAMENTO", "").strip()
            if not link:
                raise Exception("Link de rastreamento não definido nas configurações.")

        resposta = requests.get(f"{link}/leituras")
        if resposta.status_code != 200:
            raise Exception(f"Erro HTTP {resposta.status_code}")

        registros = resposta.json()
        if not registros:
            messagebox.showinfo("📊 Leituras", "Nenhuma leitura confirmada ainda.")
            return

        janela_leituras = tk.Toplevel()
        janela_leituras.title("📊 Leituras Confirmadas (Servidor)")
        janela_leituras.geometry("600x400")
        janela_leituras.configure(bg=COR_FUNDO)

        colunas = ("CNPJ", "IP", "Data/Hora")
        tabela = ttk.Treeview(janela_leituras, columns=colunas, show="headings")

        for col in colunas:
            tabela.heading(col, text=col)
            tabela.column(col, anchor="center", stretch=True)

        for linha in registros:
            tabela.insert("", "end", values=(linha["cnpj"], linha["ip"], linha["data_hora"]))

        tabela.pack(expand=True, fill="both", padx=10, pady=10)

    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao buscar leituras do servidor:\n{e}")


def abrir_configuracoes():
    def salvar_configuracoes():
        config = {
            "TELEGRAM_TOKEN": token_var.get(),
            "TELEGRAM_CHAT_ID": chat_id_var.get(),
            "EMAIL_REMETENTE": email_var.get(),
            "LINK_RASTREAMENTO": link_var.get()
        }
        try:
            with open(ARQUIVO_CONFIG, "w") as f:
                json.dump(config, f, indent=4)
            messagebox.showinfo("✅ Sucesso", "Configurações salvas com sucesso!")
            config_win.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar configurações:\n{e}")

    try:
        with open(ARQUIVO_CONFIG) as f:
            config = json.load(f)
    except:
        config = {}

    config_win = tk.Toplevel()
    config_win.title("⚙️ Configurações")
    config_win.geometry("430x340")
    config_win.configure(bg=COR_FUNDO)

    tk.Label(config_win, text="Token do Telegram:", bg=COR_FUNDO).pack(pady=5)
    token_var = tk.StringVar(value=config.get("TELEGRAM_TOKEN", ""))
    tk.Entry(config_win, textvariable=token_var, width=50).pack()

    tk.Label(config_win, text="Chat ID:", bg=COR_FUNDO).pack(pady=5)
    chat_id_var = tk.StringVar(value=config.get("TELEGRAM_CHAT_ID", ""))
    tk.Entry(config_win, textvariable=chat_id_var, width=50).pack()

    tk.Label(config_win, text="E-mail Remetente:", bg=COR_FUNDO).pack(pady=5)
    email_var = tk.StringVar(value=config.get("EMAIL_REMETENTE", ""))
    tk.Entry(config_win, textvariable=email_var, width=50).pack()

    tk.Label(config_win, text="Link de Rastreamento:", bg=COR_FUNDO).pack(pady=5)
    link_var = tk.StringVar(value=config.get("LINK_RASTREAMENTO", ""))
    tk.Entry(config_win, textvariable=link_var, width=50).pack()

    tk.Button(config_win, text="💾 Salvar", font=FONTE_BOTAO, command=salvar_configuracoes).pack(pady=20)


# Interface principal
janela = tk.Tk()
janela.title("📦 DP Automação Mailgun - Painel de Controle")
janela.geometry("500x500")
janela.config(bg=COR_FUNDO)

tk.Label(janela, text="Painel de Envio & Rastreamento", font=FONTE_TITULO, bg=COR_FUNDO).pack(pady=(20, 10))

botoes = [
    ("📇 Cadastrar Empresas", abrir_clientes_gui),
    ("📂 Abrir Pasta PDFs", abrir_pasta_entrada),
    ("📤 Enviar Documentos", enviar_documentos),
    ("📊 Ver Leituras Confirmadas", ver_leituras),
    ("📡 Testar Telegram (/ping)", testar_telegram),
    ("⚙️ Configurações", abrir_configuracoes),
]

for texto, comando in botoes:
    tk.Button(janela, text=texto, font=FONTE_BOTAO, width=30, pady=8, command=comando).pack(pady=ESPACAMENTO)

tk.Label(janela, text="🧠 Sistema desenvolvido por Denisson", font=("Segoe UI", 9), bg=COR_FUNDO, fg="#555").pack(side="bottom", pady=15)

janela.mainloop()
