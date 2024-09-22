import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import moviepy.editor as mp

df_homens: DataFrame = pd.read_excel('C:\\Users\\gisel\\OneDrive\\Documentos\\Tcc-demografia.xlsm', sheet_name='Brazil_Homens')
df_mulheres: DataFrame = pd.read_excel('C:\\Users\\gisel\\OneDrive\\Documentos\\Tcc-demografia.xlsm', sheet_name='Brazil_Mulheres')


png_files = []


df_homens.drop('Ano', axis=1, inplace=True)
df_mulheres.drop('Ano', axis=1, inplace=True)


def percentual(x, pos):
    x = abs(x)
    return f'{x:.0f}%'


# Loop sobre os anos
for ano in df_homens.index:
    plt.figure(figsize=(10, 8))

    total_populacao = df_homens.loc[ano].sum() + df_mulheres.loc[ano].sum()
    # Dados para o ano específico
    populacao_homens: DataFrame = -df_homens.loc[ano] / total_populacao * 100
    populacao_mulheres: DataFrame = df_mulheres.loc[ano] / total_populacao * 100
    faixa_etaria = df_homens.columns
    # Plotar as barras
    plt.barh(faixa_etaria, populacao_homens, color='red', label='Homens')
    plt.barh(faixa_etaria, populacao_mulheres, color='blue', label='Mulheres')

    # Configurar o gráfico
    plt.xlabel('População (%)')
    plt.ylabel('Faixa Etária')
    ano_1 = 2024 + ano
    plt.title(f'Estrutura Etária em {ano_1} (%)')
    plt.legend()

    # Aplicar o formato percentual ao eixo X
    plt.gca().xaxis.set_major_formatter(FuncFormatter(percentual))

    filename = f"estrutura_etaria_{ano_1}.png"
    plt.savefig(filename)
    png_files.append(filename)
    plt.show()
    plt.close()

clip = mp.ImageSequenceClip(png_files, fps=2)
clip.write_videofile('estrutura_etaria.mp4', codec='libx264')
