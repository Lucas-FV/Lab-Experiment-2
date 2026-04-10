import pandas as pd
df = pd.read_csv('resultados_finais_sprint2.csv')

# O comando describe() já calcula a contagem, média, desvio padrão e mediana (50%) de uma vez só!
print(df[['cbo_median', 'lcom_median', 'dit_median']].describe())