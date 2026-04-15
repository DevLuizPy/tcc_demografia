import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# =============================================================================
# 1. LEITURA DOS DADOS
# =============================================================================
nome_arquivo = 'ipea.csv'

try:
    df = pd.read_csv(nome_arquivo, sep=';', decimal=',', usecols=[0, 1])
except FileNotFoundError:
    print(f"Erro: Arquivo '{nome_arquivo}' não encontrado.")
    exit()

df.columns = ['Data', 'Valor']
df = df.dropna()

# =============================================================================
# 2. TRATAMENTO E FILTRO DE ANOS (2004 a 2025)
# =============================================================================
df['Ano'] = df['Data'].astype(str).str[:4].astype(int)
df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')

# Agrupa por Ano e soma
df_anual = df.groupby('Ano')['Valor'].sum().reset_index()

# FILTRO: Remove 2003 e 2026 (Anos incompletos)
df_anual = df_anual[(df_anual['Ano'] >= 2004) & (df_anual['Ano'] <= 2025)]

# Cria uma coluna em Bilhões para a tabela do Excel ficar limpa
# (Assumindo que o dado do IPEA está em milhares. Se estiver em Reais absolutos, mude para / 1000000000)
df_anual['Valor_Bilhoes'] = df_anual['Valor'] / 1000000

# =============================================================================
# 3. EXPORTAÇÃO DA TABELA
# =============================================================================
df_anual.to_excel('Tabela_Anual_IPEA_Limpa.xlsx', index=False)
print("Tabela anual exportada com sucesso!")

# =============================================================================
# 4. GERAÇÃO DO GRÁFICO COM EIXO AJUSTADO
# =============================================================================
# Formatador para o eixo Y ficar como "R$ -150 Bi"
def formata_bilhoes(x, pos):
    bilhoes = x / 1000000 # Ajusta a escala visualmente
    return f'R$ {bilhoes:.0f} Bi'

plt.figure(figsize=(10, 6))

plt.plot(df_anual['Ano'], df_anual['Valor'], marker='o', color='firebrick', linewidth=2.5)

plt.fill_between(df_anual['Ano'], df_anual['Valor'], 0,
                 where=(df_anual['Valor'] < 0), color='firebrick', alpha=0.3, label='Déficit')
plt.fill_between(df_anual['Ano'], df_anual['Valor'], 0,
                 where=(df_anual['Valor'] >= 0), color='teal', alpha=0.3, label='Superávit')

plt.title('Evolução do Resultado do RGPS (2004-2025)', fontsize=14)
plt.xlabel('Ano', fontsize=12)
plt.ylabel('Resultado Nominal', fontsize=12)

plt.axhline(0, color='black', linewidth=1.2)

# Aplica o formatador no eixo Y
plt.gca().yaxis.set_major_formatter(FuncFormatter(formata_bilhoes))

# Força o eixo X a mostrar apenas números inteiros (anos)
plt.xticks(df_anual['Ano'], rotation=45)

plt.legend()
plt.tight_layout()

plt.savefig('grafico_anual_ipea_ajustado.png', dpi=300)
print("Gráfico gerado com eixo corrigido!")
plt.show()
