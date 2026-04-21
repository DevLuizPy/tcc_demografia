import os
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
import moviepy.editor as mp

# =====================================================================
# SEÇÃO 0: CARREGAMENTO E LIMPEZA
# =====================================================================
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
caminho_arquivo = os.path.join(DIRETORIO_ATUAL, 'Base_de_dados_Onu.xlsx')

df_homens = pd.read_excel(caminho_arquivo, sheet_name='Brazil_Homens')
df_mulheres = pd.read_excel(caminho_arquivo, sheet_name='Brazil_Mulheres')

png_files = []

df_homens.drop('Ano', axis=1, inplace=True)
df_mulheres.drop('Ano', axis=1, inplace=True)

df_homens.columns = [f"{col} anos" for col in df_homens.columns]
df_mulheres.columns = [f"{col} anos" for col in df_mulheres.columns]

# =====================================================================
# SEÇÃO 1: CÁLCULO DOS INDICADORES E EXPORTAÇÃO
# =====================================================================
anos_tabela = []
razao_dep_lista = []
razao_sup_lista = []
mediana_lista = []
pop_65_mais_lista = []

for ano in df_homens.index:
    ano_real = 2024 + ano
    pop_total = df_homens.loc[ano] + df_mulheres.loc[ano]

    pop_0_14 = pop_total.iloc[0:3].sum()
    pop_15_64 = pop_total.iloc[3:13].sum()
    pop_65_mais = pop_total.iloc[13:].sum()

    rd = ((pop_0_14 + pop_65_mais) / pop_15_64) * 100
    rs = pop_15_64 / (pop_0_14 + pop_65_mais)
    percentual_65_mais = (pop_65_mais / pop_total.sum()) * 100

    total_pessoas = pop_total.sum()
    metade = total_pessoas / 2
    acumulado = 0
    mediana = 0

    for col, pop_faixa in pop_total.items():
        if acumulado + pop_faixa >= metade:
            limite_inf_str = str(col).split('-')[0].replace('+', '').replace(' anos', '')
            limite_inf = int(limite_inf_str)
            largura_classe = 5
            mediana = limite_inf + ((metade - acumulado) / pop_faixa) * largura_classe
            break
        acumulado += pop_faixa

    anos_tabela.append(ano_real)
    razao_dep_lista.append(rd)
    razao_sup_lista.append(rs)
    mediana_lista.append(mediana)
    pop_65_mais_lista.append(percentual_65_mais)

df_indicadores = pd.DataFrame({
    'Ano': anos_tabela,
    'Razão de Dependência (%)': np.round(razao_dep_lista, 2),
    'Razão de Suporte (Ativos/Inativos)': np.round(razao_sup_lista, 2),
    'Idade Mediana': np.round(mediana_lista, 1),
    '% Idosos (65+)': np.round(pop_65_mais_lista, 2)
})

# Salvando dentro da pasta certa
caminho_excel_out = os.path.join(DIRETORIO_ATUAL, 'Indicadores_Demograficos_Brasil_ONU.xlsx')
df_indicadores.to_excel(caminho_excel_out, index=False)

# =====================================================================
# SEÇÃO 2: GRÁFICOS DE LINHA
# =====================================================================
def estilizar_grafico(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    ax.set_xlim(df_indicadores['Ano'].min(), df_indicadores['Ano'].max())

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df_indicadores['Ano'], df_indicadores['Razão de Dependência (%)'], color='#b2182b', linewidth=3)
ax.set_title('Projeção da Razão de Dependência - Brasil (2024-2100)', pad=15, fontsize=14, fontweight='bold')
ax.set_ylabel('Razão de Dependência (%)')
estilizar_grafico(ax)
plt.tight_layout()
plt.savefig(os.path.join(DIRETORIO_ATUAL, 'grafico_razao_dependencia.png'), dpi=300)
plt.close()

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df_indicadores['Ano'], df_indicadores['Razão de Suporte (Ativos/Inativos)'], color='#053061', linewidth=3)
ax.set_title('Projeção da Razão de Suporte Demográfico - Brasil (2024-2100)', pad=15, fontsize=14, fontweight='bold')
ax.set_ylabel('Ativos por Inativo')
estilizar_grafico(ax)
plt.tight_layout()
plt.savefig(os.path.join(DIRETORIO_ATUAL, 'grafico_razao_suporte.png'), dpi=300)
plt.close()

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df_indicadores['Ano'], df_indicadores['Idade Mediana'], color='#762a83', linewidth=3)
ax.set_title('Evolução da Idade Mediana - Brasil (2024-2100)', pad=15, fontsize=14, fontweight='bold')
ax.set_ylabel('Idade (anos)')
estilizar_grafico(ax)
plt.tight_layout()
plt.savefig(os.path.join(DIRETORIO_ATUAL, 'grafico_idade_mediana.png'), dpi=300)
plt.close()

# =====================================================================
# SEÇÃO 3: VÍDEO DAS PIRÂMIDES ETÁRIAS
# =====================================================================
def percentual(x, pos):
    return f'{abs(x):.0f}%'

print("Gerando frames da pirâmide...")

for ano in df_homens.index:
    plt.figure(figsize=(10, 8))

    total_populacao = df_homens.loc[ano].sum() + df_mulheres.loc[ano].sum()
    populacao_homens = -df_homens.loc[ano] / total_populacao * 100
    populacao_mulheres = df_mulheres.loc[ano] / total_populacao * 100
    faixa_etaria = df_homens.columns

    plt.barh(faixa_etaria, populacao_homens, color='red', label='Homens')
    plt.barh(faixa_etaria, populacao_mulheres, color='blue', label='Mulheres')
    
    plt.xlabel('População (%)')
    plt.ylabel('Faixa Etária')
    ano_1 = 2024 + ano
    plt.title(f'Estrutura Etária em {ano_1} (%)')
    plt.legend()

    plt.xlim(-6, 6)
    plt.xticks(np.arange(-6, 7, 1))
    plt.gca().xaxis.set_major_formatter(FuncFormatter(percentual))

    # Salvando os frames 
    filename = os.path.join(DIRETORIO_ATUAL, f"estrutura_etaria_{ano_1}.png")
    plt.savefig(filename, dpi=300)
    png_files.append(filename)
    plt.close()

print("Renderizando vídeo...")
clip = mp.ImageSequenceClip(png_files, fps=4) 
# Salvando o vídeo final 
clip.write_videofile(os.path.join(DIRETORIO_ATUAL, 'estrutura_etaria.mp4'), codec='libx264')
print("Tudo gerado e salvo dentro da subpasta com sucesso!")