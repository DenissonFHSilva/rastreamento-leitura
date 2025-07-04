import os
import pandas as pd
from datetime import datetime

CAMINHO_LOG = 'dados/envios_log.xlsx'

def registrar_envio(cnpj, destino, empresa, arquivos):
    """
    Registra o envio de documentos para um cliente no arquivo Excel de log.
    """
    data_envio = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    nomes_arquivos = ', '.join(os.path.basename(a) for a in arquivos)

    novo_registro = {
        'data_envio': data_envio,
        'empresa': empresa,
        'cnpj': cnpj,
        'email': destino,
        'arquivos': nomes_arquivos
    }

    try:
        if os.path.exists(CAMINHO_LOG):
            df = pd.read_excel(CAMINHO_LOG, engine='openpyxl')
            df = pd.concat([df, pd.DataFrame([novo_registro])], ignore_index=True)
        else:
            df = pd.DataFrame([novo_registro])

        df.to_excel(CAMINHO_LOG, index=False, engine='openpyxl')
        print(f"[📋 LOG] Envio registrado para {empresa}")
    except Exception as e:
        print(f"[❌ LOG] Falha ao registrar envio para {empresa}: {e}")
