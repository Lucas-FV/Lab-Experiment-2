import csv
import subprocess
import os

# Configurações iniciais
ARQUIVO_CSV_REPOSITORIOS = 'top_1000_java_repos.csv'
CAMINHO_CK_JAR = 'ck/target/ck.jar'
PASTA_DESTINO_CLONE = 'repositorio_teste_s01'

def obter_primeiro_repositorio(csv_file):
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return next(reader) # Pega apenas a primeira linha de dados

def clonar_repositorio(clone_url, destino):
    print(f"Clonando {clone_url} para a pasta '{destino}'...")
    subprocess.run(['git', 'clone', clone_url, destino], check=True)
    print("Clone finalizado com sucesso!")

def executar_ck(pasta_alvo):
    print("\nExecutando a ferramenta CK...")
    
    # Cria uma pasta para não bagunçar a raiz do seu projeto
    pasta_saida_csv = "resultados_sprint_1"
    if not os.path.exists(pasta_saida_csv):
        os.makedirs(pasta_saida_csv)
        
    # Comando otimizado: java -jar ck.jar <dir> <use_jars> <max_files> <variables> <output_dir>
    comando = [
        'java', '-jar', CAMINHO_CK_JAR,
        pasta_alvo,
        'false', # Ignora arquivos .jar externos
        '0',     # Controle automático de partições
        'false', # Ignora métricas de variáveis (foca só nas classes/métodos)
        os.path.abspath(pasta_saida_csv) + '/'
    ]
    
    try:
        subprocess.run(comando, check=True)
        print(f"\nAnálise do CK concluída! Arquivos salvos na pasta: {pasta_saida_csv}")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o CK: {e}")

if __name__ == '__main__':
    print("--- Iniciando Automação da Sprint 1 ---")
    
    # 1. Lê o primeiro repo
    primeiro_repo = obter_primeiro_repositorio(ARQUIVO_CSV_REPOSITORIOS)
    url_para_clonar = primeiro_repo['clone_url']
    nome_repo = primeiro_repo['name']
    
    print(f"Repositório selecionado: {nome_repo}")
    
    # 2. Clona (se já não existir)
    if not os.path.exists(PASTA_DESTINO_CLONE):
        clonar_repositorio(url_para_clonar, PASTA_DESTINO_CLONE)
    else:
        print(f"A pasta '{PASTA_DESTINO_CLONE}' já existe. Pulando etapa de clone.")
        
    # 3. Executa o CK
    executar_ck(PASTA_DESTINO_CLONE)