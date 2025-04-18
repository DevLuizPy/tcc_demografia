import pandas as pd

# Dicionários de tradução
edattain_labels = {
    1: "Ensino fundamental incompleto",
    2: "Ensino fundamental completo",
    3: "Ensino médio completo",
    4: "Ensino superior completo"
}

sex_labels = {
    1: "Homem",
    2: "Mulher"
}

# Censos e arquivos
anos_censos = [2010, 2000, 1991, 1980, 1970, 1960]
arquivos_censos = {ano: f"censo_{ano}.csv" for ano in anos_censos}

# Lista para armazenar os DataFrames de cada ano
dados_todos_anos = []

for ano, arquivo in arquivos_censos.items():
    df_censo = pd.read_csv(arquivo)

    # Filtrar os dados para pessoas com mais de 25 anos, sexo e educação válidos, e força de trabalho conhecida
    df_filtrado = df_censo[
        (df_censo['AGE'] > 24) &
        (df_censo['SEX'].isin([1, 2])) &
        (df_censo['EDATTAIN'].isin([1, 2, 3, 4])) &
        (df_censo['LABFORCE'].isin([1, 2]))
    ]

    # Na força de trabalho
    dentro = df_filtrado[df_filtrado['LABFORCE'] == 2]
    grupo_dentro = dentro.groupby(['EDATTAIN', 'SEX'])['PERWT'].sum().reset_index()
    grupo_dentro["Situacao"] = "Na força de trabalho"
    grupo_dentro["Nível educacional"] = grupo_dentro["EDATTAIN"].map(edattain_labels)
    grupo_dentro["Sexo"] = grupo_dentro["SEX"].map(sex_labels)
    grupo_dentro = grupo_dentro[["Situacao", "Nível educacional", "Sexo", "PERWT"]]
    grupo_dentro = grupo_dentro.rename(columns={"PERWT": ano})

    # Fora da força de trabalho (sem decomposição)
    total_fora = df_filtrado[df_filtrado["LABFORCE"] == 1]["PERWT"].sum()
    grupo_fora = pd.DataFrame({
        "Situacao": ["Fora da força de trabalho"],
        "Nível educacional": [None],
        "Sexo": [None],
        ano: [total_fora]
    })

    # Concatenar
    df_ano = pd.concat([grupo_dentro, grupo_fora], ignore_index=True)
    dados_todos_anos.append(df_ano)

# Juntar os dados de todos os anos
df_final = dados_todos_anos[0]
for df in dados_todos_anos[1:]:
    df_final = pd.merge(df_final, df, on=["Situacao", "Nível educacional", "Sexo"], how="outer")

# Ordenar colunas
colunas_ordem = ["Situacao", "Nível educacional", "Sexo"] + sorted(arquivos_censos.keys(), reverse=True)
df_final = df_final[colunas_ordem]

# Exportar
df_final.to_excel("forca_trabalho_brasil.xlsx", index=False)
print("Arquivo 'forca_trabalho_brasil.xlsx' criado com sucesso.")
