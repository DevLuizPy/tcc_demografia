import pandas as pd

# Censos de 2010 a 1960
anos_censos = [2010, 2000, 1991, 1980, 1970, 1960]
arquivos_censos = {ano: f"censo_{ano}.csv" for ano in anos_censos}

# Listas de idades para as categorias dependentes, e a remoção das idades inválidas
idade_dependente_crianca = [1, 2, 3]
idade_dependente_idoso = [21, 22, 23, 24, 25]
idades_invalidas = [5, 6, 7, 8, 9, 10, 11, 98]

# DataFrame para armazenar a razão de suporte para o estado do Rio de Janeiro
df_razao_suporte_rj = pd.DataFrame(columns=['Ano', 'Razão de Suporte'])

# Calcular a razão de suporte para o estado do Rio de Janeiro em cada censo
for ano, arquivo in arquivos_censos.items():
    df_censo = pd.read_csv(arquivo)

    # Filtrar os dados para o estado do Rio de Janeiro (código 33)
    df_rj = df_censo[df_censo[f'GEO1_BR{ano}'] == 33]

    # Eliminar idades inconsistentes
    df_rj = df_rj[~df_rj['AGE2'].isin(idades_invalidas)]

    # Calcular as somas ponderadas para cada faixa etária
    soma_crianca = df_rj[df_rj['AGE2'].isin(idade_dependente_crianca)]['PERWT'].sum()
    soma_idoso = df_rj[df_rj['AGE2'].isin(idade_dependente_idoso)]['PERWT'].sum()
    soma_total = df_rj['PERWT'].sum()

    # Cálculo da idade produtiva (total - dependentes) e da razão de suporte
    idade_produtiva = soma_total - (soma_crianca + soma_idoso)
    razao_de_suporte = idade_produtiva / (soma_crianca + soma_idoso)
    df_razao_suporte_rj = pd.concat([df_razao_suporte_rj, pd.DataFrame({'Ano': [ano], 'Razão de Suporte': [razao_de_suporte]})])

# Salvar o resultado final como um arquivo Excel
df_razao_suporte_rj.to_excel("razao_suporte_rj.xlsx", index=False)

print("Cálculo concluído e arquivo salvo como 'razao_suporte_rj.xlsx'.")
