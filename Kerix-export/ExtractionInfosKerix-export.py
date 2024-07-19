#Ce code permet d'extraire les infos utiles de kerix-export.net avec bs4

#2000 Sites Scrapés en 5 minutes

import requests
from bs4 import BeautifulSoup
from lxml import etree #permet de localiser les elements par xpath
import pandas as pd
from concurrent.futures import ThreadPoolExecutor  #permet d'executer les fonctions en parallèle pour accélerer l'execution

def splitchiffres(s):  #permet de split une chaine de caractères en une chaine contenant les chiffres et une les lettres
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
lienscsv = '/Users/othmaneirhboula/WebScrap/Kerix-export/Liens/Liens.csv'
df = pd.read_csv(lienscsv)
urls = df.values.tolist()

def extract_info(url):
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = session.get(f'https://www.kerix-export.net{url}', headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        dom = etree.HTML(str(soup))
        # Utilisation d'une fonction pour réduire la répétition du code pour extraire le texte avec BeautifulSoup
        def extract_text(tag, attrs):
            try:
                element = soup.find(tag, attrs)
                return element.text.strip() if element else "N/A"
            except Exception:
                return "N/A"

        # Utilisation d'une fonction pour réduire la répétition du code pour extraire le texte avec XPath
        def extract_xpath_text(path):
            try:
                return dom.xpath(path)[0].text.strip()
            except Exception:
                return "N/A"


        # Extraction des differents élements demandés
        Entreprise = extract_text("h1", {"class": "card-title card-title-md mt-2"})
        Adresse = extract_text("p", {"class": "card-text"})
        Tel = extract_xpath_text('/html/body/div[4]/div[4]/div/div/div/div[2]/div[2]/div/p[1]')
        Tel2 = extract_xpath_text('/html/body/div[4]/div[4]/div/div/div/div[2]/div[2]/div/p[2]')
        Tel3 = extract_xpath_text('/html/body/div[4]/div[4]/div/div/div/div[2]/div[2]/div/p[3]')
        Fax = extract_text('div', {"id": "collapseExample2"})
        try:
            Site = soup.find('a', class_='btn btn-down website').get('href')
        except Exception:
            Site = "N/A"
        Effectif = extract_xpath_text('/html/body/div[4]/div[5]/div/div/div[1]/span')
        try:
            Effectif=Effectif.split(': ')[1].replace('\n', '')  #traitement de la chaine de caractères pour ne garder que la valeur utile
        except:
            Effectif = Effectif

        Capital = extract_xpath_text('/html/body/div[4]/div[5]/div/div/div[3]/span')
        try:
            Capital= Capital.split(': ')[1] #traitement de la chaine de caractères pour ne garder que la valeur utile
        except:
            Capital = Capital
        CA = extract_xpath_text('/html/body/div[4]/div[5]/div/div/div[2]/span')
        RC = extract_xpath_text('/html/body/div[4]/div[5]/div/div/div[4]/span')
        Creation = extract_xpath_text('/html/body/div[4]/div[5]/div/div/div[5]/span')
        try:
            Creation= Creation.replace('\n', '') #traitement de la chaine de caractères pour ne garder que la valeur utile
        except:
            Creation = Creation
        ICE = extract_xpath_text('/html/body/div[4]/div[5]/div/div/div[6]/span')
        try:
            ICE = ICE.replace('ICE : ', '') #traitement de la chaine de caractères pour ne garder que la valeur utile
        except:
            ICE = ICE
        RespoExport = extract_text('p', {"class": "par-list"})
        Activite = extract_xpath_text('/html/body/div[4]/div[9]/div/div/div/p')

        # Nettoyer et séparer les données extraites
        try:
            Capital = Capital.replace('\n', '')
            Capital = Capital.replace('CAPITAL : ','')
            FormeJuridique, Capital = splitchiffres(Capital)
        except Exception:
            FormeJuridique = "N/A"

        try:
            RC = RC.replace('\n', '')
            RC= RC.replace('RC : ','')
            RC, VilleTribunal = splitchiffres(RC)

        except Exception:
            VilleTribunal = "N/A"
        try:
            Creation= Creation.replace('\n', '')
            Creation= Creation.replace('CREATION : ','')
        except:
            Creation = Creation



        try:
            produits = soup.find_all('div', class_='card-body pb-0')[0]  # il y a plusieurs élements dans la page qui ont cette même classe
            produits = produits.text.replace('\n', ' ')
            i = 1
            while not produits.startswith(' PRODUIT') and i < len(soup.find_all('div', class_='card-body pb-0')):  #permet de trouver le bon élement dans tous les élements de cette classe
                produits = soup.find_all('div', class_='card-body pb-0')[i].text.replace('\n', ' ')
                i += 1
            if produits.startswith('  ACTIVI'):
                produits = "N/A"
        except Exception:
            produits = "N/A"

        if produits != 'N/A':
            produits = produits[21:]  #garde seulement la partie utile

        sitesupp = ['https://kerix-export.net' + link['href'] for link in soup.find_all('a', href=True) if link['href'].startswith(url)]
        zoneexport = extract_xpath_text('/html/body/div[4]/div[13]/div/div/div/div/div/span')
        return [
            f'https://www.kerix-export.net{url}', Entreprise, Adresse, Tel, Tel2, Tel3, Fax, Site, Effectif,
            FormeJuridique, CA, Capital, RC, VilleTribunal, Creation, ICE, RespoExport, Activite, produits, zoneexport, sitesupp
        ]
    else:
        print(f"Erreur lors de la requête: {response.status_code}")
        return None

# Stockage des données
data = []

# Décommenter ces lignes pour utiliser ThreadPoolExecutor pour le traitement en parallèle
with ThreadPoolExecutor(max_workers=4) as executor:    #il y aura au plus 4 executions en parallèle
    results = executor.map(extract_info, [url[0] for url in urls])  #on execute le code seulement sur les 200 premières entreprises pour cet échantillon de test
for result in results:
    if result is not None:
        data.append(result)

df = pd.DataFrame(data, columns=[
    'URL', 'Entreprise', 'Adresse', 'Tel', 'Tel2', 'Tel3', 'Fax', 'Site', 'Effectif', 'FormeJuridique', 'ChiffreAffaire', 'Capital', 'RC', 'VilleTribunal', 'Creation', 'ICE', 'Dirigeant', 'Activite', 'Produits Exportes', "Zone d'exportation",'SitesSupp'
])
df.to_excel('/Users/othmaneirhboula/WebScrap/Kerix-export/ScrapingKerix-Export_final.xlsx', index=False)

# Décommenter pour tester une URL
# print([
#     'URL', 'Entreprise', 'Adresse', 'Tel', 'Tel2', 'Tel3', 'Fax', 'Site', 'Effectif', 'FormeJuridique',
#     'ChiffreAffaire', 'Capital', 'RC', 'VilleTribunal', 'Creation', 'ICE', 'Dirigeant', 'Activite', 'Produits Exportes', 'Zone export', 'SitesSupp'
# ])
# print(extract_info('/fr/entreprise/acrow-morocco'))
