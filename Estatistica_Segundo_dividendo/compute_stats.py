import pandas as pd

df = pd.read_excel('Base_de_Dados_FMI_2.xlsx')
years = [col for col in df.columns if isinstance(col, int)]
res = []

for c in ['Brazil', 'Chile', 'Korea']:
    for s, sn in [('Total investment', 'Investimento Total'), ('Gross national savings', 'Poupança Agregada')]:
        row = df[(df['Country'] == c) & (df['Subject Descriptor'] == s)]
        if not row.empty:
            # Pega os valores e converte. Se houver erro de escala (multiplicado por 1000), dividimos por 1000.
            v = pd.to_numeric(row[years].iloc[0], errors='coerce').dropna()
            
            # Ajuste de escala para os dados do FMI (dividindo por 1000 caso tenham vindo sem decimais corretos)
            if v.mean() > 1000:
                v = v / 1000
                
            res.append(f"{c} - {sn}:\n  Média: {v.mean():.2f}%\n  Mediana: {v.median():.2f}%\n  Desvio Padrão: {v.std():.2f}%")

print('\n'.join(res))
