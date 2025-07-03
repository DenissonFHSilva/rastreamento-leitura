import os
import re
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox

CAMINHO_PLANILHA = 'dados/clientes.xlsx'

# --- Utilitários de dados ---
def carregar_clientes():
    if not os.path.exists(CAMINHO_PLANILHA):
        return pd.DataFrame(columns=['cnpj', 'empresa', 'email', 'responsavel'])
    df = pd.read_excel(CAMINHO_PLANILHA, dtype=str).fillna('')
    df['cnpj'] = df['cnpj'].str.replace(r'\D', '', regex=True).str.zfill(14)
    return df

def salvar_clientes(df):
    try:
        pasta = os.path.dirname(CAMINHO_PLANILHA)
        if pasta and not os.path.exists(pasta):
            os.makedirs(pasta)
            print(f"📁 Pasta criada: {pasta}")
        df.to_excel(CAMINHO_PLANILHA, index=False)
        print(f"✅ Planilha atualizada: {CAMINHO_PLANILHA}")
    except Exception as e:
        print(f"❌ Erro ao salvar a planilha: {e}")
        messagebox.showerror("Erro", f"Não foi possível salvar o arquivo.\n\n{e}")

# --- Funcionalidades GUI ---
def limpar_formulario():
    for var in [empresa_var, cnpj_var, email_var, resp_var]:
        var.set('')
    tabela.selection_remove(tabela.selection())

def carregar_tabela():
    for i in tabela.get_children():
        tabela.delete(i)
    df = carregar_clientes()
    for _, row in df.iterrows():
        tabela.insert('', 'end', values=(row['cnpj'], row['empresa'], row['email'], row['responsavel']))

def excluir_cliente():
    item = tabela.selection()
    if not item:
        messagebox.showwarning("Atenção", "Nenhum cliente selecionado.")
        return
    valores = tabela.item(item[0])['values']
    cnpj = re.sub(r'\D', '', str(valores[0])).zfill(14)

    if not messagebox.askyesno("Confirmar exclusão", f"Deseja remover o cliente de CNPJ {cnpj}?"):
        return

    df = carregar_clientes()
    df_filtrado = df[df['cnpj'] != cnpj]

    if len(df_filtrado) == len(df):
        messagebox.showwarning("Aviso", "CNPJ não encontrado. Nenhum cliente removido.")
        return

    salvar_clientes(df_filtrado)
    carregar_tabela()
    limpar_formulario()
    messagebox.showinfo("Sucesso", "Cliente excluído com sucesso.")

def inserir_ou_atualizar():
    cnpj = re.sub(r'\D', '', cnpj_var.get()).zfill(14)
    empresa = empresa_var.get().strip()
    email = email_var.get().strip()
    responsavel = resp_var.get().strip()

    if not empresa or not cnpj or not email:
        messagebox.showerror("Erro", "Campos obrigatórios: Empresa, CNPJ e E-mail.")
        return

    df = carregar_clientes()
    if cnpj in df['cnpj'].values:
        idx = df[df['cnpj'] == cnpj].index[0]
        df.loc[idx] = [cnpj, empresa, email, responsavel]
        msg = "Cliente atualizado com sucesso."
    else:
        novo = pd.DataFrame([[cnpj, empresa, email, responsavel]], columns=df.columns)
        df = pd.concat([df, novo], ignore_index=True)
        msg = "Cliente adicionado com sucesso."

    salvar_clientes(df)
    carregar_tabela()
    limpar_formulario()
    messagebox.showinfo("Sucesso", msg)

def selecionar(event):
    item = tabela.selection()
    if item:
        valores = tabela.item(item[0])['values']
        cnpj_var.set(valores[0])
        empresa_var.set(valores[1])
        email_var.set(valores[2])
        resp_var.set(valores[3])

# --- Interface gráfica ---
root = tk.Tk()
root.title("Cadastro de Clientes – DP Automação")

frm = ttk.Frame(root, padding=12)
frm.grid()

cnpj_var = tk.StringVar()
empresa_var = tk.StringVar()
email_var = tk.StringVar()
resp_var = tk.StringVar()

ttk.Label(frm, text="CNPJ:").grid(column=0, row=0, sticky='w')
ttk.Entry(frm, textvariable=cnpj_var).grid(column=1, row=0)

ttk.Label(frm, text="Empresa:").grid(column=0, row=1, sticky='w')
ttk.Entry(frm, textvariable=empresa_var, width=40).grid(column=1, row=1)

ttk.Label(frm, text="E-mail:").grid(column=0, row=2, sticky='w')
ttk.Entry(frm, textvariable=email_var, width=40).grid(column=1, row=2)

ttk.Label(frm, text="Responsável:").grid(column=0, row=3, sticky='w')
ttk.Entry(frm, textvariable=resp_var, width=40).grid(column=1, row=3)

ttk.Button(frm, text="Salvar", command=inserir_ou_atualizar).grid(column=0, row=4, pady=10)
ttk.Button(frm, text="Limpar", command=limpar_formulario).grid(column=1, row=4, sticky='w')
ttk.Button(frm, text="Excluir", command=excluir_cliente).grid(column=2, row=4, sticky='w')

cols = ('CNPJ', 'Empresa', 'E-mail', 'Responsável')
tabela = ttk.Treeview(root, columns=cols, show='headings')
for col in cols:
    tabela.heading(col, text=col)
    tabela.column(col, width=150)

tabela.bind('<<TreeviewSelect>>', selecionar)
tabela.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

carregar_tabela()
root.mainloop()
