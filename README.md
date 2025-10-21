# 🕓 Agendamento de Scripts Python
Agendamento de Scripts com Scheduler e Dockerfile

Este projeto automatiza a execução de scripts Python em horários específicos utilizando a biblioteca [`schedule`](https://pypi.org/project/schedule/).
Neste projeto foram utilizado 4 arquivos
O código foi configurado para:

No exemplo ele executa os 2 scripts o `chamado_abertos.py` e `mensagem_via_bancodados4.py` mas por motivos de segurança não disponibilizei também esses arquivos, mas
a idéia é demosntrar a execução chamando arquivos a partir de um arquivo principal.

- Executar os scripts `chamado_abertos.py` e `enviando_midia.py` **toda segunda-feira às 06:00**.
- Executar o script `mensagem_via_bancodados4.py` **todos os dias às 10:30**.

Além disso, o sistema foi ajustado para utilizar o fuso horário do Brasil (`America/Sao_Paulo`), garantindo que o agendamento ocorra no horário correto mesmo em servidores com timezone UTC.

---

## 🚀 Funcionalidades

- **Agendamento automático de tarefas** com base em horários fixos.
- **Execução sequencial** dos scripts com verificação de sucesso.
- **Logs com data e hora** para acompanhamento da execução.
- **Controle de fuso horário** via `pytz`.
- **Verificação de geração de arquivo PDF** antes de executar o próximo script.

---

## 📂 Estrutura dos Arquivos

```bash
your_project/
└── Automacao/
    ├── requirements.txt
    ├── Dockerfile
    ├── chamado_abertos.py
    ├── enviando_midia.py
    ├── mensagem_via_bancodados.py
    └── scheduler_main.py

---

## 🧩 Código Principal (`scheduler_main.py`)

```python
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

schedule.every().monday.at("06:00").do(executar_ciclo)
schedule.every().day.at("10:30").do(executar_mensagem)

print(f"[{datetime.now(tz)}] Agendamentos iniciados:")
print("- Segunda-feira às 06:00 → executar_ciclo()")
print("- Todos os dias às 10:30 → executar_mensagem()")
print("Aguardando execução...", flush=True)

while True:
    now = datetime.now(tz)
    schedule.run_pending()
    print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] Aguardando próxima execução...", flush=True)
    time.sleep(30)
```


# 🕐 Configurando o Fuso Horário

Se o ambiente (servidor, container Docker, etc.) estiver configurado com o fuso UTC, o agendamento pode não rodar no horário esperado.
Para garantir o fuso correto:

- **Adicione no arquivo Dockerfile, no nosso exemplo utilizando o fuso horário brasileiro.:
  
  ```export TZ="America/Sao_Paulo"```  

