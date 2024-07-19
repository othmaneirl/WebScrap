# Ce code permet de récuperer les urls des annonces sur le site Yakeey
import requests
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import re

def geturl(type, page):
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    url = f'https://yakeey.com/fr-ma/{type}/biens/maroc?page={page}'
    response = session.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to retrieve page {page}. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    links = ['https://yakeey.com'+link.get('href') for link in soup.select("a.MuiBox-root.mui-1y4n71p") if link.get('href')]
    return list(set(links))

def process_urls(type, max_page):
    all_links = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(geturl, type, page) for page in range(1, max_page + 1)]
        for future in futures:
            all_links.extend(future.result())
            print(f"Processed URL for {type}")
    return list(set(all_links))

# Définir les types et les pages maximum
types_and_pages = {
    'achat': 44,
    'location': 14
}

# Récupérer les liens pour chaque type
results = []
for type, max_page in types_and_pages.items():
    results.extend(process_urls(type, max_page))

# Convertir les résultats en DataFrame
df = pd.DataFrame(results, columns=['URL'])
print(df)
df.to_csv('/Users/othmaneirhboula/WebScrap/Yakeey_Final/Liens/Liens.csv', index=False)
