import pandas as pd

# Dataframe e nome das colunas dos censos
arquivos_censos = {
    "censo_2010.csv": "GEO2_BR2010",
    "censo_2000.csv": "GEO2_BR2000"
}

# Dataframe da tabela dos municipios
df_municipios = pd.read_excel("tabela_municipios.xlsx")
estatisticas_lista = []

# Calculo para cada censo
for arquivo, coluna_codigo in arquivos_censos.items():
    df_censo = pd.read_csv(arquivo)

    # Mapear os códigos para o ano do censo
    ano_censo = int(arquivo[-8:-4])
    codigos_municipios = df_municipios[f'codigo_{ano_censo}'].dropna().astype(int).unique()

    # Filtro para os municípios da rmrj
    df_censo = df_censo[df_censo[coluna_codigo].isin(codigos_municipios)]

    # Excluir valores inválidos
    df_censo = df_censo[~df_censo['INCTOT'].isin([9999998, 9999999])]

    # Calculo da média e o desvio padrão da renda
    total_peso = df_censo['PERWT'].sum()
    media_renda = (df_censo['INCTOT'] * df_censo['PERWT']).sum() / total_peso
    variancia_ponderada = ((df_censo['INCTOT'] - media_renda) ** 2 * df_censo['PERWT']).sum() / total_peso
    desvio_padrao_renda = variancia_ponderada ** 0.5
    estatisticas_lista.append({
        'Ano do Censo': ano_censo,
        'Média da Renda': media_renda,
        'Desvio Padrão da Renda': desvio_padrao_renda
    })

# Criação do Dataframe com as estatisticas
estatisticas_agregadas = pd.DataFrame(estatisticas_lista)

# Salvar o resultado em um novo arquivo Excel
estatisticas_agregadas.to_excel("estatisticas_renda_agregada_rmrj.xlsx", index=False)

print("Cálculo concluído e arquivo salvo como 'estatisticas_renda_agregada_rmrj.xlsx'.")
