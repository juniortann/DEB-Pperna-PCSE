import pandas as pd

df = pd.read_csv(r'Chlor.csv', sep=';')

chlor = df.Chlor
temperature = df.Temperature
time = df.Time_month

chlor.mean()
chlor.hist()
chlor.median()
