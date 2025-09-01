import pandas as pd
import numpy as np

# Number of samples
num_amostras = 200

# Set seed for reproducibility
np.random.seed(42)

# Generate data for the independent variables
# Let's assume these are indices from 0 to 100
digitalizacao = np.random.randint(0, 101, num_amostras)
teleprocedimento = np.random.randint(0, 101, num_amostras)
competencias_administrativas = np.random.randint(0, 101, num_amostras)

# Generate the dependent variable 'Esforço Fiscal'
# We'll create a positive correlation with the other variables + some noise
# The coefficients (0.3, 0.25, 0.4) are chosen to reflect a potential relative importance
esforco_fiscal = (0.3 * digitalizacao +
                  0.25 * teleprocedimento +
                  0.4 * competencias_administrativas +
                  np.random.normal(0, 10, num_amostras)) # Adding some noise

# Ensure the 'esforco_fiscal' is within a reasonable range (e.g., 0 to 100)
esforco_fiscal = np.clip(esforco_fiscal, 0, 100)

# Create a DataFrame
df = pd.DataFrame({
    'Digitalizacao': digitalizacao,
    'Teleprocedimento': teleprocedimento,
    'Competencias_Administrativas': competencias_administrativas,
    'Esforco_Fiscal': esforco_fiscal
})

# Save to CSV
df.to_csv('dados_fiscais.csv', index=False)

print("Arquivo 'dados_fiscais.csv' gerado com sucesso com {} amostras.".format(num_amostras))
