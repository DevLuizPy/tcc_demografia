import pandas as pd

import os

df = pd.read_excel(os.path.join(os.path.dirname(__file__), 'Produtividade_FGV.xlsx'), sheet_name="Produtividade - R$ 2021", header=None)

anos = pd.to_numeric(df.iloc[8:55, 0], errors='coerce')
produtividade = pd.to_numeric(df.iloc[8:55, 2], errors='coerce')

mask = anos.notna() & produtividade.notna()
anos = anos[mask]
produtividade = produtividade[mask]

df_prod = pd.DataFrame({'Ano': anos.astype(int), 'Prod': produtividade})
df_prod.set_index('Ano', inplace=True)

def calc_cagr(val_i, val_f, periods):
    return ( (val_f / val_i) ** (1/periods) - 1 ) * 100

periods_to_calc = [
    (1981, 2024),
    (1981, 1990),
    (1991, 2000),
    (2000, 2010),
    (2010, 2022)
]

for start, end in periods_to_calc:
    try:
        if start in df_prod.index and end in df_prod.index:
            val_start = df_prod.loc[start, 'Prod']
            val_end = df_prod.loc[end, 'Prod']
            num_years = end - start
            cagr = calc_cagr(val_start, val_end, num_years)
            print(f'CAGR {start}-{end}: {cagr:.2f}% (Inicial: R$ {val_start:.2f}, Final: R$ {val_end:.2f})')
        else:
            print(f'Anos não encontrados para o período {start}-{end}')
    except Exception as e:
        print(f'Erro no período {start}-{end}: {e}')
