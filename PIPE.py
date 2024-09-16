import os
import requests
from tabulate import tabulate
import pandas as pd

# Configurações básicas
base_url = 'https://api.pipedrive.com/v1'
api_token = 'a816c8b037aaf077699b11b603757363e2b58ed9'

def display_table(title, data):
    # Exibe os dados no formato de tabela usando tabulate
    print(f"\n{'=' * 50}")
    print(f"{title:^50}")
    print(f"{'=' * 50}")
    print(tabulate(data, headers="keys", tablefmt="grid"))
    print("\n")

def get_deal_count(stage_id, stage_name):
    # Função para obter a contagem de negócios de um estágio específico
    deals_url = f'{base_url}/deals'
    params = {'api_token': api_token, 'stage_id': stage_id, 'status': 'open', 'limit': 100}  # Filtra negócios abertos
    response = requests.get(deals_url, params=params)
    
    if response.status_code == 200:
        deals = response.json().get('data')
        if deals is not None:
            deal_count = len(deals)
            return {"Stage": stage_name, "ID": stage_id, "Open Deals": deal_count}
        else:
            return {"Stage": stage_name, "ID": stage_id, "Open Deals": 0}
    else:
        print(f"Erro ao obter negócios para o estágio {stage_id}: {response.status_code} - {response.text}")
        return {"Stage": stage_name, "ID": stage_id, "Open Deals": "Error"}

# Lista de estágios
stages = [
    {'id': 6, 'name': 'Typeform Preenchido'}, {'id': 3, 'name': 'Assinatura'}, {'id': 1, 'name': 'ID/CPF'}, 
    {'id': 31, 'name': 'Comprovante'}, {'id': 2, 'name': 'Banco'}, {'id': 4, 'name': 'Enviado para o service'},
    {'id': 7, 'name': 'Validação'}, {'id': 8, 'name': 'Cadastro OWN'}, {'id': 10, 'name': 'Disponível para Vínculo'}, 
    {'id': 11, 'name': 'Vinculação'}, {'id': 9, 'name': 'Devolução'}, {'id': 12, 'name': 'BLACKLIST'},
    {'id': 27, 'name': 'ID/CPF'}, {'id': 28, 'name': 'Comprovante Residência'}, {'id': 29, 'name': 'Banco'}, 
    {'id': 30, 'name': 'Validado'}, {'id': 13, 'name': 'Vinculado'}, {'id': 14, 'name': 'Configurar Maquininha'}, 
    {'id': 18, 'name': 'Preparação'}, {'id': 16, 'name': 'Melhor Envio'}, {'id': 17, 'name': 'Enviada'},
    {'id': 19, 'name': 'Maquininha Enviada'}, {'id': 20, 'name': 'Código de Rastreio'}, 
    {'id': 21, 'name': 'Onboarding Inicial'}, {'id': 22, 'name': 'Ativado'}, 
    {'id': 24, 'name': 'Não transacionou'}, {'id': 23, 'name': '5k'}, {'id': 25, 'name': '10k'}, {'id': 26, 'name': '20k+'}
]

# Coleta os resultados
results = [get_deal_count(stage['id'], stage['name']) for stage in stages]

# Exibe a tabela formatada
display_table("Negócios Abertos por Estágio", results)

# Converte os resultados em DataFrame
df_results = pd.DataFrame(results)

# Exibe o DataFrame
print(df_results)

# Verifica se está rodando em um ambiente com display gráfico
if os.getenv('DISPLAY'):
    import tkinter as tk
    
    # Código para exibir janela Tkinter com notificação
    def on_close():
        print("A janela foi fechada.")
        root.destroy()  # Fecha a janela

    # Configuração da janela
    root = tk.Tk()
    root.title("Notificação de Execução")
    label = tk.Label(root, text="O script foi executado. Feche esta janela quando terminar.")
    label.pack(padx=20, pady=20)

    # Configuração do botão de fechar
    root.protocol("WM_DELETE_WINDOW", on_close)

    # Executa a janela
    root.mainloop()
else:
    print("Ambiente headless detectado, Tkinter desativado.")
