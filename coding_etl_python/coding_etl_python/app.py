import pandas as pd
from pydantic import ValidationError
import streamlit as st
from validador import Anuncio

# Função para validar os dados do CSV usando o modelo Pydantic


def validar_dados(df):
    erros = []
    # Iterar sobre as linhas do DataFrame
    for index, row in df.iterrows():
        try:
            anuncio = Anuncio(
                Organizador=row['Organizador'],
                Ano_Mes=row['Ano_Mes'],
                Dia_da_Semana=row['Dia_da_Semana'],
                Tipo_Dia=row['Tipo_Dia'],
                Objetivo=row['Objetivo'],
                Date=row['Date'],
                AdSet_name=row['AdSet_name'],
                Amount_spent=row['Amount_spent'],
                Link_clicks=row['Link_clicks'],
                Impressions=row['Impressions'],
                Conversions=row['Conversions'],
                Segmentação=row['Segmentação'],
                Tipo_de_Anúncio=row['Tipo_de_Anúncio'],
                Fase=row['Fase']
            )
        except ValidationError as e:
            erros.append((index, e.errors()))
    return erros


def main():
    # Configuração do Streamlit
    st.title("Validador de Anúncios")
    st.write("Faça o upload de um arquivo CSV para validar os dados dos anúncios.")


# Upload do arquivo CSV
uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")
if uploaded_file is not None:
    # Leitura do arquivo CSV
    df = pd.read_csv(uploaded_file)

    # Validação dos dados
    erros = validar_dados(df)

    if erros:
        st.write("Foram encontrados erros nos seguintes registros:")
        for index, error in erros:
            st.write(f"Linha {index + 1}: {error}")
    else:
        st.write("Todos os registros foram validados com sucesso!")

if __name__ == "__main__":
    main()
