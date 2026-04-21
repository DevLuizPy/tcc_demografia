import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np

# 1. Leitura e Limpeza dos Dados
df = pd.read_excel(
    'Tabela_9514_Piramide.xlsx',
    skiprows=7,
    usecols="A, C, D",
    names=['Idade', 'Homens', 'Mulheres']
)

df['Idade'] = df['Idade'].astype(str)
df = df[~df['Idade'].str.contains('Total', case=False, na=False)]
df = df.dropna()

# 2. Cálculo dos Totais e Formatação das Legendas
total_homens = df['Homens'].sum()
total_mulheres = df['Mulheres'].sum()

total_homens_form = f"{total_homens:,}".replace(',', '.')
total_mulheres_form = f"{total_mulheres:,}".replace(',', '.')

label_homens = f"Homens ({total_homens_form})"
label_mulheres = f"Mulheres ({total_mulheres_form})"

# 3. Cálculo dos Percentuais Relativos
total_populacao = total_homens + total_mulheres
df['Homens_Pct'] = -(df['Homens'] / total_populacao) * 100
df['Mulheres_Pct'] = (df['Mulheres'] / total_populacao) * 100

def percentual(x, pos):
    x = abs(x)
    return f'{x:.0f}%'

# 4. Geração do Gráfico
plt.figure(figsize=(10, 8))

plt.barh(df['Idade'], df['Homens_Pct'], color='red', label=label_homens)
plt.barh(df['Idade'], df['Mulheres_Pct'], color='blue', label=label_mulheres)

plt.xlabel('População (%)')
plt.ylabel('Faixa Etária')
plt.title('Estrutura Etária do Brasil (%) - 2022')

# Configuração da Grade Vertical
ticks_x_especificos = np.arange(-4, 5, 1)
plt.xticks(ticks_x_especificos)
plt.grid(axis='x', linestyle='--', alpha=0.5)

plt.legend(title="Gênero", loc='upper right')
plt.gca().xaxis.set_major_formatter(FuncFormatter(percentual))

plt.tight_layout()
plt.savefig('piramide_etaria_brasil_pct_2022_final.png')
plt.show()
