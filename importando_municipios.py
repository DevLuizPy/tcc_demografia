import pandas as pd
import tabula
import pandas

# tabula.convert_into("geolevel2 - Brasil.pdf", "municipios.csv", output_format="csv", pages="all")


df_municipios = pd.read_csv("municipios.csv")
print(df_municipios)
