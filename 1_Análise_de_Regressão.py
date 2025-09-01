import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np

st.title('Análise de Determinantes de Esforço Fiscal')

st.header('Introdução')
st.write("""
Esta aplicação analisa os determinantes do esforço fiscal, utilizando uma combinação de dados macroeconômicos reais e variáveis proxy para digitalização, teleprocedimento e competências administrativas.
""")

# Data loading
st.header('Visualização dos Dados Combinados')

@st.cache_data
def carregar_dados():
    try:
        df = pd.read_csv('dados_combinados.csv')
        return df
    except FileNotFoundError:
        st.error("Arquivo 'dados_combinados.csv' não encontrado. Por favor, execute o script 'analise_exploratoria.py' primeiro.")
        return None

df = carregar_dados()

if df is not None:
    # Fill NA values with the mean of the column for the regression
    df.fillna(df.mean(), inplace=True)

    st.dataframe(df)

    # Regression Analysis
    st.header('Análise de Regressão')
    st.write("Aqui, usamos um modelo de regressão linear para testar nossas hipóteses, controlando por variáveis macroeconômicas.")

    # Define features (X) and target (y)
    features = ['Digitalizacao', 'Teleprocedimento', 'Competencias_Administrativas', 'PIB_PC', 'IPC']
    target = 'Esforco_Fiscal_Proxy'

    X = df[features]
    y = df[target]

    # Train the model
    model = LinearRegression()
    model.fit(X, y)

    # Display results
    st.subheader('Coeficientes do Modelo')
    st.write("Os coeficientes representam o impacto de cada variável no Esforço Fiscal.")

    coefs = pd.DataFrame(model.coef_, X.columns, columns=['Coeficiente'])
    st.dataframe(coefs)

    st.write("""
    **Interpretação dos Coeficientes:**
    - O modelo agora mostra o efeito de cada variável de pesquisa *mantendo as variáveis macroeconômicas constantes*.
    """)

    st.subheader('Intercepto do Modelo')
    st.write(f"O intercepto do modelo é: {model.intercept_:.4f}")

    st.subheader("Fórmula do Modelo")
    formula = f"Esforco\_Fiscal = {model.intercept_:.4f}"
    for i, feature in enumerate(features):
        # Add a plus or minus sign based on the coefficient's value
        sign = "+" if model.coef_[i] >= 0 else "-"
        formula += f" {sign} {abs(model.coef_[i]):.4f} \times {feature.replace('_', '\_')}"
    st.latex(formula)


    # Visualizations
    st.header('Visualizações Gráficas')
    st.write("Gráficos de dispersão para visualizar a relação entre cada variável e o Esforço Fiscal.")

    # Only plot our main research variables
    main_features = ['Digitalizacao', 'Teleprocedimento', 'Competencias_Administrativas']
    for feature in main_features:
        fig, ax = plt.subplots()
        ax.scatter(df[feature], df[target], alpha=0.5)
        ax.set_xlabel(feature)
        ax.set_ylabel(target)
        ax.set_title(f'{target} vs. {feature}')
        st.pyplot(fig)

    # Interactive Prediction
    st.sidebar.header('Faça sua Previsão')
    st.sidebar.write("Ajuste os valores para prever o Esforço Fiscal. Os valores macroeconômicos serão fixados na média.")

    digitalizacao_input = st.sidebar.slider('Nível de Digitalização', 0, 100, 50)
    teleprocedimento_input = st.sidebar.slider('Nível de Teleprocedimento', 0, 100, 50)
    competencias_input = st.sidebar.slider('Nível de Competências Administrativas', 0, 100, 50)
    
    # Use mean values for the control variables in the prediction
    pib_pc_mean = df['PIB_PC'].mean()
    ipc_mean = df['IPC'].mean()

    input_data = np.array([[digitalizacao_input, teleprocedimento_input, competencias_input, pib_pc_mean, ipc_mean]])
    prediction = model.predict(input_data)

    st.sidebar.subheader('Resultado da Previsão')
    st.sidebar.metric(label="Esforço Fiscal Previsto (Proxy)", value=f"{prediction[0]:.4f}")
    st.sidebar.caption(f"Cálculo feito com PIB per capita de {pib_pc_mean:.2f} e IPC de {ipc_mean:.2f} (valores médios).")
