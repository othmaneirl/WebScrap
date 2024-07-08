import polars as pl

file1_path = 'population_with_Tribunal_RC.xlsx'
file2_path = 'infos_entrprises_with_Tribunal_RC.xlsx'
output_path = 'donnees_rapprochees.xlsx'

# Lire les fichiers Excel
df1 = pl.read_excel(file1_path)
df2 = pl.read_excel(file2_path)

# Extraire les colonnes 'ICE'
column1 = df1['Tribunal_RC']
column2 = df2['Tribunal_RC']

# Identifier les valeurs communes et fusionner les dataframes
merged = df1.join(df2, on='Tribunal_RC', how='inner')

# Écrire le résultat dans un nouveau fichier Excel
merged.write_excel(output_path)

print(f"Fichier Excel créé : {output_path}")
