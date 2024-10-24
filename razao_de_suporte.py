import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import moviepy.editor as mp


df_censo_2010: DataFrame = pd.read_csv("C:\\Users\\gisel\\Documents\\ipumsi_00003.csv")


def razao_de_suporte():
    cidade: int = int(input('Digite o código da cidade'))
