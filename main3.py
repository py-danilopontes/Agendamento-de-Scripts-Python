import time
import subprocess
import os
import schedule
from datetime import datetime
import pytz

tz = pytz.timezone("America/Sao_Paulo")

def executar_ciclo():
    print(f"[{datetime.now(tz)}] >> Rodando chamado_abertos.py", flush=True)
    subprocess.run(["python", "chamado_abertos.py"])

    pdf_path = "chamados_aberto-pendentes.pdf"
    timeout = 120
    waited = 0
    while not os.path.exists(pdf_path) and waited < timeout:
        print(f"[{datetime.now(tz)}] Aguardando criação do PDF...", flush=True)
        time.sleep(5)
        waited += 5

    if not os.path.exists(pdf_path):
        print(f"[{datetime.now(tz)}] Erro: PDF não foi gerado no tempo esperado!", flush=True)
        return

    print(f"[{datetime.now(tz)}] >> PDF criado, rodando enviando_midia.py", flush=True)
    subprocess.run(["python", "enviando_midia.py"])
    print(f"[{datetime.now(tz)}] >> Ciclo completo finalizado", flush=True)

def executar_mensagem():
    print(f"[{datetime.now(tz)}] >> Executando mensagem_via_bancodados4.py", flush=True)
    subprocess.run(["python", "mensagem_via_bancodados4.py"])
    print(f"[{datetime.now(tz)}] >> Execução de mensagem_via_bancodados4.py finalizada", flush=True)

# Agenda usando hora local brasileira
schedule.every().monday.at("06:00").do(executar_ciclo)
schedule.every().day.at("10:05").do(executar_mensagem)

print(f"[{datetime.now(tz)}] Agendamentos iniciados:")
print("- Segunda-feira às 06:00 → executar_ciclo()")
print("- Todos os dias às 10:05 → executar_mensagem()")
print("Aguardando execução...", flush=True)

while True:
    # Ajuste: verifica o horário considerando o fuso
    now = datetime.now(tz)
    schedule.run_pending()
    print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] Aguardando próxima execução...", flush=True)
    time.sleep(60)
