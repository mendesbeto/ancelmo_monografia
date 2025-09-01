import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.title("Análise Exploratória de Dados Macroeconômicos")

st.write("Esta página apresenta uma análise dos dados macroeconômicos carregados do arquivo `Données.csv`.")

# Load the combined data
try:
    df = pd.read_csv('dados_combinados.csv')
except FileNotFoundError:
    st.error("Arquivo 'dados_combinados.csv' não encontrado. Por favor, execute o script 'analise_exploratoria.py' primeiro.")
    st.stop()

st.header("Visualização dos Dados Brutos")
st.dataframe(df)

st.header("Evolução do PIB Nominal (PIB_Nom)")

# Create the plot
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df['ANNEE'], df['PIB_Nom'], marker='o', linestyle='-')
ax.set_xlabel("Ano")
ax.set_ylabel("PIB Nominal")
ax.set_title("Evolução do PIB Nominal (1994-2024)")
ax.grid(True)

# Display the plot
st.pyplot(fig)

st.write("""
**Observação:** O gráfico mostra o crescimento do PIB Nominal ao longo do tempo.
Podemos observar períodos de crescimento mais rápido e outros de estagnação.
Esta visualização é o primeiro passo para entender o contexto econômico.
""")

st.header("Evolução da População Total (Ption_tot)")

fig2, ax2 = plt.subplots(figsize=(12, 6))
ax2.plot(df['ANNEE'], df['Ption_tot'], marker='o', linestyle='-', color='green')
ax2.set_xlabel("Ano")
ax2.set_ylabel("População Total")
ax2.set_title("Evolução da População Total (1994-2024)")
ax2.grid(True)
st.pyplot(fig2)

st.header("Evolução da Inflação (IPC)")

fig3, ax3 = plt.subplots(figsize=(12, 6))
ax3.plot(df['ANNEE'], df['IPC'], marker='o', linestyle='-', color='red')
ax3.set_xlabel("Ano")
ax3.set_ylabel("Inflação (IPC)")
ax3.set_title("Evolução da Inflação (IPC) (1994-2024)")
ax3.grid(True)
st.pyplot(fig3)

st.header("Análise da População Feminina")

# Calculate the percentage of the female population
df['Percent_Feminina'] = (df['Ption_Fim'] / df['Ption_tot']) * 100

st.write("### Proporção da População Feminina ao Longo do Tempo")

fig4, ax4 = plt.subplots(figsize=(12, 6))
ax4.plot(df['ANNEE'], df['Percent_Feminina'], marker='o', linestyle='-', color='purple')
ax4.set_xlabel("Ano")
ax4.set_ylabel("População Feminina (%)")
ax4.set_title("Proporção da População Feminina (1994-2024)")
ax4.grid(True)
ax4.set_ylim(45, 55) # Set y-axis limits to better visualize small changes
st.pyplot(fig4)
st.write("""
**Observação:** A proporção da população feminina tem se mantido relativamente estável, em torno de 51%.
""")


st.write("### Comparação do Crescimento Populacional por Gênero")
fig5, ax5 = plt.subplots(figsize=(12, 6))
ax5.plot(df['ANNEE'], df['Ption_Fim'], marker='o', linestyle='-', label='Feminino')
ax5.plot(df['ANNEE'], df['Ption_Masc'], marker='x', linestyle='--', label='Masculino')
ax5.set_xlabel("Ano")
ax5.set_ylabel("População")
ax5.set_title("Crescimento da População por Gênero (1994-2024)")
ax5.legend()
ax5.grid(True)
st.pyplot(fig5)
st.write("""
**Observação:** O gráfico mostra o crescimento contínuo de ambas as populações, feminina e masculina, ao longo do tempo, com a população feminina consistentemente maior que a masculina.
""")
