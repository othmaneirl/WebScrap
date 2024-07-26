# Ce code permet d'extraire les informations utiles du site kerix.net avec bs4

# 2000 Sites scrapés en 15 minutes

import requests
from bs4 import BeautifulSoup
from lxml import etree
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

# Fonction pour séparer les chiffres et les lettres dans une chaîne
def splitchiffres(s):
    if s[0].isdigit():
        for i in range(len(s)):
            if s[i].isalpha():
                return s[:i], s[i:]
    else:
        for i in range(len(s)):
            if s[i].isdigit():
                return s[:i], s[i:]
    return s, ""

# Chemin vers le fichier CSV contenant les URL
lienscsv = 'Liens/Liens.csv'
df = pd.read_csv(lienscsv)
urls = df.values.tolist()

# Fonction pour extraire les informations d'une URL donnée
def extract_info(url):
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }  # headers pour imiter un navigateur
    response = session.get(f'https://www.kerix.net{url}', headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        dom = etree.HTML(str(soup))

        # Fonction pour extraire le texte d'un élément HTML avec BeautifulSoup
        def extract_text(tag, attrs):
            try:
                element = soup.find(tag, attrs)
                return element.text.strip() if element else "N/A"
            except Exception:
                return "N/A"

        # Fonction pour extraire le texte d'un élément HTML avec XPath
        def extract_xpath_text(path):
            try:
                return dom.xpath(path)[0].text.strip()
            except Exception:
                return "N/A"

        # Extraction des informations principales
        Entreprise = extract_text("h1", {"class": "card-title card-title-md mt-2"})
        Adresse = extract_text("p", {"class": "card-text"})
        Tel = extract_xpath_text('/html/body/div[2]/div[4]/div[2]/div/div[2]/div[1]/div[1]/div/p[1]')
        Tel2 = extract_xpath_text('/html/body/div[2]/div[4]/div[2]/div/div[2]/div[1]/div[1]/div/p[2]')
        Tel3 = extract_xpath_text('/html/body/div[2]/div[4]/div[2]/div/div[2]/div[1]/div[1]/div/p[3]')
        Fax = extract_text('div', {"id": "collapseExample2"})
        Infos = extract_text("div", {"class": "card-body pb-0"}).replace('\n', ' ')
        Dirigeant = extract_text("p", {"class": "par-list"}).replace('\n', ' ')
        Activite = extract_xpath_text('/html/body/div[2]/div[9]/div/div/div/p')

        # Extraction de l'URL du site
        try:
            Site = soup.find('a', class_='btn btn-down website').get('href')
        except Exception:
            Site = "N/A"

        # Extraction et nettoyage des informations supplémentaires
        try:
            valeurs = Infos.split('-')
            while len(valeurs) < 6:
                valeurs.append("N/A")

            Effectif, ChiffreAffaire, Capital, RC, Creation, ICE = valeurs
            Effectif = Effectif.replace('EFFECTIF :', '')
            ChiffreAffaire = ChiffreAffaire.replace('CHIFFRE D\'AFFAIRES :', '')
            Capital = Capital.replace('CAPITAL :', '').replace(' DH  ', '')
            temp, temp2, FormeJuridique, Capital = Capital.split(' ')
            RC = RC.replace('RC :', '').replace('  ', '')
            try:
                RC, VilleTribunal = RC.split(' ')
            except Exception:
                VilleTribunal = "N/A"
            Creation = Creation.replace('CREATION :', '')
            ICE = ICE.replace('ICE :', '')
        except Exception:
            Effectif = Infos
            ChiffreAffaire = "N/A"
            Capital = "N/A"
            RC = "N/A"
            VilleTribunal = "N/A"
            Creation = "N/A"
            ICE = "N/A"
            FormeJuridique = "N/A"

        # Extraction des produits
        try:
            produits = soup.find_all('div', class_='card-body pb-0')[0]
            produits = produits.text.replace('\n', ' ')
            i = 1
            while not produits.startswith(' PRODUIT') and i < len(soup.find_all('div', class_='card-body pb-0')):
                produits = soup.find_all('div', class_='card-body pb-0')[i].text.replace('\n', ' ')
                i += 1
            if produits.startswith('  ACTIVI'):
                produits = "N/A"
        except Exception:
            produits = "N/A"

        if produits != 'N/A':
            produits = produits[22:]

        # Extraction des sites supplémentaires
        sitesupp = ['https://kerix.net' + link['href'] for link in soup.find_all('a', href=True) if link['href'].startswith(url)]

        return [
            f'https://www.kerix.net{url}', Entreprise, Adresse, Tel, Tel2, Tel3, Fax, Site, Effectif, FormeJuridique,
            ChiffreAffaire, Capital, RC, VilleTribunal, Creation, ICE, Dirigeant, Activite, produits, sitesupp
        ]
    else:
        print(f"Erreur lors de la requête: {response.status_code}")
        return None

# Liste pour stocker les données
data = []

# Utiliser ThreadPoolExecutor pour exécuter les tâches en parallèle
with ThreadPoolExecutor(max_workers=4) as executor:
    results = executor.map(extract_info, [url[0] for url in urls[:2000]])
    for result in results:
        if result is not None:
            data.append(result)

# Conversion des données en DataFrame et export en fichier Excel
df = pd.DataFrame(data, columns=[
    'URL', 'Entreprise', 'Adresse', 'Tel', 'Tel2', 'Tel3', 'Fax', 'Site', 'Effectif', 'FormeJuridique',
    'ChiffreAffaire', 'Capital', 'RC', 'VilleTribunal', 'Creation', 'ICE', 'Dirigeant', 'Activite', 'Produits', 'SitesSupp'
])
df.to_excel('ScrapingKerix.xlsx', index=False)

# Affichage des produits
print(df['Produits'])

# Décommenter la ligne ci-dessous pour tester la fonction avec une URL spécifique
# print(extract_info('/fr/annuaire-entreprise/atlas-copco-maroc'))
