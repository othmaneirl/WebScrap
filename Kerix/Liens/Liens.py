# Ce code permet d'aller sur chaque URL de recherche des entreprises par lettre sur le site kerix.net et de récupérer les liens des entreprises sur chaque page.
import requests
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

entrprisesparlettre = 'Liens/kerix.xlsx' # Chemin vers le fichier Excel contenant les URL de chaque recherche et le nombre de pages à parcourir par lettre
df = pd.read_excel(entrprisesparlettre)  #lire le fichier excel
urls = df.values.tolist()          #convertir le dataframe en liste

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
    a_tags = soup.find_all('a', class_='btn-success btn btn-sm bg-green-light pull-right')  #récupérer les liens des entreprises
    links = []
    for a in a_tags:
        link = a.get('href') #récupérer le lien
        if link:
            links.append(link)
    return links

def process_url(url_info):  #fonction pour traiter les URL
    base_url, _, max_pages = url_info
    all_links = []
    for i in range(1, max_pages + 1):
        page_url = f"{base_url}?page={i}"  #récuperer les pages de chaque URL
        links = geturl(page_url)
        all_links.extend(links)
        print(f"Processed page {i} for URL: {base_url}")
    return all_links #retourner les liens

# Utiliser ThreadPoolExecutor pour exécuter les tâches en parallèle
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(process_url, url_info) for url_info in urls]
    results = [future.result() for future in futures]

# Convertir les résultats en DataFrame
data = [link for sublist in results for link in sublist]
df = pd.DataFrame(data, columns=['URL'])
print(df)
df.to_excel('kerix_links4.xlsx', index=False)
