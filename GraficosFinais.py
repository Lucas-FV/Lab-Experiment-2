import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def gerar_graficos():
    sns.set_theme(style="whitegrid")

    print("Lendo o arquivo consolidado...")
    try:
        df = pd.read_csv('resultados_finais_sprint2.csv')
    except FileNotFoundError:
        print("Erro: Arquivo 'resultados_finais_sprint2.csv' não encontrado.")
        return

    metricas_qualidade = ['cbo_median', 'dit_median', 'lcom_median']

    rq_mapeamento = {
        'RQ01 - Popularidade (Estrelas)': 'stars',
        'RQ02 - Maturidade (Idade em Dias)': 'age_days',
        'RQ03 - Atividade (Releases)': 'releases',
        'RQ04 - Tamanho (Linhas de Código)': 'loc_total' 
    }

    print("Gerando gráficos...")

    for titulo_rq, coluna_x in rq_mapeamento.items():
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
        fig.suptitle(f'{titulo_rq} vs Qualidade de Código (CK)', fontsize=16, fontweight='bold')

        for i, metrica_y in enumerate(metricas_qualidade):
            sns.scatterplot(data=df, x=coluna_x, y=metrica_y, ax=axes[i], alpha=0.5, color='royalblue')
            
            axes[i].set_title(f'{coluna_x} vs {metrica_y}', fontsize=12)
            axes[i].set_xlabel(coluna_x.upper(), fontsize=10)
            axes[i].set_ylabel(metrica_y.upper(), fontsize=10)

        plt.tight_layout()
        nome_arquivo = f"Grafico_{coluna_x}.jpg" # Já ajustado para salvar como JPG
        plt.savefig(nome_arquivo, dpi=300) 
        print(f" -> Sucesso! Imagem salva: {nome_arquivo}")
        
        plt.close()

    print("\nVisualização concluída! Pode abrir as imagens na sua pasta.")

if __name__ == '__main__':
    gerar_graficos()