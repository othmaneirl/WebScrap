import pandas as pd
import os

# Définir le fichier de sortie


# Liste pour stocker les DataFrames de chaque fichier CSV
dfs = []

# Obtenir une liste triée des fichiers CSV dans le répertoire
file_names = sorted([file_name for file_name in os.listdir() if file_name.endswith('.csv') and file_name.startswith('entreprises_')])

# Parcourir les fichiers CSV triés
for file_name in file_names:
    file_path = os.path.join(file_name)
    df = pd.read_csv(file_path, dtype=str)
    df['Tribunal'] = df['Tribunal'].str.replace('Tribunal de ', '')
    # Vérifiez et affichez les colonnes pour déboguer
    print(f"Fichier : {file_name}, Colonnes : {df.columns.tolist()}")

    # Ajoutez le DataFrame à la liste
    dfs.append(df)

# Combiner tous les DataFrames en un seul
combined_df = pd.concat(dfs, ignore_index=True)
# Enlever les lignes où la colonne 'Nom de l\'entreprise' contient 'N/A'
combined_df = combined_df[combined_df["Nom de l'entreprise"] != 'N/A']
# Vérifiez et affichez les colonnes du DataFrame combiné pour déboguer
print(f"Colonnes du DataFrame combiné : {combined_df.columns.tolist()}")

# Sauvegarder le DataFrame combiné dans un nouveau fichier CSV
combined_df.to_excel("Classement2020_ordo.xlsx", index=False)

