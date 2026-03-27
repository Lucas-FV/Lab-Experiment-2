import urllib.request
import urllib.error
import json
import csv
import time

# Configurações da API
TOKEN = '' 
HEADERS = {
    'Authorization': f'token {TOKEN}',
    'Accept': 'application/vnd.github.v3+json',
    'User-Agent': 'Python-urllib' # O GitHub exige um User-Agent
}
BASE_URL = 'https://api.github.com/search/repositories'

def get_top_java_repos():
    repos_data = []
    
    for page in range(1, 11):
        # Montando a URL com os parâmetros
        url = f"{BASE_URL}?q=language:java&sort=stars&order=desc&per_page=100&page={page}"
        
        print(f"Buscando página {page} de 10...")
        
        # Criando a requisição com os headers
        req = urllib.request.Request(url, headers=HEADERS)
        
        try:
            with urllib.request.urlopen(req) as response:
                # Lendo e convertendo a resposta de JSON para dicionário Python
                data = json.loads(response.read().decode('utf-8'))
                items = data.get('items', [])
                
                for repo in items:
                    repos_data.append({
                        'name': repo['name'],
                        'full_name': repo['full_name'],
                        'html_url': repo['html_url'],
                        'clone_url': repo['clone_url'],
                        'stars': repo['stargazers_count'],
                        'created_at': repo['created_at'],
                        'size_kb': repo['size']
                    })
        except urllib.error.HTTPError as e:
            print(f"Erro na requisição: {e.code} - {e.reason}")
            # Lê o corpo do erro se houver
            erro_body = e.read().decode('utf-8')
            print(erro_body)
            break
            
        # Pausa de 2 segundos para respeitar o limite da API
        time.sleep(10)
        
    return repos_data

def save_to_csv(repos, filename="top_1000_java_repos.csv"):
    if not repos:
        print("Nenhum dado para salvar.")
        return
        
    keys = repos[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(repos)
    print(f"\nSucesso! Arquivo '{filename}' gerado com {len(repos)} repositórios.")

if __name__ == "__main__":
    print("Iniciando a mineração dos repositórios Java...")
    java_repos = get_top_java_repos()
    save_to_csv(java_repos)