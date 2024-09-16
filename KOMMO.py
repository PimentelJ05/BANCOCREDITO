import os
import requests
from tabulate import tabulate
import pandas as pd

# Configurações básicas
BASE_URL = 'https://creditoessencial.kommo.com/api/v4/leads'
TOKEN_URL = 'https://creditoessencial.kommo.com/oauth2/access_token'

# Tokens e credenciais
access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImIyOWM4YTNkNjhhMzQxNTg4YmVhMGIwNmRkZmM0ZGVjNzA5ZTA4NzAwMTBiOTE0YTY4ODE4OGY1ZTAzYzhhZTliZDE0NWEzYWUyNWQ1ZWZkIn0.eyJhdWQiOiIzMWU5ZjgzNy1jOTlhLTQ5YTUtOGFkYS1mNzEwMmJiNmMzYzciLCJqdGkiOiJiMjljOGEzZDY4YTM0MTU4OGJlYTBiMDZkZGZjNGRlYzcwOWUwODcwMDEwYjkxNGE2ODgxODhmNWUwM2M4YWU5YmQxNDVhM2FlMjVkNWVmZCIsImlhdCI6MTcyNjQ5MTIzMSwibmJmIjoxNzI2NDkxMjMxLCJleHAiOjE3MjY1Nzc2MzEsInN1YiI6IjEwNDY2MDM1IiwiZ3JhbnRfdHlwZSI6IiIsImFjY291bnRfaWQiOjMyMDYxNDU1LCJiYXNlX2RvbWFpbiI6ImtvbW1vLmNvbSIsInZlcnNpb24iOjIsInNjb3BlcyI6WyJwdXNoX25vdGlmaWNhdGlvbnMiLCJmaWxlcyIsImNybSIsImZpbGVzX2RlbGV0ZSIsIm5vdGlmaWNhdGlvbnMiXSwiaGFzaF91dWlkIjoiNmZkMmRkMWUtZDUxYS00MzcyLTk3NjYtODRlMzA4YzhmNTBlIiwiYXBpX2RvbWFpbiI6ImFwaS1nLmtvbW1vLmNvbSJ9.HO-qfcgtH5i85f0Z-mlQ--Lj5uuGfNCaD7suoyRg275MRv9XwNNDFXVC_Xj7-UaSQhWT2JLme9sOdofvDTbw2s1BRKu5JyKkjUPKJcMWJnWto-0hKIAPLcKqkN8dFkCmF9gTYpiBjm5RB3lxedJl352r2oJw1L3y_QgX7ezmsFJunwDVMVbwqnbTKvj2lbmocrRKxZJ8jeNa54H9x6tleQ8ztWNAfPmSKJs53iKocDAoQVcDpBsFWHTu6_fygyXVJxroTY_dZ8b37ehRpRXQUSiTFrNZi2h4V8IHuB6Vj1T6Er1aNudFWXlI5iTnu-91_M4wK4pD6eDGR9NqB4M0rA'
refresh_token = 'def50200d7fea6f4f07c6a22983e07d135303765bc4d9df6a41141ce14ae4b7586230763a3c6a77a20861ab16bd4755ec1e0454e01f94f73805edbabb68eb0322cd7494539dbc137be0834457ad5a353d391390cd366d48866293771f4400a70d7c82fc42b85a2df2f783fb689da0e589571fce27e6d88d545697fae23b3c7fc064c0011f13b70aa620bdc542d992eaa184ceebf098db48dbd14bca53f54773298e434a0223211d2317fca6a13c44028cecfb54c8dccdaa00498892a9f8345419d6d146cd894324f8429b3343d1a779e4e0dc3cb7c98146afe8834b34d7a53c31a7c061767860f750691d448d8827f47ed26856ce7586f8a433401f4dc61dfe9c136e66f4e444056d511c67f7f6b28c9ff90e82d1a967b603559c75ac74ae99b781534dad68bbf82406410ba99086242248c8bb3925362971ad8a5cbc61df8547811985a0f5a7bbf73ad01bfb784c641a68e2f9740dcb44a067e12da10c07b4d9db42fcef05d0282199360a7d9e4b48ade71e9b8719af340a8df809e111b243a03e31d124fca2cdd4fbfeba28cb5846a94fe34e0744bd334d057fdf3711dafac270c66385cbe526c7ae337848f7b355aae121867298d2ae825823e5ac64f1b0af1905bfcffc4ee0c6ab27c3e82d2a36704a3d324e41c4a02731f7ec3e6a5467e5df32586a07c575829c40a20c0d1'
client_id = 'a137738a-4c0d-44cd-9c8e-f2c35734c62e'
client_secret = 'f7fojh7YZP7SFaJ9ivd2kZ67wD8JTjw1AFfh0Ozv1FX7lhoZkwFhz3Q6UlTDNgdf'

def renovar_access_token(refresh_token):
    """
    Renova o access token usando o refresh token.
    """
    dados = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'redirect_uri': 'https://creditoessencial.com/oauth/callback'
    }
    response = requests.post(TOKEN_URL, data=dados)

    if response.status_code == 200:
        tokens = response.json()
        return tokens['access_token'], tokens['refresh_token']
    else:
        print(f"Erro ao renovar o token: {response.status_code} - {response.text}")
        return None, None

