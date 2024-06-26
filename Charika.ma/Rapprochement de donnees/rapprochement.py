import pandas as pd
import time

start_time = time.time()

# Charger les deux fichiers Excel
file1 = '/Users/othmaneirhboula/WebScrap/Charika.ma/Rapprochement de donnees/contrib.xlsx'
file2 = '/Users/othmaneirhboula/WebScrap/Charika.ma/Output/infos_entrprises.xlsx'

df1 = pd.read_excel(file1, dtype=str)
df2 = pd.read_excel(file2, dtype=str)

# Renommer les colonnes
df1.rename(columns={'RAISON_SOCIALE': 'Raison_Sociale', 'NUM_REGISTRE_COMMERCE': 'RC', 'LIBELLE_RC': 'Tribunal'}, inplace=True)
df2.rename(columns={'Nom de l\'entreprise': 'Nom_Entreprise'}, inplace=True)

# Vérifier l'existence des colonnes nécessaires
required_columns_df1 = ['RC', 'Tribunal']
required_columns_df2 = ['RC', 'Tribunal']

for col in required_columns_df1:
    if col not in df1.columns:
        raise KeyError(f"La colonne {col} n'existe pas dans df1")

for col in required_columns_df2:
    if col not in df2.columns:
        raise KeyError(f"La colonne {col} n'existe pas dans df2")

# Convertir les colonnes en chaînes de caractères
df1['RC'] = df1['RC'].astype(str)
df1['Tribunal'] = df1['Tribunal'].astype(str)
df2['RC'] = df2['RC'].astype(str)
df2['Tribunal'] = df2['Tribunal'].astype(str)

# Dictionnaire de correspondance des villes
city_mappings = {
    "Agadir": "AGADIR", "Alhoceima": "ALHOCEIMA", "Asilah": "ASILAH", "Azilal": "AZILAL",
    "Ben Ahmed": "BEN AHMED", "Ben Slimane": "BEN SLIMANE", "Benguerir": "BENGUERIR",
    "Beni Mellal": "BENI MELLAL", "Berkane": "BERKANE", "Berrechid": "BERRECHID",
    "Bouarfa": "BOUARFA", "Boujaad": "BOUJAAD", "Boulmane": "BOULMANE", "Casablanca": "CASABLANCA",
    "Chefchaouen": "CHEFCHAOUEN", "Eljadida": "ELJADIDA", "Errachidia": "ERRACHIDIA",
    "Essaouira": "ESSAOUIRA", "Essmara": "ES-SMARA", "Fes": "FES",
    "Fkih Ben Sallah": "FKIH BEN SALEH", "Guelmim": "GUELMIM", "Guercif": "GUERCIF",
    "Imintanoute": "IMINTANOUTE", "Inzegane": "INZEGANE", "Kasba Tadla": "KASBA TADLA",
    "Kelaa Sraghna": "KALAA-SRAGHNA", "Kenitra": "KENITRA", "Khemisset": "KHEMISSET",
    "Khenifra": "KHENIFRA", "Khouribga": "KHOURIBGA", "Ksar Kebir": "KSAR KEBIR",
    "Laayoune": "LAAYOUNE", "Larache": "LARACHE", "Marrakech": "MARRAKECH",
    "Meknes": "MEKNES", "Midelt": "MIDELT", "Mohammedia": "MOHAMEDIA",
    "Nador": "NADOR", "Ouarzazate": "OUARZAZATE", "Ouazzane": "OUAZZANE",
    "Oued Zem": "OUED ZEM", "Oujda": "OUJDA", "Rabat": "RABAT",
    "Rommani": "ROMANI", "Safi": "SAFI", "Sale": "SALE",
    "Sefrou": "SEFROU", "Settat": "SETTAT", "Sidi Bennour": "SIDI BENNOUR",
    "Sidi Kacem": "SIDI KACEM", "Sidi Slimane": "SIDI SLIMANE", "Souk Larbaa": "SOUK LARBAA",
    "Tanger": "TANGER", "Tantan": "TANTAN", "Taounat": "TAOUNATE",
    "Taroudant": "TAROUDANTE", "Tata": "TATA", "Taza": "TAZA",
    "Temara": "TEMARA", "Tetouan": "TETOUAN", "Tinghir": "TINGHIR",
    "Tiznit": "TIZNIT", "Youssoufia": "YOUSSOUFIA", "Zagora": "ZAGORA"
}

# Appliquer les mappings de ville à df2
df2['Tribunal'] = df2['Tribunal'].apply(lambda x: city_mappings.get(x, x))

# Créer la colonne Tribunal_RC
df1['Tribunal_RC'] = df1['Tribunal'] + '_' + df1['RC']
df2['Tribunal_RC'] = df2['Tribunal'] + '_' + df2['RC']

# Trouver les Tribunal_RC communs
common_tribunal_rcs = set(df1['Tribunal_RC']).intersection(set(df2['Tribunal_RC']))

# Filtrer les dataframes pour ne garder que les lignes avec Tribunal_RC communs
df1_filtered = df1[df1['Tribunal_RC'].isin(common_tribunal_rcs)]
df2_filtered = df2[df2['Tribunal_RC'].isin(common_tribunal_rcs)]


df2_non_matched = df2[~df2['Tribunal_RC'].isin(common_tribunal_rcs)]

# Sauvegarder les lignes non correspondantes dans un autre fichier Excel
df2_non_matched.to_excel('lignes_non_correspondantes.xlsx', index=False)

end_time = time.time()
print(f"Temps d'exécution : {end_time - start_time} secondes")
