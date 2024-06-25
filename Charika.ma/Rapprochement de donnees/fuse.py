import pandas as pd

file1_path = 'population_with_Tribunal_RC.xlsx'
file2_path = 'infos_entrprises_with_Tribunal_RC.xlsx'
output_path = 'donnees_rapprochees.xlsx'

# Lire les fichiers Excel
df1 = pd.read_excel(file1_path,dtype=str)
df2 = pd.read_excel(file2_path,dtype=str)

# Extraire les colonnes 'ICE'
column1 = df1['Tribunal_RC']
column2 = df2['Tribunal_RC']

# Identifier les valeurs communes
merged= pd.merge(df1, df2, on='Tribunal_RC', how='inner')

# Écrire le résultat dans un nouveau fichier Excel
merged.to_excel(output_path, index=False,)

print(f"Fichier Excel créé : {output_path}")
