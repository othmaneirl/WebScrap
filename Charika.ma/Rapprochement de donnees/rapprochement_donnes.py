import pandas as pd
from rapidfuzz import process, fuzz
from tqdm import tqdm

file1 = '/Users/othmaneirhboula/Desktop/df1.xlsx'
file2 = '/Users/othmaneirhboula/Desktop/df2.xlsx'

df1 = pd.read_excel(file1)
df2 = pd.read_excel(file2)


def fuzzy_merge(df_1, df_2, keys, threshold=80, limit=2):
    """
    Rapprocher deux dataframes sur la base de multiples paires de clés floues.

    :param df_1: Premier DataFrame
    :param df_2: Second DataFrame
    :param keys: Liste de tuples contenant les paires de clés (clé1, clé2)
    :param threshold: Seuil de similarité pour considérer un match
    :param limit: Nombre maximum de correspondances potentielles à examiner
    :return: DataFrame avec les correspondances trouvées
    """

    def get_matches(x, s):
        matches = process.extract(x, s, limit=limit, scorer=fuzz.WRatio)
        return [match[0] for match in matches if match[1] >= threshold]

    for key1, key2 in keys:
        s = df_2[key2].tolist()
        tqdm.pandas(desc=f"Traitement de {key1} et {key2}")
        df_1[f'matches_{key1}_{key2}'] = df_1[key1].progress_apply(lambda x: get_matches(x, s))
        df_1[f'best_match_{key1}_{key2}'] = df_1[f'matches_{key1}_{key2}'].apply(lambda x: ','.join(x) if x else None)

    return df_1


# Liste des paires de colonnes pour le rapprochement
keys_to_match = [
    ('Nom de l\'entrepriseRC','NOM_PRENOM_RSNUM_REG_COM')
]

# Rapprochement flou entre les colonnes spécifiées
print("Début du rapprochement...")
merged_df = fuzzy_merge(df2, df1, keys_to_match)

# Sauvegarder le résultat dans un nouveau fichier Excel
print("Sauvegarde du résultat...")
merged_df.to_excel('merged_output.xlsx', index=False)

print("Rapprochement terminé et sauvegardé dans 'merged_output.xlsx'")