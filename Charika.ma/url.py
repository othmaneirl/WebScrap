import pandas as pd

# Chemins vers les fichiers CSV
file1_path = '/Users/othmaneirhboula/WebScrap/1.csv'
file2_path = '/Users/othmaneirhboula/WebScrap/2.csv'
output_path = '/Users/othmaneirhboula/WebScrap/filtered_url.csv'

# Lire les fichiers CSV dans des dataframes
df1 = pd.read_csv(file1_path, header=None)
df2 = pd.read_csv(file2_path, header=None)

# Extraire les URLs des dataframes et les convertir en ensembles pour une comparaison rapide
urls_df1 = set(df1[0])
urls_df2 = set(df2[0])

# Retirer les URLs de df2 de df1
remaining_urls = urls_df1 - urls_df2

# Convertir le résultat en dataframe
result_df = pd.DataFrame(list(remaining_urls), columns=['URL'])

# Enregistrer le résultat dans un nouveau fichier CSV
result_df.to_csv(output_path, index=False)

print(f"Les URLs filtrées ont été enregistrées dans {output_path}")
