from flask import Flask, render_template, request, send_file
import csv, os, requests, time, datetime
import pandas as pd

clientes = []

def importaBase(diretorio, formato):
    if formato.upper() == '.XLSX' | '.XLS':
        df = pd.read_excel(diretorio)
        values = (df['CNPJ'].values.tolist())
        return values
    elif formato.upper() == '.CSV' | '.TXT':
        df = pd.read_csv(diretorio)
        values = (df['CNPJ'].values.tolist())
        return values
    else:
        print('Opção inválida')
        
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

def rodaProj(import_directory, export_directory, formato):
    pegaDados(importaBase(import_directory, formato))
    export(clientes, export_directory)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    file_path = ''
    export_path = ''
    if datetime.datetime.now().minute in (0, 15, 30, 45):
        for file_name in os.listdir(os.path.join(app.root_path, 'uploads')):
            os.remove(os.path.join(os.path.join(app.root_path, 'uploads'), file_name))
    
    if request.method == 'POST':
        current_time = f'{datetime.datetime.now().hour}{datetime.datetime.now().minute}{datetime.datetime.now().second}'
        file = request.files['import']
        file_path = os.path.join(app.root_path, 
                                 'uploads', 
                                 f'{current_time}-{file.filename}') #rodaProj(file_path, export_directory)
        export_path = os.path.join(app.root_path, 
                                   'uploads', 
                                   f'processado_{current_time}-{os.path.splitext(file.filename)[0]}.csv') #rodaProj(file_path, export_path)
        file.save(file_path)
        rodaProj(file_path, export_path, os.path.splitext(file.filename)[1])
        return send_file(export_path, as_attachment=True)

if __name__ == '__main__':
    app.run()