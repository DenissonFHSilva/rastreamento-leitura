import schedule
import time
import os
import shutil
from src.agrupador import agrupar_por_cnpj_conteudo
from src.smtp_envio import enviar_email_smtp
from src.config import (
    CAMINHO_PDF,
    CAMINHO_ENVIADOS,
    ENVIO_HORARIO,
    REMETENTE,
    PLANILHA_CLIENTES
)

def enviar_emails_agrupados():
    grupos = agrupar_por_cnpj_conteudo(CAMINHO_PDF)
    for cnpj, arquivos in grupos.items():
        try:
            enviar_email_smtp(cnpj, arquivos)
            for arq in arquivos:
                shutil.move(arq, os.path.join(CAMINHO_ENVIADOS, os.path.basename(arq)))
        except Exception as e:
            print(f"[ERRO] {cnpj}: {e}")

def iniciar_agendamento():
    schedule.every().day.at(ENVIO_HORARIO).do(enviar_emails_agrupados)
    print(f"[⏳] Envio agendado para {ENVIO_HORARIO}")
    while True:
        schedule.run_pending()
        time.sleep(60)
