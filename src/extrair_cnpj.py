import re
import pdfplumber

def extrair_cnpj_pdf(caminho_pdf):
    """
    Extrai o primeiro CNPJ encontrado no conteúdo textual de um PDF.
    Retorna o CNPJ apenas com números, ou None se nada for encontrado.
    """
    try:
        with pdfplumber.open(caminho_pdf) as pdf:
            texto = ''.join(pagina.extract_text() or '' for pagina in pdf.pages)

        padrao_cnpj = r'\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}'
        encontrados = re.findall(padrao_cnpj, texto)

        if encontrados:
            return re.sub(r'\D', '', encontrados[0])  # Remove pontuação
    except Exception as e:
        print(f"[❌] Erro ao extrair CNPJ de '{caminho_pdf}': {e}")

    return None
