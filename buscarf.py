import requests
import pandas as pd

importado, processado = [], []

def importar(diretorio, formato):
    match formato.upper():
        case '.XLSX' | '.XLS':
            try:
                df = pd.read_excel(diretorio)
                importado.append(df['CNPJ'].values.tolist())
                print('Base importada com sucesso!')
            except KeyError:
                print('Coluna inexistente')
        case '.CSV' | '.TXT':
            try:
                df = pd.read_csv(diretorio)
                importado.append(df['CNPJ'].values.tolist())
                print('Base importada com sucesso!')
            except KeyError:
                print('Coluna inexistente')
        case _:
            print('Arquivo não suportado. Por favor, utilize arquivos nos formatos .XLSX, .XLS, .CSV ou .TXT')
        
def buscar():
    
    print('\n##### INICIANDO BUSCA DE DADOS #####\n')
       
    for cnpj in importado[0]:
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
                'natureza juridica' : ''
            }
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
                'natureza juridica': cliente['natureza_juridica']
            }

        print(f"Armazenando dados de {dados['razao']} - {dados['cnpj']}")
        processado.append(dados)
        completa = ''

    print('\n##### FIM DA BUSCA DE DADOS #####\n')        

def processar():
    try:
        df = pd.DataFrame(processado)
        print('Dados armazenados com sucesso!')
        return df
    except Exception as e:
        print(f'Erro ao armazenar dados: {e}')
        return pd.DataFrame()

def exportar(diretorio, formato):
    importar(diretorio, formato)
    buscar()
    return processar()