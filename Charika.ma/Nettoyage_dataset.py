import pandas as pd

# Charger le fichier Excel
file_path = '/Users/othmaneirhboula/WebScrap/Charika.ma/Output/infos_clean2.xlsx'  # Remplacez par le chemin correct de votre fichier Excel
df = pd.read_excel(file_path, dtype={'ICE': str})
# Supprimer les espaces en début et fin de toutes les cellules
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Assurer que les coordonnées géographiques ont un format cohérent
def format_coordinates(coord):
    try:
        lat, lon = map(float, coord.split(' : '))
        return f"{lat:.6f}, {lon:.6f}"
    except:
        return coord

df['Coordonnees geographiques'] = df['Coordonnees geographiques'].apply(format_coordinates)

# Garder seulement le nom.csv de la ville dans la colonne 'Tribunal'
df['Tribunal'] = df['Tribunal'].apply(lambda x: x.replace('Tribunal de ', '') if isinstance(x, str) else x)

# Enlever les lignes où la colonne 'Nom de l\'entreprise' contient 'N/A'
df = df[df['Nom de l\'entreprise'] != 'N/A']

# Enlever les lignes où la colonne ICE contient 'Afficher l'ICE'

# Enregistrer les données nettoyées dans un nouveau fichier Excel
cleaned_file_path = '/Users/othmaneirhboula/WebScrap/Charika.ma/Output/infos_entrprises.xlsx'
df.to_excel(cleaned_file_path, index=False)

print(f"Les données nettoyées ont été enregistrées dans {cleaned_file_path}")
