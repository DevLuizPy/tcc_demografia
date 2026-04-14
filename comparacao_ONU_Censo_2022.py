import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# ==========================================
# 1. PREPARAÇÃO DOS DADOS DA ONU (2024)
# ==========================================
df_homens_onu = pd.read_excel('C:\\Users\\gisel\\OneDrive\\Documentos\\Tcc-demografia.xlsm', sheet_name='Brazil_Homens')
df_mulheres_onu = pd.read_excel('C:\\Users\\gisel\\OneDrive\\Documentos\\Tcc-demografia.xlsm', sheet_name='Brazil_Mulheres')

df_homens_onu.drop('Ano', axis=1, inplace=True)
df_mulheres_onu.drop('Ano', axis=1, inplace=True)

# Pegando a primeira linha (índice 0), que corresponde ao ano inicial (2024)
pop_homens_onu = df_homens_onu.iloc[0]
pop_mulheres_onu = df_mulheres_onu.iloc[0]

total_onu = pop_homens_onu.sum() + pop_mulheres_onu.sum()
pct_homens_onu = -(pop_homens_onu / total_onu) * 100
pct_mulheres_onu = (pop_mulheres_onu / total_onu) * 100

# Criando a lista de faixas etárias padronizada
faixas_etarias = [f"{col} anos" for col in df_homens_onu.columns]


# ==========================================
# 2. PREPARAÇÃO DOS DADOS DO CENSO (2022)
# ==========================================
df_censo = pd.read_excel('Tabela_9514_Piramide.xlsx', skiprows=7, usecols="A, C, D", names=['Idade', 'Homens', 'Mulheres'])
df_censo['Idade'] = df_censo['Idade'].astype(str)
df_censo = df_censo[~df_censo['Idade'].str.contains('Total', case=False, na=False)].dropna()

total_censo = df_censo['Homens'].sum() + df_censo['Mulheres'].sum()
pct_homens_censo = -(df_censo['Homens'] / total_censo) * 100
pct_mulheres_censo = (df_censo['Mulheres'] / total_censo) * 100


# ==========================================
# 3. CÁLCULO DA DIFERENÇA PERCENTUAL (Console)
# ==========================================
# Cria uma tabela no terminal para você ver a diferença exata (ONU - Censo)
df_diferenca = pd.DataFrame({
    'Faixa Etária': faixas_etarias,
    'Diferença Homens (%)': abs(pct_homens_onu.values) - abs(pct_homens_censo.values),
    'Diferença Mulheres (%)': pct_mulheres_onu.values - pct_mulheres_censo.values
})
print("\n=== DIFERENÇA PERCENTUAL (ONU 2024 - CENSO 2022) ===")
print(df_diferenca.to_string(index=False))
print("====================================================\n")


# ==========================================
# 4. PLOTAGEM DA PIRÂMIDE SOBREPOSTA
# ==========================================
def percentual(x, pos):
    return f'{abs(x):.0f}%'

plt.figure(figsize=(12, 8))

# 1ª Camada: Censo 2022 (Barras preenchidas e levemente transparentes)
# Usando .values para garantir que o Pandas não tente realinhar os índices incorretamente
plt.barh(faixas_etarias, pct_homens_censo.values, color='red', alpha=0.5, label='Homens - Censo (2022)')
plt.barh(faixas_etarias, pct_mulheres_censo.values, color='blue', alpha=0.5, label='Mulheres - Censo (2022)')

# 2ª Camada: ONU 2024 (Apenas os contornos vazados)
# color='none' deixa o miolo vazio, e edgecolor pinta a linha
plt.barh(faixas_etarias, pct_homens_onu.values, color='none', edgecolor='darkred', linewidth=2, label='Homens - ONU (2024)')
plt.barh(faixas_etarias, pct_mulheres_onu.values, color='none', edgecolor='darkblue', linewidth=2, label='Mulheres - ONU (2024)')

plt.xlabel('População (%)', fontsize=12)
plt.ylabel('Faixa Etária', fontsize=12)
plt.title('Comparação da Estrutura Etária do Brasil: Censo 2022 vs ONU 2024', fontsize=14)
plt.legend(loc='upper right')

# Formatação final
plt.gca().xaxis.set_major_formatter(FuncFormatter(percentual))
plt.grid(axis='x', linestyle='--', alpha=0.4)

plt.tight_layout()
plt.savefig('comparacao_censo2022_onu2024.png', dpi=300)
plt.show()
