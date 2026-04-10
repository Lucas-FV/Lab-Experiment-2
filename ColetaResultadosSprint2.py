import csv
import subprocess
import os
import shutil
import stat

# Configurações
ARQUIVO_CSV_ENTRADA = 'top_1000_java_repos.csv'
CAMINHO_CK_JAR = 'ck.jar'
PASTA_RESULTADOS_BRUTOS = 'Resultados_CK_Brutos'

# Cria a pasta final onde os arquivos CSV brutos ficarão salvos
os.makedirs(PASTA_RESULTADOS_BRUTOS, exist_ok=True)

def forcar_exclusao(func, path, _):
    """Força a exclusão de arquivos protegidos (Apenas Leitura) pelo Git no Windows."""
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception:
        pass

def limpar_pastas(pasta_clone, pasta_ck):
    """Tenta apagar as pastas de forma segura."""
    for pasta in (pasta_clone, pasta_ck):
        if os.path.exists(pasta):
            shutil.rmtree(pasta, onerror=forcar_exclusao)

def iniciar_coleta():
    with open(ARQUIVO_CSV_ENTRADA, mode='r', encoding='utf-8') as f_in:
        reader = csv.DictReader(f_in)
        
        for index, repo in enumerate(reader, 1):
            nome_repo = repo.get('name', f'Repo_{index}').replace('/', '-')
            print(f"\n Processando ({index}/1000): {nome_repo}...")
            
            pasta_clone = f'Repo-Testados/repo_{index}'
            pasta_ck = f'Repo-Testados/ck_{index}'
            
            limpar_pastas(pasta_clone, pasta_ck)
            
            try:
                # 1. Clona o repositório 
                try:
                    url_clone = repo.get('clone_url', '')
                    comando_clone = ('git', 'clone', '-c', 'core.longpaths=true', '--depth', '1', url_clone, pasta_clone)
                    subprocess.run(comando_clone, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                except subprocess.CalledProcessError:
                    print(f"  -> Erro ao clonar {nome_repo}. Pulando...")
                    continue
                
                # 2. Executa o CK
                os.makedirs(pasta_ck, exist_ok=True)
                caminho_absoluto = os.path.abspath(pasta_ck) + '/'
                comando_ck = ('java', '-Xmx2g', '-jar', CAMINHO_CK_JAR, pasta_clone, 'false', '0', 'false', caminho_absoluto)
                
                try:
                    subprocess.run(comando_ck, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                except subprocess.CalledProcessError:
                    print(f"  -> Erro na execução do CK. Pulando...")
                    continue
                    
                # 3. Extrai apenas o class.csv e joga na pasta final
                arquivo_class_gerado = os.path.join(pasta_ck, 'class.csv')
                
                if os.path.exists(arquivo_class_gerado):
                    if os.path.getsize(arquivo_class_gerado) > 200: 
                        nome_arquivo_final = f"{index}_{nome_repo}_class.csv"
                        caminho_final = os.path.join(PASTA_RESULTADOS_BRUTOS, nome_arquivo_final)
                        
                        shutil.copy2(arquivo_class_gerado, caminho_final)
                        print(f"  -> Sucesso! {nome_arquivo_final} salvo na pasta de resultados.")
                    else:
                        print(f"  -> Repositório sem classes Java válidas. Pulando...")
                else:
                    print(f"  -> CK não gerou resultados. Pulando...")
            
            finally:
                # 4. Apaga as pastas: O 'finally' garante que isso vai rodar MESMO se houver um 'continue' lá em cima
                limpar_pastas(pasta_clone, pasta_ck)

if __name__ == '__main__':
    print("Iniciando Extração Bruta da Sprint 2...")
    iniciar_coleta()
    print(f"\nColeta finalizada! Verifique a pasta '{PASTA_RESULTADOS_BRUTOS}'.")