import pandas as pd


LiensCSV= '/Users/othmaneirhboula/WebScrap/LEI/Liens/Liens.csv'
df = pd.read_csv(LiensCSV)  #lire le csv
urls = df.values.tolist()
Liens= []
for url in urls:
    Liens.append('https://lei.info'+url[0])   #ajouter le lien de base à chaque lien
Liens=set(Liens)
Liens=list(Liens)
df = pd.DataFrame(Liens, columns=['URL'])
df.to_csv('Liens.csv', index=False)   #enregistrer les liens dans un fichier csv
print(df)