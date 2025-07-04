import os
import re
import shutil
from collections import defaultdict
from PyPDF2 import PdfReader
from src.smtp_envio import enviar_email_smtp  # Certifique-se de que esse módulo está ok

PASTA_PDFS = 'entrada_pdf'
PASTA_ENVIADOS = 'enviados'

def extrair_cnpj(texto):
    padrao = r'\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}'
    encontrados = re.findall(padrao, texto)
    if encontrados:
        return re.sub(r'\D', '', encontrados[0])
    return None

def cnpj_do_pdf(caminho_pdf):
    try:
        leitor = PdfReader(caminho_pdf)
        texto = ''
        for pagina in leitor.pages:
            texto += pagina.extract_text() or ''
        return extrair_cnpj(texto)
    except Exception as e:
        print(f"❌ Erro ao ler PDF '{caminho_pdf}': {e}")
        return None

def coletar_anexos_por_cnpj():
    agrupados = defaultdict(list)
    for nome in os.listdir(PASTA_PDFS):
        if not nome.lower().endswith('.pdf'):
            continue
        caminho = os.path.join(PASTA_PDFS, nome)
        cnpj = cnpj_do_pdf(caminho)
        if cnpj:
            agrupados[cnpj].append(caminho)
        else:
            print(f"⚠️  CNPJ não encontrado em: {nome}")
    return agrupados

def enviar_para_todos():
    agrupados = coletar_anexos_por_cnpj()
    if not agrupados:
        print("📭 Nenhum CNPJ válido encontrado nos PDFs.")
        return

    os.makedirs(PASTA_ENVIADOS, exist_ok=True)

    for cnpj, anexos in agrupados.items():
        print(f"\n📤 Enviando para CNPJ: {cnpj} ({len(anexos)} anexo[s])")
        try:
            enviar_email_smtp(cnpj, anexos)

            for arquivo in anexos:
                destino = os.path.join(PASTA_ENVIADOS, os.path.basename(arquivo))
                shutil.move(arquivo, destino)

            print(f"📦 {len(anexos)} arquivo[s] movido[s] para '{PASTA_ENVIADOS}'")

        except Exception as e:
            print(f"❌ Erro ao enviar para {cnpj}: {e}")

if __name__ == '__main__':
    enviar_para_todos()
