# Analise de dados com ydata_profiling
# Instalar a biblioteca ydata_profiling
# pip install ydata_profiling

import pandas as pd
from ydata_profiling import ProfileReport

# Carregar o arquivo csv
df = pd.read_csv('data.csv')
# Criar o relatorio
profile = ProfileReport(df, title='Profiling Report')
# Salvar o relatorio
profile.to_file('output.html')