def contar_leads_por_status(access_token, refresh_token, pipeline_id, status_id):
    """
    Conta os leads para um pipeline e status específicos.
    """
    url = BASE_URL
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    params = {
        'filter[statuses][0][pipeline_id]': pipeline_id,
        'filter[statuses][0][status_id]': status_id,
        'limit': 250
    }

    total_leads = 0
    page = 1

    while True:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            try:
                data = response.json()
                leads = data.get('_embedded', {}).get('leads', [])
                total_leads += len(leads)

                next_page_url = data.get('_links', {}).get('next', {}).get('href')
                if next_page_url:
                    params['page'] = page + 1
                    page += 1
                else:
                    break
            except ValueError:
                print("Erro ao processar a resposta JSON:", response.text)
                break
        elif response.status_code == 401:
            print("Token expirado, tentando renovar...")
            new_access_token, new_refresh_token = renovar_access_token(refresh_token)
            if new_access_token:
                access_token = new_access_token
                headers['Authorization'] = f'Bearer {access_token}'
                refresh_token = new_refresh_token
                continue
            else:
                print("Erro ao renovar o token.")
                break
        elif response.status_code == 204:
            # Captura o erro específico de status 204
            return 0, None  # Tratar como 0 ao invés de erro
        else:
            print(f"Erro ao contar leads para o funil {pipeline_id} e status {status_id}: {response.status_code} - {response.text}")
            return 0, None  # Tratar como 0 ao invés de erro

    return total_leads, None

def obter_contagem_leads_atual_por_funil(access_token, refresh_token, pipeline_ids_with_statuses, pipeline_names):
    """
    Obtém a contagem de leads atual para cada funil e status, incluindo o nome do funil.
    """
    contagem_leads_atual_por_funil = []
    erros = []

    for pipeline_id, statuses in pipeline_ids_with_statuses.items():
        funil_nome = pipeline_names.get(pipeline_id, 'Desconhecido')  # Obter o nome do funil
        for status_id, status_nome in statuses.items():
            total_leads, erro = contar_leads_por_status(access_token, refresh_token, pipeline_id, status_id)
            if erro:
                erros.append({
                    'Funil': funil_nome,
                    'Status': status_nome,
                    'Erro': erro
                })
            else:
                contagem_leads_atual_por_funil.append({
                    'Funil': funil_nome,
                    'Status': status_nome,
                    'Leads': total_leads if total_leads is not None else 0
                })

    return contagem_leads_atual_por_funil, erros

# Mapeamento dos IDs dos funis para seus nomes
pipeline_names = {
    8778991: 'QUALIFICAÇÃO LEAD',
    9547016: 'POS SMART',
    9547000: 'MINIZINHA',
    9447940: 'TAP TO PAY',
    9423092: 'ATIVAÇÃO',
    9493916: 'CLIENTES'
}

# IDs dos funis e status
pipeline_ids_with_statuses = {
    8778991: {68816231: 'FORMS SITE', 68816235: 'coleta de informações', 69202523: 'forms type enviado',
              71785620: 'Negociação', 69202527: 'FORMS TYPE preenchido', 71889068: 'Comprovante de RESIDÊNCIA',
              71019584: 'identidade', 72605264: 'BANCO', 69297283: 'ASSINATURA', 70729739: 'enviado para o service',
              72059336: 'Cadastro OWN', 72059748: 'Maquininha enviada'},
    9547016: {73684280: 'NEGOCIAÇÃO', 73681896: 'TYPEFORM ENVIADO', 73681900: 'TYPEFORM PREENCHIDO',
              73681904: 'ASSINATURA PENDENTE', 73682068: 'ENVIADO SERVICE'},
    9547000: {73684288: 'NEGOCIAÇÃO', 73681812: 'TYPEFORM ENVIADO', 73681816: 'TYPE PREENCHIDO',
              73681820: 'ASSINATURA PENDENTE', 73682088: 'ENVIADO SERVICE'},
    9447940: {73684380: 'NEGOCIAÇÃO', 73052232: 'TYPEFORM ENVIADO', 73052236: 'TYPEFORM PREENCHIDO',
              73052240: 'ASSINATURA PENDENTE', 73682176: 'ENVIADO SERVICE'},
    9423092: {72892352: 'Maquininha enviada', 72895996: 'Maquininha não entregue', 72892356: 'código de rastreio',
              72892360: 'onboarding inicial', 72951124: 'Não testou', 73579648: 'Não transacionaram 1 MÊS',
              73350144: 'Em processo de resolução', 73166604: 'SEM CONTATO', 72892632: 'Testou mas não ativou',
              73347540: 'ACOMPANHAMENTO ATIVAÇÃO', 73348816: 'Trocar chip', 72892652: 'maquininha Com defeito',
              72892648: 'devolução'},
    9493916: {73337976: '<5k', 73336036: '5k', 73336040: '10k', 73336044: '20k+'}
}

# Obter leads atuais para cada funil e status
leads_atual, erros = obter_contagem_leads_atual_por_funil(access_token, refresh_token, pipeline_ids_with_statuses, pipeline_names)

# Converte os resultados em DataFrame
df_leads = pd.DataFrame(leads_atual)

# Exibe o DataFrame de Leads
print("\nTabela de Leads:")
print(df_leads)

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
