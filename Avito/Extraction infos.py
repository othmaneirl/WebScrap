# Ce code permet d'extraire les données des annonces à partir d'un fichier csv contenant toutes les urls a scraper

#2000 annonces scrapées en 5 minutes


import requests
from bs4 import BeautifulSoup
from lxml import etree
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import csv

def csv_to_dict(filename): # Fonction pour convertir les colonnes d'un fichier CSV en dictionnaire
    result_dict = {}
    with open(filename, mode='r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if len(row) == 2:
                key, value = row
                result_dict[key] = value
    return result_dict

# Chemin vers le fichier CSV contenant les numéros de téléphone
filename = '/Users/othmaneirhboula/WebScrap/Avito/Liens/NumTelBoutiques.csv'
numeros = csv_to_dict(filename)

# Chemin vers le fichier CSV contenant les URL
lienscsv = '/Users/othmaneirhboula/WebScrap/Avito/Liens/Liens.csv'
df = pd.read_csv(lienscsv)
urls = df.values.tolist()

def extract_text(soup, tag, attrs): # Fonction pour extraire le texte d'un élément HTML avec BeautifulSoup
    try:
        element = soup.find(tag, attrs)
        return element.text.strip() if element else "N/A"
    except Exception:
        return "N/A"

def extract_xpath_text(dom, path): # Fonction pour extraire le texte d'un élément HTML avec XPath
    try:
        return dom.xpath(path)[0].text.strip()
    except Exception:
        return "N/A"

def extract_info(url):  # Fonction pour extraire les informations d'une page du site avito.ma
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = session.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        dom = etree.HTML(str(soup))

        # Extraction des différents éléments demandés
        annonceur = extract_text(soup, "p", {"class": "sc-1x0vz2r-0 fUTtTl sc-1l0do2b-9 bkvpcU"})
        article = extract_text(soup, "h1", {"class": "sc-1g3sn3w-12 jUtCZM"})
        prix = extract_xpath_text(dom, '/html/body/div/div/main/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/p')
        if prix == "N/A":
            prix = extract_xpath_text(dom, '/html/body/div/div/main/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[3]/div[1]/div[1]/div[2]/p')
        sous_categorie = extract_xpath_text(dom, '/html/body/div/div/main/div/div[3]/div[1]/div[1]/div[1]/ol/li[7]/a')
        categorie = extract_xpath_text(dom, '/html/body/div/div/main/div/div[3]/div[1]/div[1]/div[1]/ol/li[6]/a')
        date_annonce = soup.find("time").get("datetime") if soup.find("time") else "N/A"
        ville = extract_text(soup, "span", {"class": "sc-1x0vz2r-0 iotEHk"})

        try:
            numero = numeros[annonceur]
        except Exception:
            numero = "N/A"

        # Retourner les résultats
        return [annonceur, article, prix, categorie, sous_categorie, date_annonce, ville, numero, url]
    else:
        print(f"Erreur lors de la requête: {response.status_code}")
        return None

# # Stockage des données
data = []

# Utiliser ThreadPoolExecutor pour exécuter les tâches en parallèle
with ThreadPoolExecutor(max_workers=3) as executor:
    results = executor.map(extract_info, [url[0] for url in urls[:2000]])

for result in results:
    if result is not None:
        data.append(result)

# Enregistrer les résultats dans un fichier Excel
df = pd.DataFrame(data, columns=['annonceur', 'article', 'prix', 'categorie', 'sous-categorie', 'date_annonce', 'ville', 'tel', 'URL'])
df.to_excel('/Users/othmaneirhboula/WebScrap/Avito/ScrapingAvito.xlsx', index=False)

