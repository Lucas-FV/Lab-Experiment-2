import urllib.request
import urllib.error
import json
import csv
import time
import re

# Configurações da API
TOKEN = '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' 
HEADERS = {
    'Authorization': f'token {TOKEN}',
    'Accept': 'application/vnd.github.v3+json',
    'User-Agent': 'Python-urllib'
}

CSV_ENTRADA = 'top_1000_java_repos.csv'
CSV_SAIDA = 'top_1000_java_repos_atualizado.csv'

def get_release_count(full_name):
    """Pede ao GitHub apenas 1 release por página e lê o cabeçalho para descobrir a última página (total)"""
    url = f"https://api.github.com/repos/{full_name}/releases?per_page=1"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req) as response:
            link_header = response.getheader('Link')
            if link_header:
                match = re.search(r'page=(\d+)>; rel="last"', link_header)
                if match:
                    return int(match.group(1))
            data = json.loads(response.read().decode('utf-8'))
            return len(data)
    except Exception:
        return 0

def atualizar_csv():
    print("Lendo o arquivo original...")
    try:
        with open(CSV_ENTRADA, 'r', encoding='utf-8') as f_in:
            reader = list(csv.DictReader(f_in))
    except FileNotFoundError:
        print(f"Erro: Arquivo '{CSV_ENTRADA}' não encontrado na pasta.")
        return
    
    fieldnames = list(reader[0].keys())
    if 'releases' not in fieldnames:
        fieldnames.append('releases')

    print(f"Buscando a quantidade de releases para {len(reader)} repositórios...")
    print("Isso deve levar cerca de 10 a 15 minutos (respeitando o limite do GitHub).")
    
    with open(CSV_SAIDA, 'w', newline='', encoding='utf-8') as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        
        for index, row in enumerate(reader, 1):
            full_name = row['full_name']
            print(f"[{index}/{len(reader)}] Checando {full_name}...")
            row['releases'] = get_release_count(full_name)
            writer.writerow(row)
            time.sleep(0.7)

if __name__ == '__main__':
    atualizar_csv()
    print(f"\nConcluído! Arquivo salvo como: {CSV_SAIDA}")