import os
from collections import defaultdict
from src.extrair_cnpj import extrair_cnpj_pdf

def agrupar_por_cnpj_conteudo(pasta):
    """
    Percorre todos os PDFs da pasta informada, extrai o CNPJ de cada um
    e agrupa os arquivos por CNPJ detectado.
    """
    grupos = defaultdict(list)

    for nome_arquivo in os.listdir(pasta):
        if not nome_arquivo.lower().endswith('.pdf'):
            continue

        caminho = os.path.join(pasta, nome_arquivo)
        try:
            cnpj = extrair_cnpj_pdf(caminho)
            if cnpj:
                grupos[cnpj].append(caminho)
            else:
                print(f"[⚠] CNPJ não encontrado em: {nome_arquivo}")
        except Exception as e:
            print(f"[❌] Erro ao processar {nome_arquivo}: {e}")

    return grupos
