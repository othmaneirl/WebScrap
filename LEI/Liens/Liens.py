import requests
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import re


def geturl(url): #fonction pour récupérer les liens des entreprises
    session = requests.Session()
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        } #headers pour imiter un navigateur
    response = session.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []

    # Charger le fichier HTML
    html_content = response.text

    # Créer une instance BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')  #parser le contenu html
    a_tags = soup.find_all('a')  # récupérer les liens des entreprises
    links = []
    for a in a_tags:
        link = a.get('href')  # récupérer le lien
        if link and re.match(r'^/\d', link):
            links.append(link)
    return links
urls=[f'https://lei.info/catalog?page={i}&pageSize=40000' for i in range(1, 54 + 1)]  #récupérer les urls de 54 pages contenant 40000 entreprises chacunes
def process_url(url_info):  #fonction pour traiter les URL
    base_url=url_info
    all_links = []
    page_url = base_url  #récuperer les pages de chaque URL
    links = geturl(page_url)
    all_links.extend(links)
    print(f"Processed URL: {base_url}")
    return all_links #retourner les liens

# Utiliser ThreadPoolExecutor pour exécuter les tâches en parallèle
with ThreadPoolExecutor(max_workers=8) as executor:
    futures = [executor.submit(process_url, url_info) for url_info in urls]
    results = [future.result() for future in futures]

# Convertir les résultats en DataFrame
data = [link for sublist in results for link in sublist]
df = pd.DataFrame(data, columns=['URL'])
print(df)
df.to_csv('Liens.csv', index=False)
