import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

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


# Função para a criação das faixas etárias
def definir_faixa_etaria(idade):
    if idade <= 4:
        return "0-4"
    elif idade <= 9:
        return "5-9"
    elif idade <= 14:
        return "10-14"
    elif idade <= 19:
        return "15-19"
    elif idade <= 24:
        return "20-24"
    elif idade <= 29:
        return "25-29"
    elif idade <= 34:
        return "30-34"
    elif idade <= 39:
        return "35-39"
    elif idade <= 44:
        return "40-44"
    elif idade <= 49:
        return "45-49"
    elif idade <= 54:
        return "50-54"
    elif idade <= 59:
        return "55-59"
    elif idade <= 64:
        return "60-64"
    elif idade <= 69:
        return "65-69"
    elif idade <= 74:
        return "70-74"
    elif idade <= 79:
        return "75-79"
    elif idade <= 84:
        return "80-84"
    elif idade <= 89:
        return "85-89"
    elif idade <= 94:
        return "90-94"
    elif idade <= 99:
        return "95-99"
    else:
        return "100+"


# Criação da piramide etária para cada censo
for arquivo, ano in zip(arquivos_censo, anos):
    df = pd.read_csv(arquivo)

    # Removendo valores inválidos
    df = df[(df['AGE'] != 999) & (df['SEX'] != 9)]
    df['Faixa Etária'] = df['AGE'].apply(definir_faixa_etaria)

    piramide = df.groupby(['Faixa Etária', 'SEX'])['PERWT'].sum().reset_index()
    homens = piramide[piramide['SEX'] == 1].set_index('Faixa Etária')['PERWT']
    mulheres = piramide[piramide['SEX'] == 2].set_index('Faixa Etária')['PERWT']

    todas_faixas = [
        "0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39",
        "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "75-79",
        "80-84", "85-89", "90-94", "95-99", "100+"
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
    plt.close()  # Boa prática para liberar memória ao gerar múltiplos gráficos
