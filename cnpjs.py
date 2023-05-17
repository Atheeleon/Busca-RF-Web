import csv, os, requests, time
import pandas as pd
from pathlib import Path

clientes = []

def pegaDados(lista):
    global clientes
    completa = ''
    for cnpj in lista:
        completa = ''
        for x in range(14 - len(str(cnpj))):
            completa += '0'
            
        cnpj = completa + str(cnpj)

        url = f"https://minhareceita.org/{cnpj}"

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        cliente = response.json()
        if 'message' in cliente:
            dados = {
                'cnpj': cnpj,
                'razao': 'nao encontrado',
                'nome': '',
                'cidade': '',
                'uf': '',
                'bairro': '',
                'rua': '',
                'numero': '',
                'email': '',
                'telefone 1': '',
                'telefone 2': '',
                'segmento': '',
                'cadastro': '',
                'matriz/filial': '',
            }

            print(f"Fazendo o append de {dados['razao']} - {dados['cnpj']}")
            clientes.append(dados)
            completa = ''
        else:
            dados = {
                'cnpj': cliente['cnpj'],
                'razao': cliente['razao_social'],
                'nome': cliente['nome_fantasia'],
                'cidade': cliente['municipio'],
                'uf': cliente['uf'],
                'bairro': cliente['bairro'],
                'rua': cliente['logradouro'],
                'numero': cliente['numero'],
                'email': cliente['email'],
                'telefone 1': cliente['ddd_telefone_1'],
                'telefone 2': cliente['ddd_telefone_2'],
                'segmento': cliente['cnae_fiscal_descricao'],
                'cadastro': cliente['descricao_situacao_cadastral'],
                'matriz/filial': cliente['descricao_identificador_matriz_filial'],
            }

            print(f"Fazendo o append de {dados['razao']} - {dados['cnpj']}")
            clientes.append(dados)
            completa = ''

def importaBase(diretorio):
    df = pd.read_excel(diretorio)
    values = (df['CNPJ'].values.tolist())
    return values
    
def export(lista, export_directory):
    csv_columns = ['cnpj', 'razao', 'nome', 'cidade', 'uf', 'bairro', 'rua', 'numero', 'email', 'telefone 1',
                   'telefone 2', 'segmento', 'cadastro', 'matriz/filial']
    csv_file = export_directory

    with open(csv_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in lista:
                writer.writerow(data)
                print(f"Export de: {data['cnpj']} - {data['razao']}")
                time.sleep(1)

def rodaProj(import_directory, export_directory):
    pegaDados(importaBase(import_directory))
    export(clientes, export_directory)