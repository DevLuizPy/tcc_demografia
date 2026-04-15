import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Carregando os arquivos com todos os censos
arquivos_censo = ["censo_1960.csv", "censo_1970.csv", "censo_1980.csv", "censo_1991.csv",
                  "censo_2000.csv", "censo_2010.csv"]
anos = [1960, 1970, 1980, 1991, 2000, 2010]


# Função para formatação dos números em percentual no eixo X
def formatar_percentual(x, pos):
    return f'{abs(x):.0f}%'


# Função para a criação das faixas etárias (agora com "anos")
def definir_faixa_etaria(idade):
    if idade <= 4:
        return "0-4 anos"
    elif idade <= 9:
        return "5-9 anos"
    elif idade <= 14:
        return "10-14 anos"
    elif idade <= 19:
        return "15-19 anos"
    elif idade <= 24:
        return "20-24 anos"
    elif idade <= 29:
        return "25-29 anos"
    elif idade <= 34:
        return "30-34 anos"
    elif idade <= 39:
        return "35-39 anos"
    elif idade <= 44:
        return "40-44 anos"
    elif idade <= 49:
        return "45-49 anos"
    elif idade <= 54:
        return "50-54 anos"
    elif idade <= 59:
        return "55-59 anos"
    elif idade <= 64:
        return "60-64 anos"
    elif idade <= 69:
        return "65-69 anos"
    elif idade <= 74:
        return "70-74 anos"
    elif idade <= 79:
        return "75-79 anos"
    elif idade <= 84:
        return "80-84 anos"
    elif idade <= 89:
        return "85-89 anos"
    elif idade <= 94:
        return "90-94 anos"
    elif idade <= 99:
        return "95-99 anos"
    else:
        return "100+ anos"


# Criação da piramide etária para cada censo
for arquivo, ano in zip(arquivos_censo, anos):
    df = pd.read_csv(arquivo)

    # Removendo valores inválidos
    df = df[(df['AGE'] != 999) & (df['SEX'] != 9)]
    df['Faixa Etária'] = df['AGE'].apply(definir_faixa_etaria)

    piramide = df.groupby(['Faixa Etária', 'SEX'])['PERWT'].sum().reset_index()
    homens = piramide[piramide['SEX'] == 1].set_index('Faixa Etária')['PERWT']
    mulheres = piramide[piramide['SEX'] == 2].set_index('Faixa Etária')['PERWT']

    # Atualizando a lista para corresponder aos retornos da função
    todas_faixas = [
        "0-4 anos", "5-9 anos", "10-14 anos", "15-19 anos", "20-24 anos", "25-29 anos", "30-34 anos", "35-39 anos",
        "40-44 anos", "45-49 anos", "50-54 anos", "55-59 anos", "60-64 anos", "65-69 anos", "70-74 anos", "75-79 anos",
        "80-84 anos", "85-89 anos", "90-94 anos", "95-99 anos", "100+ anos"
    ]

    homens = homens.reindex(todas_faixas, fill_value=0)
    mulheres = mulheres.reindex(todas_faixas, fill_value=0)

    # Cálculo dos percentuais
    total_populacao = homens.sum() + mulheres.sum()
    homens_pct = (homens / total_populacao) * 100
    mulheres_pct = (mulheres / total_populacao) * 100

    # Invertendo valores dos homens para o gráfico (agora usando o percentual)
    homens_negativos_pct = -homens_pct

    # Configurações do gráfico
    plt.figure(figsize=(10, 6))

    # Plotando percentuais, mas mostrando os totais absolutos na legenda
    plt.barh(homens_negativos_pct.index, homens_negativos_pct, color='blue',
             label=f'Homens ({homens.sum():,.0f})'.replace(',', '.'))
    plt.barh(mulheres_pct.index, mulheres_pct, color='red', label=f'Mulheres ({mulheres.sum():,.0f})'.replace(',', '.'))

    plt.title(f'Estrutura Etária do Brasil (%) - {ano}')
    plt.xlabel('População (%)')
    plt.ylabel('Faixa Etária')
    plt.legend(title="Gênero", loc='upper right')
    plt.grid(axis='x', linestyle='--', alpha=0.7)

    # Aplicando o formatador de percentual
    plt.gca().get_xaxis().set_major_formatter(FuncFormatter(formatar_percentual))

    plt.tight_layout()
    plt.savefig(f'piramide_etaria_brasil_pct_{ano}.png', format='png')
    plt.show()
    plt.close()
