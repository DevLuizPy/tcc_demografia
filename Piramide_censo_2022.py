import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# 1. Leitura dos dados
# skiprows=8 pula as 8 primeiras linhas para começar exatamente na linha 9 do Excel.
# Correção no usecols para pegar as colunas exatas: A, C e D
df = pd.read_excel(
    'Tabela_9514_Piramide.xlsx',
    skiprows=7,
    usecols="A, C, D",
    names=['Idade', 'Homens', 'Mulheres']
)

# Transforma a coluna Idade em texto para garantir que o eixo Y seja categórico
df['Idade'] = df['Idade'].astype(str)

# Remove a linha de "Total" caso ela exista no final da tabela
df = df[~df['Idade'].str.contains('Total', case=False, na=False)]
df = df.dropna()

# 2. Formatador do eixo X para porcentagem
def percentual(x, pos):
    x = abs(x)
    return f'{x:.0f}%'

# 3. Cálculo dos percentuais
total_populacao = df['Homens'].sum() + df['Mulheres'].sum()
df['Homens_Pct'] = -(df['Homens'] / total_populacao) * 100
df['Mulheres_Pct'] = (df['Mulheres'] / total_populacao) * 100

# 4. Geração do gráfico
plt.figure(figsize=(10, 8))

# Mantendo o estilo do seu código original
plt.barh(df['Idade'], df['Homens_Pct'], color='red', label='Homens')
plt.barh(df['Idade'], df['Mulheres_Pct'], color='blue', label='Mulheres')

plt.xlabel('População (%)')
plt.ylabel('Faixa Etária')
plt.title('Estrutura Etária do Brasil (%) - 2022')
plt.legend()

# Aplicando a formatação percentual
plt.gca().xaxis.set_major_formatter(FuncFormatter(percentual))

# Ajusta o layout para não cortar os textos e salva a imagem
plt.tight_layout()
plt.savefig('piramide_etaria_brasil_pct_2022.png')
plt.show()
