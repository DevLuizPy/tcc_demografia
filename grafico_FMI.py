import pandas as pd
import matplotlib.pyplot as plt

# 1. Carregar os dados (Mesma lógica de índices)
df = pd.read_excel('Base_de_Dados_FMI_2.xlsx', header=None)
anos = list(range(1981, 2023))

# 3. Puxar os dados e corrigir a escala (/ 1000)
br_inv = pd.to_numeric(df.iloc[1, 8:50], errors='coerce') / 1000
br_poup = pd.to_numeric(df.iloc[2, 8:50], errors='coerce') / 1000
ch_inv = pd.to_numeric(df.iloc[3, 8:50], errors='coerce') / 1000
ch_poup = pd.to_numeric(df.iloc[4, 8:50], errors='coerce') / 1000
kr_inv = pd.to_numeric(df.iloc[5, 8:50], errors='coerce') / 1000
kr_poup = pd.to_numeric(df.iloc[6, 8:50], errors='coerce') / 1000

# 4. A Magia do Gráfico ABNT (COM CORES VISÍVEIS)
fig, ax = plt.subplots(figsize=(12, 7))

# --- BRASIL (Linhas SÓLIDAS e Grossas) ---
# Usando Vermelho Escuro e Azul Marinho para contraste máximo
ax.plot(anos, br_inv, color='#b2182b', linewidth=3.5, linestyle='-', label='Brasil - Investimento')
ax.plot(anos, br_poup, color='#053061', linewidth=3.5, linestyle='-', label='Brasil - Poupança')

# --- CHILE (Linhas TRACEJADAS) ---
# Usando Verde Escuro e Ouro Velho saturados
ax.plot(anos, ch_inv, color='#1b7837', linewidth=2.5, linestyle='--', label='Chile - Investimento')
ax.plot(anos, ch_poup, color='#b8860b', linewidth=2.5, linestyle='--', label='Chile - Poupança')

# --- COREIA DO SUL (Linhas PONTILHADAS) ---
# Usando Roxo Escuro e Laranja Queimado vibrantes
ax.plot(anos, kr_inv, color='#762a83', linewidth=2.5, linestyle=':', label='Coreia - Investimento')
ax.plot(anos, kr_poup, color='#d95f02', linewidth=2.5, linestyle=':', label='Coreia - Poupança')

# --- Configurações Finais ABNT ---
ax.set_title('Gráfico X – Taxa de Investimento e Poupança Nacional (% do PIB) \nBrasil, Chile e Coreia do Sul (1981-2022)', pad=15, fontsize=12)
ax.set_ylabel('% do PIB')
ax.set_xlabel('Ano')
ax.set_ylim(bottom=0) # Eixo Y começando do ZERO (essencial!)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xticks(range(1981, 2023, 4))

# Legenda fora do gráfico (embaixo) com 3 colunas
ax.legend(frameon=False, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3, fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.3)

plt.tight_layout()
plt.savefig('Grafico_Comparacao_Cores_Visiveis.png', dpi=300, bbox_inches='tight')
print("Gráfico com cores saturadas gerado com sucesso!")
plt.show()
