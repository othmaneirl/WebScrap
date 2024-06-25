import pandas as pd

file2 = '/Users/othmaneirhboula/WebScrap/Charika.ma/Output/infos_entrprises.xlsx'
file1 = '/Users/othmaneirhboula/WebScrap/Charika.ma/Rapprochement de donnees/contrib.xlsx'

df1 = pd.read_excel(file1, dtype=str)
df2 = pd.read_excel(file2, dtype=str)

df1.rename(columns={'RAISON_SOCIALE': 'Raison_Sociale', 'NUM_REGISTRE_COMMERCE': 'RC', 'LIBELLE_RC': 'Tribunal'}, inplace=True)
df2.rename(columns={'Nom de l\'entreprise': 'Nom_Entreprise'}, inplace=True)

required_columns_df1 = [ 'RC', 'Tribunal']
required_columns_df2 = [ 'RC', 'Tribunal']

for col in required_columns_df1:
    if col not in df1.columns:
        raise KeyError(f"La colonne {col} n'existe pas dans df1")

for col in required_columns_df2:
    if col not in df2.columns:
        raise KeyError(f"La colonne {col} n'existe pas dans df2")


df1['RC'] = df1['RC'].astype(str)
df1['Tribunal'] = df1['Tribunal'].astype(str)
df2['RC'] = df2['RC'].astype(str)
df2['Tribunal'] = df2['Tribunal'].astype(str)

city_mappings = {
    "Agadir": "AGADIR",
    "Alhoceima": "ALHOCEIMA",
    "Asilah": "ASILAH",
    "Azilal": "AZILAL",
    "Ben Ahmed": "BEN AHMED",
    "Ben Slimane": "BEN SLIMANE",
    "Benguerir": "BENGUERIR",
    "Beni Mellal": "BENI MELLAL",
    "Berkane": "BERKANE",
    "Berrechid": "BERRECHID",
    "Bouarfa": "BOUARFA",
    "Boujaad": "BOUJAAD",
    "Boulmane": "BOULMANE",
    "Casablanca": "CASABLANCA",
    "Chefchaouen": "CHEFCHAOUEN",
    "Eljadida": "ELJADIDA",
    "Errachidia": "ERRACHIDIA",
    "Essaouira": "ESSAOUIRA",
    "Essmara": "ES-SMARA",
    "Fes": "FES",
    "Fkih Ben Sallah": "FKIH BEN SALEH",
    "Guelmim": "GUELMIM",
    "Guercif": "GUERCIF",
    "Imintanoute": "IMINTANOUTE",
    "Inzegane": "INZEGANE",
    "Kasba Tadla": "KASBA TADLA",
    "Kelaa Sraghna": "KALAA-SRAGHNA",
    "Kenitra": "KENITRA",
    "Khemisset": "KHEMISSET",
    "Khenifra": "KHENIFRA",
    "Khouribga": "KHOURIBGA",
    "Ksar Kebir": "KSAR KEBIR",
    "Laayoune": "LAAYOUNE",
    "Larache": "LARACHE",
    "Marrakech": "MARRAKECH",
    "Meknes": "MEKNES",
    "Midelt": "MIDELT",
    "Mohammedia": "MOHAMEDIA",
    "Nador": "NADOR",
    "Ouarzazate": "OUARZAZATE",
    "Ouazzane": "OUAZZANE",
    "Oued Zem": "OUED ZEM",
    "Oujda": "OUJDA",
    "Rabat": "RABAT",
    "Rommani": "ROMANI",
    "Safi": "SAFI",
    "Sale": "SALE",
    "Sefrou": "SEFROU",
    "Settat": "SETTAT",
    "Sidi Bennour": "SIDI BENNOUR",
    "Sidi Kacem": "SIDI KACEM",
    "Sidi Slimane": "SIDI SLIMANE",
    "Souk Larbaa": "SOUK LARBAA",
    "Tanger": "TANGER",
    "Tantan": "TANTAN",
    "Taounat": "TAOUNATE",
    "Taroudant": "TAROUDANTE",
    "Tata": "TATA",
    "Taza": "TAZA",
    "Temara": "TEMARA",
    "Tetouan": "TETOUAN",
    "Tinghir": "TINGHIR",
    "Tiznit": "TIZNIT",
    "Youssoufia": "YOUSSOUFIA",
    "Zagora": "ZAGORA"
}


df2['Tribunal'] = df2['Tribunal'].apply(lambda x: city_mappings.get(x, x))

df1['Tribunal_RC'] = df1['Tribunal'] + '_' + df1['RC']
df2['Tribunal_RC'] = df2['Tribunal'] + '_' + df2['RC']

common_tribunal_rcs = set(df1['Tribunal_RC']).intersection(set(df2['Tribunal_RC']))
df1_filtered = df1[df1['Tribunal_RC'].isin(common_tribunal_rcs)]
df2_filtered = df2[df2['Tribunal_RC'].isin(common_tribunal_rcs)]
merged_df = pd.merge(df1_filtered, df2_filtered, how='right', on=['Tribunal_RC'])
print(merged_df.head())
output_path = 'Rapprochement de donnees/donnees_rapprochees.xlsx'
merged_df.to_excel(output_path, index=False)
print(f"Rapprochement terminé et sauvegardé dans {output_path}")