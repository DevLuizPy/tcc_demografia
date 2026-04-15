import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# =============================================================================
# 1. CARREGAMENTO E LIMPEZA ROBUSTA DOS DADOS
# =============================================================================
print("Lendo a base do NTA...")
df_nta = pd.read_excel('NTA.xlsx')

df_nta.columns = df_nta.columns.str.strip()
if 'VarName' in df_nta.columns:
    df_nta['VarName'] = df_nta['VarName'].astype(str).str.strip().str.upper()

df_nta['Year'] = pd.to_numeric(df_nta['Year'], errors='coerce')

anos_nta = [1996, 2002, 2008]
perfis = {}
idades = np.arange(91)  # Vetor de 0 a 90

# =============================================================================
# 2. EXTRAÇÃO DOS DADOS
# =============================================================================
for ano in anos_nta:
    linha_yl = df_nta[(df_nta['Year'] == ano) & (df_nta['VarName'] == 'YL')]
    linha_c = df_nta[(df_nta['Year'] == ano) & (df_nta['VarName'] == 'C')]

    if linha_yl.empty or linha_c.empty:
        print(f"ALERTA: Dados não encontrados para o ano {ano}. Verificando o próximo...")
        continue

    yl_vetor = linha_yl.loc[:, 'Age0':'Age90'].values[0]
    c_vetor = linha_c.loc[:, 'Age0':'Age90'].values[0]
    perfis[ano] = {'YL': yl_vetor, 'C': c_vetor}

print("Dados extraídos com sucesso! Iniciando a geração dos gráficos...")

# =============================================================================
# ESTÉTICA GLOBAL (Minimalismo Acadêmico)
# =============================================================================
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12


def limpar_eixos(ax):
    """Remove as bordas superior e direita para um visual clean."""
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(1.2)
    ax.spines['bottom'].set_linewidth(1.2)
    ax.tick_params(width=1.2)


# =============================================================================
# 3. GERAÇÃO DOS 3 GRÁFICOS INDIVIDUAIS (NOMINAIS)
# =============================================================================
for ano, dados in perfis.items():
    fig, ax = plt.subplots(figsize=(10, 6))

    c_vetor = dados['C']
    yl_vetor = dados['YL']

    # Paleta Elegante: Vermelho Carmesim (C) e Azul Marinho (YL)
    cor_c = '#B22222'
    cor_yl = '#000080'

    ax.plot(idades, c_vetor, label='Consumo (C)', color=cor_c, linewidth=3)
    ax.plot(idades, yl_vetor, label='Renda do Trabalho (YL)', color=cor_yl, linewidth=3)

    ax.fill_between(idades, c_vetor, yl_vetor, where=(yl_vetor > c_vetor),
                    interpolate=True, color=cor_yl, alpha=0.1, label='Superávit')
    ax.fill_between(idades, c_vetor, yl_vetor, where=(c_vetor >= yl_vetor),
                    interpolate=True, color=cor_c, alpha=0.1, label='Déficit')

    ax.set_title(f'Perfil Etário de Consumo e Renda do Trabalho - Brasil {ano}', pad=15)
    ax.set_xlabel('Idade (anos)')
    ax.set_ylabel('Valores per capita anuais nominais')

    ax.set_xlim(0, 90)
    ax.set_ylim(bottom=0)

    limpar_eixos(ax)  # Aplica o visual clean (sem grades)
    ax.legend(
        loc='upper left',
        fontsize=11,
        frameon=True,
        facecolor='white',  # Fundo totalmente branco
        edgecolor='#CCCCCC',  # Borda cinza neutra e bem clara
        framealpha=1.0,  # Sem transparência (opaco)
        borderpad=1.2,
        labelspacing=0.8
    )

    plt.tight_layout()
    nome_arq_indiv = f'grafico_nta_perfil_nominal_{ano}.png'
    plt.savefig(nome_arq_indiv, dpi=300, transparent=False, facecolor='white')
    plt.close()
    print(f" -> Salvo com sucesso: {nome_arq_indiv}")

# =============================================================================
# 4. GERAÇÃO DO GRÁFICO COMPARATIVO (NORMALIZADO)
# =============================================================================
if len(perfis) > 0:
    fig, ax = plt.subplots(figsize=(11, 6.5))

    # Degradê de cores para mostrar a evolução do tempo (Tons mais escuros)
    cores_c = {1996: '#FB6A4A', 2002: '#CB181D', 2008: '#67000D'}  # Tons de Vermelho Escuro
    cores_yl = {1996: '#6BAED6', 2002: '#08519C', 2008: '#08306B'}  # Tons de Azul Escuro
    estilos = {1996: ':', 2002: '--', 2008: '-'}

    for ano, dados in perfis.items():
        c_vetor = dados['C']
        yl_vetor = dados['YL']

        fator_normalizacao = np.mean(yl_vetor[30:50])
        c_norm = c_vetor / fator_normalizacao
        yl_norm = yl_vetor / fator_normalizacao

        ax.plot(idades, c_norm, label=f'Consumo ({ano})',
                color=cores_c[ano], linestyle=estilos[ano], linewidth=2.5)
        ax.plot(idades, yl_norm, label=f'Renda ({ano})',
                color=cores_yl[ano], linestyle=estilos[ano], linewidth=2.5)

    ax.set_title('Evolução do Perfil de Consumo e Renda do Trabalho (1996 a 2008)', pad=15)
    ax.set_xlabel('Idade (anos)')
    ax.set_ylabel('Valores Normalizados (Média YL 30-49 anos = 1)')

    ax.set_xlim(0, 90)
    ax.set_ylim(bottom=0)

    limpar_eixos(ax)  # Aplica o visual clean (sem grades)

    # Legenda fora do gráfico para não poluir as curvas
    ax.legend(
        loc='upper left',
        fontsize=11,
        frameon=True,
        facecolor='white',  # Fundo totalmente branco
        edgecolor='#CCCCCC',  # Borda cinza neutra e bem clara
        framealpha=1.0,  # Sem transparência (opaco)
        borderpad=1.2,
        labelspacing=0.8
    )
    plt.tight_layout()

    nome_arq_comp = 'grafico_nta_comparativo_normalizado.png'
    plt.savefig(nome_arq_comp, dpi=300, transparent=False, facecolor='white', bbox_inches='tight')
    plt.close()
    print(f" -> Salvo com sucesso: {nome_arq_comp}")

print("\nMissão cumprida! Gráficos elegantes gerados.")
