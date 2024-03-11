import streamlit as st
import pandas as pd
import plotly.express as px

def carregar_dados(arquivo_excel):
    df = pd.read_excel(arquivo_excel)
    return df

def calcular_lucro_total(dados):
    if 'VALOR' in dados.columns and 'QUANTIDADE' in dados.columns:
        dados['LUCRO'] = dados['VALOR'] * dados['QUANTIDADE']
        return dados
    else:
        st.warning("Não é possível calcular o lucro total, pois as colunas 'VALOR' e 'QUANTIDADE' não estão presentes.")
        return dados

def main():
    st.title('Dashboard com Streamlit e Excel')

    # Permitir que o usuário selecione o arquivo Excel
    arquivo_excel = st.file_uploader("Selecione o arquivo Excel", type=["xlsx"])

    if arquivo_excel:
        # Carregar dados do Excel
        dados = carregar_dados(arquivo_excel)

        # Filtro de valores para colunas específicas
        colunas_filtro = st.multiselect('Selecione as colunas para filtro', dados.columns)
        if colunas_filtro:
            for coluna in colunas_filtro:
                valores_unicos = dados[coluna].dropna().unique()
                valor_selecionado = st.selectbox(f'Selecione um valor para {coluna}', valores_unicos)
                dados = dados[dados[coluna] == valor_selecionado]

        # Remover células vazias
        dados = dados.dropna()

        # Calcular lucro total
        dados = calcular_lucro_total(dados)

        # Mostrar os dados filtrados
        st.subheader('Visualização dos Dados Filtrados e Sem Células Vazias')
        st.dataframe(dados)

        # Adicionar gráfico de barras
        if not dados.empty:
            st.subheader('Gráfico de Barras')
            fig_bar = px.bar(dados, x=dados.columns[0], y=dados.columns[2], title=f'{dados.columns[2]} por {dados.columns[0]}')
            st.plotly_chart(fig_bar)

        # Adicionar gráfico de dispersão
        if len(dados.columns) >= 4:
            st.subheader('Gráfico de Dispersão')
            fig_scatter = px.scatter(dados, x=dados.columns[1], y=dados.columns[2], color=dados.columns[0], title=f'Dispersão {dados.columns[1]} x {dados.columns[2]}')
            st.plotly_chart(fig_scatter)

        # Exibir lucro total se as colunas 'VALOR' e 'QUANTIDADE' estiverem presentes
        if 'LUCRO' in dados.columns:
            st.subheader(f'Lucro Total: R$ {dados["LUCRO"].sum():.2f}')

if __name__ == '__main__':
    main()
