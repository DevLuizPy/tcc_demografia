import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import moviepy.editor as mp

df_homens: DataFrame = pd.read_excel('C:\\Users\\gisel\\OneDrive\\Documentos\\Tcc-demografia.xlsm',
                                     sheet_name='Brazil_Homens')
df_mulheres: DataFrame = pd.read_excel('C:\\Users\\gisel\\OneDrive\\Documentos\\Tcc-demografia.xlsm',
                                       sheet_name='Brazil_Mulheres')

png_files = []

df_homens.drop('Ano', axis=1, inplace=True)
df_mulheres.drop('Ano', axis=1, inplace=True)

# Adicionando " anos" ao nome de todas as colunas de faixa etária
df_homens.columns = [f"{col} anos" for col in df_homens.columns]
df_mulheres.columns = [f"{col} anos" for col in df_mulheres.columns]

# =====================================================================
# SEÇÃO 1: CÁLCULO DOS INDICADORES DEMOGRÁFICOS E EXPORTAÇÃO
# =====================================================================
anos_tabela = []
razao_dep_lista = []
razao_sup_lista = []
mediana_lista = []

for ano in df_homens.index:
    ano_real = 2024 + ano

    pop_total = df_homens.loc[ano] + df_mulheres.loc[ano]

    # Divide nas grandes faixas etárias
    pop_0_14 = pop_total.iloc[0:3].sum()
    pop_15_64 = pop_total.iloc[3:13].sum()
    pop_65_mais = pop_total.iloc[13:].sum()

    # Cálculos das Razões
    rd = ((pop_0_14 + pop_65_mais) / pop_15_64) * 100
    rs = pop_15_64 / (pop_0_14 + pop_65_mais)

    # Cálculo da Idade Mediana
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

df_indicadores = pd.DataFrame({
    'Ano': anos_tabela,
    'Razão de Dependência (%)': razao_dep_lista,
    'Razão de Suporte (Ativos/Inativos)': razao_sup_lista,
    'Idade Mediana': mediana_lista
})

df_indicadores['Razão de Dependência (%)'] = df_indicadores['Razão de Dependência (%)'].round(2)
df_indicadores['Razão de Suporte (Ativos/Inativos)'] = df_indicadores['Razão de Suporte (Ativos/Inativos)'].round(2)
df_indicadores['Idade Mediana'] = df_indicadores['Idade Mediana'].round(1)

# === SALVANDO EM EXCEL ===
df_indicadores.to_excel('Indicadores_Demograficos_Brasil_ONU.xlsx', index=False)

# =====================================================================
# SEÇÃO 2: GERAÇÃO DOS GRÁFICOS DE LINHA (INDICADORES ATÉ 2100)
# =====================================================================
# 1. Gráfico da Razão de Dependência
plt.figure(figsize=(10, 6))
plt.plot(df_indicadores['Ano'], df_indicadores['Razão de Dependência (%)'], color='firebrick', linewidth=2.5)
plt.title('Projeção da Razão de Dependência - Brasil (2024-2100)', fontsize=14)
plt.xlabel('Ano', fontsize=12)
plt.ylabel('Razão de Dependência (%)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('grafico_razao_dependencia.png', dpi=300)
plt.close()

# 2. Gráfico da Razão de Suporte
plt.figure(figsize=(10, 6))
plt.plot(df_indicadores['Ano'], df_indicadores['Razão de Suporte (Ativos/Inativos)'], color='teal', linewidth=2.5)
plt.title('Projeção da Razão de Suporte Demográfico - Brasil (2024-2100)', fontsize=14)
plt.xlabel('Ano', fontsize=12)
plt.ylabel('Proporção (Ativos para cada Inativo)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('grafico_razao_suporte.png', dpi=300)
plt.close()

# 3. Gráfico da Idade Mediana
plt.figure(figsize=(10, 6))
plt.plot(df_indicadores['Ano'], df_indicadores['Idade Mediana'], color='purple', linewidth=2.5)
plt.title('Evolução da Idade Mediana - Brasil (2024-2100)', fontsize=14)
plt.xlabel('Ano', fontsize=12)
plt.ylabel('Idade (anos)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('grafico_idade_mediana.png', dpi=300)
plt.close()

print("Gráficos de indicadores salvos com sucesso (PNG)!")


# =====================================================================
# SEÇÃO 3: GERAÇÃO DO VÍDEO DAS PIRÂMIDES ETÁRIAS
# =====================================================================
def percentual(x, pos):
    x = abs(x)
    return f'{x:.0f}%'


for ano in df_homens.index:
    plt.figure(figsize=(10, 8))

    total_populacao = df_homens.loc[ano].sum() + df_mulheres.loc[ano].sum()
    populacao_homens: DataFrame = -df_homens.loc[ano] / total_populacao * 100
    populacao_mulheres: DataFrame = df_mulheres.loc[ano] / total_populacao * 100
    faixa_etaria = df_homens.columns

    plt.barh(faixa_etaria, populacao_homens, color='red', label='Homens')
    plt.barh(faixa_etaria, populacao_mulheres, color='blue', label='Mulheres')
    plt.xlabel('População (%)')
    plt.ylabel('Faixa Etária')
    ano_1 = 2024 + ano
    plt.title(f'Estrutura Etária em {ano_1} (%)')
    plt.legend()

    plt.gca().xaxis.set_major_formatter(FuncFormatter(percentual))

    filename = f"estrutura_etaria_{ano_1}.png"
    plt.savefig(filename)
    png_files.append(filename)
    plt.close()

clip = mp.ImageSequenceClip(png_files, fps=2)
clip.write_videofile('estrutura_etaria.mp4', codec='libx264')
