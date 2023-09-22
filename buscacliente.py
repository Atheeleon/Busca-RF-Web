import csv, requests, openpyxl
from flask import request, send_file
import os, datetime


def pegaDados(cnpj):
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
        return dados
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
        return dados

def export(app):
        current_time = f'{datetime.datetime.now().hour}{datetime.datetime.now().minute}{datetime.datetime.now().second}'
        file = request.files['import']
        file_path = os.path.join(app.root_path, 
                                 'uploads', 
                                 f'{current_time}-{file.filename}')
        export_path = os.path.join(app.root_path, 
                                   'uploads', 
                                   f'processado_{current_time}-{os.path.splitext(file.filename)[0]}.xlsx')
        file.save(file_path)
        return send_file(export_path, as_attachment=True)