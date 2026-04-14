import pandas as pd
import numpy as np

# =============================================================================
# ETAPA 1: CARREGAR OS TRABALHADORES EFETIVOS L(t)
# =============================================================================
print("Carregando L(t) dos resultados anteriores...")
# Lê o arquivo que o seu código anterior já processou e salvou
df_l = pd.read_excel("resultado_dividendo_brasil_NTA_com_2022.xlsx")

# Filtrar apenas para o peso de 2008 e os anos que nos interessam (2000, 2010, 2022)
df_l_2008 = df_l[(df_l['Ano_Base_NTA'] == 2008) & (df_l['Ano_Censo'].isin([2000, 2010, 2022]))].copy()

# Criar um dicionário para busca rápida: {Ano: Valor do L(t)}
dict_L = dict(zip(df_l_2008['Ano_Censo'], df_l_2008['L_t (Produtores)']))

# =============================================================================
# ETAPA 2: CARREGAR O PIB Y(t) DO FRED
# =============================================================================
print("Carregando Y(t) da Base_FRED_PIB...")
# Lendo a planilha (header=0 significa que a linha 1 é o cabeçalho)
df_pib = pd.read_excel("Base_FRED_PIB.xlsx", sheet_name="Annual", header=0)

# O FRED geralmente vem com duas colunas, renomeamos para Data e PIB
df_pib.columns = ['Data', 'PIB']

# Converter para datetime e extrair apenas o Ano
df_pib['Data'] = pd.to_datetime(df_pib['Data'])
df_pib['Ano'] = df_pib['Data'].dt.year

# Filtrar apenas os anos 2000, 2010 e 2022
df_pib = df_pib[df_pib['Ano'].isin([2000, 2010, 2022])].copy()

# Criar dicionário: {Ano: Valor do PIB}
dict_Y = dict(zip(df_pib['Ano'], df_pib['PIB']))

# =============================================================================
# ETAPA 3: CÁLCULO DA PRODUTIVIDADE E TAXAS ANUALIZADAS
# =============================================================================
print("\n=== RESULTADOS: PRODUTIVIDADE DO TRABALHO EFETIVO (Y/L) ===")

def calc_crescimento(y_final, y_inicial, anos):
    return ((y_final / y_inicial) ** (1 / anos) - 1) * 100

# Fazendo a divisão Y(t) / L(t) para cada ano
yl_2000 = dict_Y[2000] / dict_L[2000]
yl_2010 = dict_Y[2010] / dict_L[2010]
yl_2022 = dict_Y[2022] / dict_L[2022]

print(f"2000: Y/L = {yl_2000:,.4f}")
print(f"2010: Y/L = {yl_2010:,.4f}")
print(f"2022: Y/L = {yl_2022:,.4f}")

# Calculando as taxas anualizadas de crescimento da produtividade
taxa_2000_2010 = calc_crescimento(yl_2010, yl_2000, 10)
taxa_2010_2022 = calc_crescimento(yl_2022, yl_2010, 12)

print("\n--- Taxas de Crescimento Anualizadas ---")
print(f"2000-2010: {taxa_2000_2010:.2f}% ao ano")
print(f"2010-2022: {taxa_2010_2022:.2f}% ao ano")

# =============================================================================
# ETAPA 4: SALVAR OS RESULTADOS PARA O TCC
# =============================================================================
df_resumo = pd.DataFrame({
    'Período': ['2000-2010', '2010-2022'],
    'Crescimento Y/L (% a.a.)': [taxa_2000_2010, taxa_2010_2022]
})

nome_arquivo = 'Resultado_Y_L_Produtividade.xlsx'
df_resumo.to_excel(nome_arquivo, index=False)
print(f"\nMatriz linda e limpa salva como '{nome_arquivo}")
