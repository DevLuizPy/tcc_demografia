import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from datetime import datetime

# ==========================================
# CONFIGURAÇÕES DE ESTÉTICA ACADÊMICA
# ==========================================
# Remove as bordas feias e desliga as linhas de grade
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.grid'] = False  # Linhas de grade removidas


# Função auxiliar para converter "1980.01" em datetime
def converter_data(val):
    try:
        ano, mes = map(int, str(val).split('.'))
        return datetime(ano, mes, 1)
    except (ValueError, AttributeError):
        return None


# ==========================================
# GRÁFICO 1: IPEA_1980_2000.xlsx
# ==========================================
arquivo_1 = 'IPEA_1980_2000.xlsx'
print("Processando arquivo 1...")

try:
    df1 = pd.read_excel(arquivo_1, header=0)
    df1.columns = ['Data', 'Valor']

    # Converter data e filtrar intervalo (Jan 1980 a Dez 2000)
    df1['Data_Completa'] = df1['Data'].apply(converter_data)
    df1 = df1.dropna(subset=['Data_Completa'])
    df1_filtrado = df1[(df1['Data_Completa'] >= datetime(1980, 1, 1)) &
                       (df1['Data_Completa'] <= datetime(2000, 12, 31))]

    # Média anual (anos completos)
    df1_anual = df1_filtrado.groupby(df1_filtrado['Data_Completa'].dt.year)['Valor'].mean().reset_index()
    df1_anual.columns = ['Ano', 'Média_Anual']

    # Criar gráfico individual
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df1_anual['Ano'], df1_anual['Média_Anual'], marker='o', color='#1f497d', linewidth=2.5, markersize=6)

    ax.set_title('Taxa Média de Desemprego Aberto - PME Antiga (1980-2000)', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Ano', fontsize=12, fontweight='bold')
    ax.set_ylabel('Desemprego (%)', fontsize=12, fontweight='bold')

    # Formatação dos eixos
    ax.set_xticks(df1_anual['Ano'])  # Força mostrar todos os anos
    plt.xticks(rotation=45)
    ax.yaxis.set_major_formatter(PercentFormatter(decimals=1))  # Coloca % no eixo Y

    plt.savefig('grafico_ipea_1980_2000.png', dpi=300, bbox_inches='tight')
    print(f"  → salvo: grafico_ipea_1980_2000.png ({len(df1_anual)} anos)")

except FileNotFoundError:
    print(f"  ✗ Erro: Arquivo {arquivo_1} não encontrado.")
plt.close()

# ==========================================
# GRÁFICO 2: IPEA_2002_2015.xlsx (até 2010)
# ==========================================
arquivo_2 = 'IPEA_2002_2015.xlsx'
print("\nProcessando arquivo 2...")

try:
    df2 = pd.read_excel(arquivo_2, header=0)
    df2.columns = ['Data', 'Valor']

    df2['Data_Completa'] = df2['Data'].apply(converter_data)
    df2 = df2.dropna(subset=['Data_Completa'])
    df2_filtrado = df2[(df2['Data_Completa'] >= datetime(2002, 3, 1)) &
                       (df2['Data_Completa'] <= datetime(2015, 12, 31))]

    # Média 2002
    df2_2002 = df2_filtrado[df2_filtrado['Data_Completa'].dt.year == 2002]
    media_2002 = df2_2002['Valor'].mean()

    # Média outros anos
    df2_outros_anos = df2_filtrado[df2_filtrado['Data_Completa'].dt.year != 2002]
    df2_anual_completo = df2_outros_anos.groupby(df2_outros_anos['Data_Completa'].dt.year)['Valor'].mean().reset_index()

    df2_anual_completo.columns = ['Ano', 'Média_Anual']

    novo_linha_2002 = pd.DataFrame({'Ano': [2002], 'Média_Anual': [media_2002]})
    df2_anual_final = pd.concat([novo_linha_2002, df2_anual_completo]).sort_values('Ano').reset_index(drop=True)

    df2_plot = df2_anual_final[df2_anual_final['Ano'] <= 2010]

    # Criar gráfico individual
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df2_plot['Ano'], df2_plot['Média_Anual'], marker='o', color='#c00000', linewidth=2.5, markersize=6)

    ax.set_title('Taxa Média de Desemprego Aberto - Nova PME (2002-2010)', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Ano', fontsize=12, fontweight='bold')
    ax.set_ylabel('Desemprego (%)', fontsize=12, fontweight='bold')

    ax.set_xticks(df2_plot['Ano'])
    ax.yaxis.set_major_formatter(PercentFormatter(decimals=1))

    plt.savefig('grafico_ipea_2002_2010.png', dpi=300, bbox_inches='tight')
    print(f"  → salvo: grafico_ipea_2002_2010.png ({len(df2_plot)} anos)")

except FileNotFoundError:
    print(f"  ✗ Erro: Arquivo {arquivo_2} não encontrado.")
plt.close()

# ==========================================
# GRÁFICO 3: IPEA_2012_2026.xlsx (até 2022)
# ==========================================
arquivo_3 = 'IPEA_2012_2026.xlsx'
print("\nProcessando arquivo 3...")

try:
    df3 = pd.read_excel(arquivo_3, header=0)
    df3.columns = ['Data', 'Valor']

    df3['Data_Completa'] = df3['Data'].apply(converter_data)
    df3 = df3.dropna(subset=['Data_Completa'])
    df3_filtrado = df3[(df3['Data_Completa'] >= datetime(2012, 3, 1)) &
                       (df3['Data_Completa'] <= datetime(2026, 1, 31))]

    # Média 2012
    df3_2012 = df3_filtrado[df3_filtrado['Data_Completa'].dt.year == 2012]
    media_2012 = df3_2012['Valor'].mean()

    # Média outros anos
    df3_outros_anos = df3_filtrado[df3_filtrado['Data_Completa'].dt.year != 2012]
    df3_anual_completo = df3_outros_anos.groupby(df3_outros_anos['Data_Completa'].dt.year)['Valor'].mean().reset_index()

    df3_anual_completo.columns = ['Ano', 'Média_Anual']

    novo_linha_2012 = pd.DataFrame({'Ano': [2012], 'Média_Anual': [media_2012]})
    df3_anual_final = pd.concat([novo_linha_2012, df3_anual_completo]).sort_values('Ano').reset_index(drop=True)

    df3_plot = df3_anual_final[df3_anual_final['Ano'] <= 2022]

    # Criar gráfico individual
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df3_plot['Ano'], df3_plot['Média_Anual'], marker='o', color='#006400', linewidth=2.5, markersize=6)

    ax.set_title('Taxa Média de Desocupação - PNAD Contínua (2012-2022)', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Ano', fontsize=12, fontweight='bold')
    ax.set_ylabel('Desemprego (%)', fontsize=12, fontweight='bold')

    ax.set_xticks(df3_plot['Ano'])
    ax.yaxis.set_major_formatter(PercentFormatter(decimals=1))

    plt.savefig('grafico_ipea_2012_2022.png', dpi=300, bbox_inches='tight')
    print(f"  → salvo: grafico_ipea_2012_2022.png ({len(df3_plot)} anos)")

except FileNotFoundError:
    print(f"  ✗ Erro: Arquivo {arquivo_3} não encontrado.")
plt.close()

print("\n" + "=" * 50)
print("GRÁFICOS GERADOS COM SUCESSO!")
print("=" * 50)
