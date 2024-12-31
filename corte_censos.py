import pandas as pd

arquivos_originais = ["censo_1960_original.csv", "censo_1970_original.csv", "censo_1980_original.csv",
                      "censo_1991_original.csv","censo_2000_original.csv", "censo_2010_original.csv",]

arquivos_novos = ["censo_1960.csv", "censo_1970.csv", "censo_1980.csv", "censo_1991.csv", "censo_2000.csv",
                  "censo_2010.csv"]

# Colunas que não serão utilizadas, logo serão removidas
colunas_remover = ["COUNTRY", "YEAR", "SAMPLE", "SERIAL", "HHWT", "PERNUM"]

# Criação da nova base de dados
for arquivo_original, arquivo_novo in zip(arquivos_originais, arquivos_novos):
    df = pd.read_csv(arquivo_original)
    df = df.drop(columns=colunas_remover, errors="ignore")
    df.to_csv(arquivo_novo, index=False)
