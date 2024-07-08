import polars as pl

# Lire le fichier Excel sans spécifier le type de données
df1 = pl.read_excel('/Users/othmaneirhboula/WebScrap/Charika.ma/Output/infos_entrprises.xlsx')
df2 = pl.read_excel('/Users/othmaneirhboula/Desktop/simpl.xlsx')

# Limiter à 200 lignes pour le traitement
df1 = df1.head(200)
df2 = df2.head(200)

# Convertir la colonne 'RC' en chaîne de caractères après la lecture
df1 = df1.with_columns([
    pl.col('RC').cast(pl.Utf8).alias('rc_normalise')
])

df2 = df2.with_columns([
    pl.col('NUM_REG_COM').cast(pl.Utf8).alias('rc_normalise')
])

# Normalisation des colonnes pour le rapprochement
def normalize_column(column):
    return column.str.to_lowercase().str.replace_all(r'\W+', '')

df1 = df1.with_columns([
    normalize_column(pl.col('Nom de l\'entreprise')).alias('nom_normalise'),
    normalize_column(pl.col('Adresse')).alias('adresse_normalise'),
    pl.col('rc_normalise')
])

df2 = df2.with_columns([
    normalize_column(pl.col('NOM_PRENOM_RS')).alias('nom_normalise'),
    normalize_column(pl.col('ADR_IMPOSITION')).alias('adresse_normalise'),
    pl.col('rc_normalise')
])

from fuzzywuzzy import fuzz, process

# Fonction pour effectuer le rapprochement flou avec plusieurs colonnes
def fuzzy_match(row, df1, threshold=40):
    scores = []
    for col in ['nom_normalise', 'adresse_normalise', 'rc_normalise']:
        match = process.extractOne(row[col], df1[col].to_list(), scorer=fuzz.token_sort_ratio)
        if match:
            scores.append(match[1])
    avg_score = sum(scores) / len(scores) if scores else 0
    if avg_score >= threshold:
        return match[2]  # Retourne l'index de la meilleure correspondance
    return None

# Rapprochement flou avec barre de progression
df2 = df2.with_columns(pl.struct(df2.columns).apply(lambda row: fuzzy_match(row, df1)).alias('match_index'))

# Filtrer les correspondances trouvées
matched_df2 = df2.filter(pl.col('match_index').is_not_null())
matched_df2 = matched_df2.with_columns(pl.col('match_index').cast(pl.Int64))

# Ajouter les informations des correspondances du fichier 1 dans le fichier 2
matched_df1 = df1.filter(pl.col('match_index').is_in(matched_df2['match_index']))

# Concaténer les DataFrames
matched_df = pl.concat([matched_df2, matched_df1], how='horizontal')

# Sauvegarde du fichier de résultats
matched_df_path = 'matched_results.xlsx'
matched_df.write_excel(matched_df_path)
