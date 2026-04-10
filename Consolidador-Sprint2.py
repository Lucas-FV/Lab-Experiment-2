import os
import pandas as pd
import csv

# Configurações
PASTA_BRUTOS = 'Resultados_CK_Brutos'
CSV_GITHUB = 'top_1000_java_repos_atualizado.csv' # Lendo o arquivo atualizado com os releases
CSV_FINAL = 'resultados_finais_sprint2.csv'

def consolidar_dados():
    repos_github = []
    
    print("Lendo os dados atualizados do GitHub...")
    try:
        with open(CSV_GITHUB, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                repos_github.append(row)
    except FileNotFoundError:
         print(f"Erro: Arquivo '{CSV_GITHUB}' não encontrado. Rode o AtualizarReleases.py primeiro.")
         return

    colunas_finais = ('name', 'stars', 'age_days', 'releases', 'size', 'cbo_median', 'dit_median', 'lcom_median', 'loc_total')

    with open(CSV_FINAL, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=colunas_finais)
        writer.writeheader()

        repos_processados = 0

        print("Calculando medianas e consolidando os dados...")
        for index, repo in enumerate(repos_github, 1):
            nome_repo_limpo = repo.get('name', '').replace('/', '-')
            nome_arquivo_ck = f"{index}_{nome_repo_limpo}_class.csv"
            caminho_arquivo_ck = os.path.join(PASTA_BRUTOS, nome_arquivo_ck)

            if os.path.exists(caminho_arquivo_ck):
                try:
                    df = pd.read_csv(caminho_arquivo_ck)
                    if not df.empty:
                        cbo_med = df.get('cbo').median() if 'cbo' in df.columns else 0
                        dit_med = df.get('dit').median() if 'dit' in df.columns else 0
                        lcom_med = df.get('lcom').median() if 'lcom' in df.columns else 0
                        loc_tot = df.get('loc').sum() if 'loc' in df.columns else 0

                        cbo_med = 0 if pd.isna(cbo_med) else cbo_med
                        dit_med = 0 if pd.isna(dit_med) else dit_med
                        lcom_med = 0 if pd.isna(lcom_med) else lcom_med
                        loc_tot = 0 if pd.isna(loc_tot) else loc_tot

                        try:
                            dt_criacao = pd.to_datetime(repo.get('created_at')).tz_localize(None)
                            dt_hoje = pd.Timestamp.now().tz_localize(None)
                            age_days = (dt_hoje - dt_criacao).days
                        except Exception:
                            age_days = 0 

                        linha = {
                            'name': repo.get('name'),
                            'stars': repo.get('stars', 0),
                            'age_days': age_days,
                            'releases': repo.get('releases', 0), # Agora puxa o valor real
                            'size': repo.get('size_kb', 0),
                            'cbo_median': round(cbo_med, 2), 
                            'dit_median': round(dit_med, 2),
                            'lcom_median': round(lcom_med, 2),
                            'loc_total': loc_tot
                        }
                        writer.writerow(linha)
                        repos_processados += 1
                        
                except Exception as e:
                    print(f"  -> Erro ao ler {nome_arquivo_ck}: {e}")

    print(f"\nSucesso absoluto! {repos_processados} repositórios foram consolidados.")
    print(f"Você pode ver o resultado final no arquivo: {CSV_FINAL}")

if __name__ == '__main__':
    consolidar_dados()