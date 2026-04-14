import pandas as pd
import numpy as np
import re

# =============================================================================
# ETAPA 1: PREPARAÇÃO DOS DADOS DO NTA (A RÉGUA)
# =============================================================================
print("Carregando arquivo NTA...")
df_nta = pd.read_excel('NTA.xlsx')

df_nta.columns = df_nta.columns.str.strip()
if 'VarName' in df_nta.columns:
    df_nta['VarName'] = df_nta['VarName'].astype(str).str.strip()

df_nta['Year'] = pd.to_numeric(df_nta['Year'], errors='coerce')
anos_nta = [1996, 2002, 2008]
perfis_nta = {}

for ano in anos_nta:
    linha_yl = df_nta[(df_nta['Year'] == ano) & (df_nta['VarName'] == 'YL')]
    linha_c = df_nta[(df_nta['Year'] == ano) & (df_nta['VarName'] == 'C')]

    yl_vetor = linha_yl.loc[:, 'Age0':'Age90'].values[0]
    c_vetor = linha_c.loc[:, 'Age0':'Age90'].values[0]

    perfis_nta[ano] = {'YL': yl_vetor, 'C': c_vetor}
print("Perfis NTA carregados com sucesso!")

# =============================================================================
# ETAPA 2: PROCESSAMENTO DOS CENSOS (1960 a 2010) - IPUMS
# =============================================================================
anos_censos = [1960, 1970, 1980, 1991, 2000, 2010]
arquivos_censos = {ano: f"censo_{ano}.csv" for ano in anos_censos}
resultados_sr = []

print("Processando os Censos (1960-2010)...")
for ano_censo, arquivo in arquivos_censos.items():
    print(f" -> Lendo Censo {ano_censo}...")
    df_censo = pd.read_csv(arquivo)

    df_censo = df_censo[df_censo['AGE'] != 999]
    df_censo['AGE_NTA'] = np.where(df_censo['AGE'] >= 90, 90, df_censo['AGE'])

    pop_por_idade = df_censo.groupby('AGE_NTA')['PERWT'].sum()
    pop_vetor = pop_por_idade.reindex(range(91), fill_value=0).values

    for ano_base_nta in anos_nta:
        L_t = np.sum(pop_vetor * perfis_nta[ano_base_nta]['YL'])
        N_t = np.sum(pop_vetor * perfis_nta[ano_base_nta]['C'])
        SR_t = L_t / N_t
        resultados_sr.append(
            {'Ano_Base_NTA': ano_base_nta, 'Ano_Censo': ano_censo, 'L_t (Produtores)': L_t, 'N_t (Consumidores)': N_t,
             'Razao_Suporte_SR': SR_t})

# =============================================================================
# ETAPA 2.1: INTEGRAÇÃO DO CENSO 2022 (SIDRA - Tabela 9514)
# =============================================================================
print(" -> Bebendo na fonte do Censo 2022 (SIDRA Tabela 9514)...")

# Pula as 7 primeiras linhas e lê apenas as colunas A e B
df_2022 = pd.read_excel('Tabela 9514.xlsx', skiprows=7, usecols="A:B", names=['Idade_str', 'Populacao'])
df_2022 = df_2022.dropna()


def extrair_idade(texto):
    texto = str(texto).lower()
    if 'menos de' in texto:
        return 0
    # Extrai apenas os números da string
    numeros = re.findall(r'\d+', texto)
    if numeros:
        return int(numeros[0])
    return -1  # Retorna -1 para lixos textuais (como a palavra "Total")


df_2022['AGE'] = df_2022['Idade_str'].apply(extrair_idade)
df_2022 = df_2022[df_2022['AGE'] >= 0]  # Remove os lixos filtrados
df_2022['Populacao'] = pd.to_numeric(df_2022['Populacao'], errors='coerce').fillna(0)

# Agrupa nos moldes do NTA (90+)
df_2022['AGE_NTA'] = np.where(df_2022['AGE'] >= 90, 90, df_2022['AGE'])
pop_por_idade_2022 = df_2022.groupby('AGE_NTA')['Populacao'].sum()
pop_vetor_2022 = pop_por_idade_2022.reindex(range(91), fill_value=0).values

# Calcula para 2022
for ano_base_nta in anos_nta:
    L_t = np.sum(pop_vetor_2022 * perfis_nta[ano_base_nta]['YL'])
    N_t = np.sum(pop_vetor_2022 * perfis_nta[ano_base_nta]['C'])
    SR_t = L_t / N_t
    resultados_sr.append(
        {'Ano_Base_NTA': ano_base_nta, 'Ano_Censo': 2022, 'L_t (Produtores)': L_t, 'N_t (Consumidores)': N_t,
         'Razao_Suporte_SR': SR_t})

# =============================================================================
# ETAPA 3: CÁLCULO DO 1º DIVIDENDO DEMOGRÁFICO
# =============================================================================
print("Calculando o Primeiro Dividendo Demográfico Final...")
df_resultados = pd.DataFrame(resultados_sr)
df_resultados = df_resultados.sort_values(by=['Ano_Base_NTA', 'Ano_Censo']).reset_index(drop=True)


def calcular_dividendo(group):
    anos_passados = group['Ano_Censo'].diff()
    group['Dividendo_Anualizado (%)'] = ((group['Razao_Suporte_SR'] / group['Razao_Suporte_SR'].shift(1)) ** (
                1 / anos_passados) - 1) * 100

    anos_str = group['Ano_Censo'].astype(str)
    group['Decada'] = anos_str.shift(1) + "-" + anos_str
    return group


df_final = df_resultados.groupby('Ano_Base_NTA', group_keys=False).apply(calcular_dividendo)
df_final = df_final[
    ['Ano_Base_NTA', 'Decada', 'Ano_Censo', 'L_t (Produtores)', 'N_t (Consumidores)', 'Razao_Suporte_SR',
     'Dividendo_Anualizado (%)']]

nome_arquivo_saida = "resultado_dividendo_brasil_NTA_com_2022.xlsx"
df_final.to_excel(nome_arquivo_saida, index=False)
print(f"Sucesso absoluto! Matriz salva como '{nome_arquivo_saida}'.")
