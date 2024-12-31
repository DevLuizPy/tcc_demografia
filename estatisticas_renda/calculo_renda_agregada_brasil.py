import pandas as pd

# Dataframe e nome das colunas dos censos
arquivos_censos = {
    "censo_2010.csv": "GEO1_BR2010",
    "censo_2000.csv": "GEO1_BR2000"
}

estatisticas_lista = []

# Calculo para cada censo
for arquivo, coluna_codigo in arquivos_censos.items():
    df_censo = pd.read_csv(arquivo)

    # Excluindo valores inválidos
    df_censo = df_censo[~df_censo['INCTOT'].isin([9999998, 9999999])]

    # Calculo da média e do desvio padrão da renda
    total_peso = df_censo['PERWT'].sum()
    media_renda = (df_censo['INCTOT'] * df_censo['PERWT']).sum() / total_peso
    variancia_ponderada = ((df_censo['INCTOT'] - media_renda) ** 2 * df_censo['PERWT']).sum() / total_peso
    desvio_padrao_renda = variancia_ponderada ** 0.5
    ano_censo = int(arquivo[-8:-4])
    estatisticas_lista.append({
        'Ano do Censo': ano_censo,
        'Média da Renda': media_renda,
        'Desvio Padrão da Renda': desvio_padrao_renda
    })

# Criação do Dataframe com as estatisticas
estatisticas_agregadas = pd.DataFrame(estatisticas_lista)

# Criação do arquivo em xlsx
estatisticas_agregadas.to_excel("estatisticas_renda_agregada_brasil.xlsx", index=False)

print("Cálculo concluído e arquivo salvo como 'estatisticas_renda_agregada_brasil.xlsx'.")
