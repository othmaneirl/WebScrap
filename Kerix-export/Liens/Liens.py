# Ce code permet d'aller sur chaque URL de recherche des entreprises par lettre sur le site kerix-export.net et de récupérer les liens des entreprises sur chaque page.

import requests
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

entrprisesparlettre = 'kerix-export.xlsx'
df = pd.read_excel(entrprisesparlettre)
urls = df.values.tolist()

def geturl(url):
    session = requests.Session()
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    response = session.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []

    # Charger le fichier HTML
    html_content = response.text

    # Créer une instance BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    a_tags = soup.find_all('a', class_='btn-success btn btn-sm bg-green-light pull-right')
    links = []
    for a in a_tags:
        link = a.get('href')
        if link:
            links.append(link)
    return links

def process_url(url_info):
    base_url, _, max_pages = url_info
    all_links = []
    for i in range(1, max_pages + 1):
        page_url = f"{base_url}?page={i}"
        links = geturl(page_url)
        all_links.extend(links)
        print(f"Processed page {i} for URL: {base_url}")
    return all_links

# Utiliser ThreadPoolExecutor pour exécuter les tâches en parallèle
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(process_url, url_info) for url_info in urls]
    results = [future.result() for future in futures]

# Convertir les résultats en DataFrame
data = [link for sublist in results for link in sublist]
df = pd.DataFrame(data, columns=['URL'])
print(df)
df.to_excel('kerix-export_links.xlsx', index=False)
