import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np  # Import necessário para gerar as linhas de grade exatas

# 1. Leitura dos dados (Sem alterações)
df = pd.read_excel(
    'Tabela_9514_Piramide.xlsx',
    skiprows=7,
    usecols="A, C, D",
    names=['Idade', 'Homens', 'Mulheres']
)

# Transforma a coluna Idade em texto (Sem alterações)
df['Idade'] = df['Idade'].astype(str)

# Remove a linha de "Total" caso ela exista no final da tabela (Sem alterações)
df = df[~df['Idade'].str.contains('Total', case=False, na=False)]
df = df.dropna()

# --- NOVO: Cálculo dos Totais e Formatação das Legendas ---
# Calcula os totais absolutos de homens e mulheres
total_homens = df['Homens'].sum()
total_mulheres = df['Mulheres'].sum()

# Formata os números no padrão brasileiro (pontos como separadores de milhar)
# Exemplo: de 83607833 para '83.607.833'
total_homens_form = f"{total_homens:,}".replace(',', '.')
total_mulheres_form = f"{total_mulheres:,}".replace(',', '.')

# Cria as novas legendas que incluem os totais formatados
label_homens = f"Homens ({total_homens_form})"
label_mulheres = f"Mulheres ({total_mulheres_form})"
# ---------------------------------------------------------

# 2. Formatador do eixo X para porcentagem (Sem alterações)
def percentual(x, pos):
    x = abs(x)
    return f'{x:.0f}%'

# 3. Cálculo dos percentuais (Otimizado usando os totais já calculados)
total_populacao = total_homens + total_mulheres
df['Homens_Pct'] = -(df['Homens'] / total_populacao) * 100
df['Mulheres_Pct'] = (df['Mulheres'] / total_populacao) * 100

# 4. Geração do gráfico
plt.figure(figsize=(10, 8))

# [ALTERAÇÃO]: Adicionando labels com os totais calculados
plt.barh(df['Idade'], df['Homens_Pct'], color='red', label=label_homens)
plt.barh(df['Idade'], df['Mulheres_Pct'], color='blue', label=label_mulheres)

plt.xlabel('População (%)')
plt.ylabel('Faixa Etária')
plt.title('Estrutura Etária do Brasil (%) - 2022')

# --- NOVO: Definindo Grade Específica (Vertical Grid Lines) ---
# Range safe para pirâmide no eixo X (%): -4% até 4% (passo 1%)
# numpy.arange gera [-4, -3, -2, -1, 0, 1, 2, 3, 4]
ticks_x_especificos = np.arange(-4, 5, 1)

# Aplica esses ticks como as marcas principais do eixo X
plt.xticks(ticks_x_especificos)

# Ativa linhas de grade apenas no eixo X (linhas VERTICAIS no gráfico)
# que cruzam as marcas exatas de 1%, 2%, 3%, 4% de cada lado e o zero.
# Usando linestyle='--' e alpha=0.5 para ficarem sutis como na imagem.
plt.grid(axis='x', linestyle='--', alpha=0.5)
# -------------------------------------------------------------

# [ALTERAÇÃO]: Adicionando Título à Legenda
plt.legend(title="Gênero", loc='upper right')

# Aplicando a formatação percentual (Sem alterações)
plt.gca().xaxis.set_major_formatter(FuncFormatter(percentual))

# Ajusta o layout para não cortar os textos e salva a imagem (Sem alterações)
plt.tight_layout()
plt.savefig('piramide_etaria_brasil_pct_2022_final.png')
plt.show()
