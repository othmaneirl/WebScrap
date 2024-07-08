import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
from multiprocessing import Pool

lienscsv = '/Users/othmaneirhboula/WebScrap/Avito/Liens/LiensArticlesPages.csv'
df = pd.read_csv(lienscsv)
urls = df.values.tolist()

def extract_links_and_articles(url):
    # Créer une session
    session = requests.Session()

    # Définir les en-têtes HTTP pour imiter un navigateur
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Envoyer une requête GET à l'URL avec les en-têtes et la session
    response = session.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []

    # Parser le contenu HTML avec BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Trouver toutes les balises <a> correspondant aux boutiques
    a_tags = soup.find_all('a', class_='sc-1jge648-0 eTbzNs')

    # Extraire les liens href et le nombre d'articles
    links = []
    for a in a_tags:
        link = a.get('href')
        if link and link.endswith('htm'):
            links.append(link)
    return links

def collect_links(url):
    links = extract_links_and_articles(url[0])
    return links

if __name__ == '__main__':
    with Pool(3) as pool:
        results = pool.map(collect_links, urls)

    # Flatten the list of lists
    liens = [link for sublist in results for link in sublist]
    liens=set(liens)
    # Enregistrer les données dans un fichier CSV
    with open('/Users/othmaneirhboula/WebScrap/Avito/Liens/Liens.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['URL'])  # Ajouter les en-têtes des colonnes
        for line in liens:
            writer.writerow([line])

    print(f"Les données ont été enregistrées dans Liens.csv")
