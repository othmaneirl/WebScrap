# Description: Ce script permet de générer les liens des pages des articles de chaque boutique.
import pandas as pd
import csv

boutiquescsv = '/Users/othmaneirhboula/WebScrap/Avito/Liens.csv/LiensBoutiquesArticles.csv'
df = pd.read_csv(boutiquescsv)
listeboutiques = df.values.tolist()

nouveaux_liens = []

for liens, num_articles in listeboutiques:
    if num_articles != "0 Articles":
        id_boutique = liens.split('id=')[1]
        num_articles_int = int(num_articles.split()[0])
        num_pages = (num_articles_int // 35) + 1
        for i in range(num_pages):
            nouveau_liens = f'https://www.avito.ma/fr/boutique?o={i + 1}&id={id_boutique}'
            nouveaux_liens.append([nouveau_liens])

with open('/Users/othmaneirhboula/WebScrap/Avito/Liens/LiensArticlesPages.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['URL'])
    writer.writerows(nouveaux_liens)

print("Les liens ont été enregistrés dans le fichier CSV.")
