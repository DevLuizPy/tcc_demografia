import pandas as pd
import matplotlib.pyplot as plt

# 1. Carregar os dados
# DICA: Verifique o nome da aba no Excel. Se for a segunda aba, use sheet_name=1
# Se você souber o nome (ex: 'Séries'), use sheet_name='Séries'
df = pd.read_excel('Produtividade_FGV.xlsx', sheet_name="Produtividade - R$ 2021", header=None)

# Debug rápido: tire o comentário da linha abaixo se o erro persistir para ver o que o Python está lendo
# print(df.head(15))

# 2. Extrair os dados (Row 9 Excel = Index 8 Python)
# Se o IBRE colocou uma coluna vazia no começo (A), o índice pode mudar.
# Vamos garantir que estamos pegando as colunas certas:
anos = pd.to_numeric(df.iloc[8:52, 0], errors='coerce') # Coluna A
produtividade = pd.to_numeric(df.iloc[8:52, 2], errors='coerce') # Coluna C

# 3. Limpeza de NAs (essencial para não quebrar o gráfico se houver linhas vazias no fim)
mask = anos.notna() & produtividade.notna()
anos = anos[mask]
produtividade = produtividade[mask]

# 4. Criação do Gráfico
fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(anos, produtividade, color='#053061', linewidth=3, label='Produtividade por Pessoa Ocupada')

ax.set_title('Gráfico X – Evolução da Produtividade do Trabalho no Brasil (1981-2024)\n(Em R$ constantes de 2021 por pessoal ocupado)',
             pad=20, fontsize=12, fontweight='bold')
ax.set_ylabel('R$ por Pessoa Ocupada')
ax.set_xlabel('Ano')

ax.set_ylim(bottom=0)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.grid(False)
ax.set_xticks(range(int(anos.min()), int(anos.max()) + 1, 4))

plt.tight_layout()
plt.savefig('Grafico_Produtividade_Final.png', dpi=300, bbox_inches='tight')
plt.show()

print("Agora foi! Gráfico gerado.")
