import pandas as pd

# Criando dataFrame para os censos
anos_censos = [2010, 2000, 1991, 1980, 1970, 1960]
arquivos_censos = {ano: f"censo_{ano}.csv" for ano in anos_censos}

# Estruturando o DataFrame para armazenar as contagens de EDATTAIN (educação) separadas por sexo para cada censo
indices = pd.MultiIndex.from_product([[1, 2, 3, 4], [1, 2]],
                                     names=["EDATTAIN", "SEX"])
contagem_edattain_por_censo = pd.DataFrame(index=indices, columns=anos_censos)

# DataFrame separado para o total de homens e mulheres com mais de 25 anos
total_homens_mulheres = pd.DataFrame(columns=['Homens', 'Mulheres'], index=anos_censos)

# Calculo para cada censo
for ano, arquivo in arquivos_censos.items():
    df_censo = pd.read_csv(arquivo)

    # Filtrar os dados para excluir valores inconsistentes e considerar apenas pessoas com mais de 25 anos
    df_brasil_censo = df_censo[
        (df_censo['SEX'] != 9) &
        (df_censo['EDATTAIN'] != 9) &
        (df_censo['AGE'] > 24)
    ]

    contagem_edattain_sexo = df_brasil_censo.groupby(['EDATTAIN', 'SEX'])['PERWT'].sum()
    contagem_edattain_por_censo[ano] = contagem_edattain_sexo.reindex(indices).fillna(0)
    total_homens = df_brasil_censo[df_brasil_censo['SEX'] == 1]['PERWT'].sum()
    total_mulheres = df_brasil_censo[df_brasil_censo['SEX'] == 2]['PERWT'].sum()
    total_homens_mulheres.loc[ano] = [total_homens, total_mulheres]

# Criação do arquivo
with pd.ExcelWriter("estatistica_populacional_brasil.xlsx") as writer:
    contagem_edattain_por_censo.to_excel(writer, sheet_name="Contagem_EDATTAIN_SEX")
    total_homens_mulheres.to_excel(writer, sheet_name="Total_Homens_Mulheres")

print("Arquivo 'estatistica_populacional_brasil.xlsx' criado com sucesso.")
