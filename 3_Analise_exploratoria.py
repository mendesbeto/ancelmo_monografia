import pandas as pd
import numpy as np

# --- Data Loading and Cleaning ---

try:
    header = pd.read_csv('Données.csv', nrows=0).columns
    year_col_name = header[0]
except FileNotFoundError:
    print("Error: 'Données.csv' not found.")
    exit()

try:
    df = pd.read_csv(
        'Données.csv',
        decimal=',',
        thousands='.'
    )
    df.rename(columns={year_col_name: 'ANNEE'}, inplace=True)
except FileNotFoundError:
    print("Error: 'Données.csv' not found. Make sure the file is in the correct directory.")
    exit()

df.loc[df['ANNEE'] > 2010, 'PNB'] = np.nan

# --- Create Proxy and Placeholder Variables ---

print("--- Creating Proxy and Placeholder Variables ---")

df['Receita_Tributaria_Proxy'] = (df['VA_SP'] * 0.10) + (df['VA_SS'] * 0.20) + (df['VA_ST'] * 0.18)

df['Esforco_Fiscal_Proxy'] = df.apply(
    lambda row: (row['Receita_Tributaria_Proxy'] / row['PIB_Nom']) if row['PIB_Nom'] > 0 else 0,
    axis=1
)

num_years = len(df)
df['Digitalizacao'] = np.linspace(10, 85, num_years).astype(int)
df['Teleprocedimento'] = np.linspace(5, 90, num_years).astype(int)
df['Competencias_Administrativas'] = np.linspace(20, 75, num_years).astype(int)

df['Digitalizacao'] += np.random.randint(-5, 6, size=num_years)
df['Teleprocedimento'] += np.random.randint(-5, 6, size=num_years)
df['Competencias_Administrativas'] += np.random.randint(-5, 6, size=num_years)

df[['Digitalizacao', 'Teleprocedimento', 'Competencias_Administrativas']] = df[['Digitalizacao', 'Teleprocedimento', 'Competencias_Administrativas']].clip(0, 100)

print("New proxy and placeholder columns added.")
print(df[['ANNEE', 'PIB_Nom', 'Receita_Tributaria_Proxy', 'Esforco_Fiscal_Proxy', 'Digitalizacao', 'Teleprocedimento', 'Competencias_Administrativas']].head())


# --- Save Combined Data ---
combined_file_path = 'dados_combinados.csv'
df.to_csv(combined_file_path, index=False)
print(f"\nCombined data with proxies saved to '{combined_file_path}'")
