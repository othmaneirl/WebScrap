# Ce code permet de récuperer les liens des annonces 'achat, location, location vacances...) du site Mubawab
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd

def geturl(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        content = response.text
        soup = BeautifulSoup(content, 'html.parser')
        links = []
        a_tags = soup.find_all('a', href=True)
        for a in a_tags:
            if a['href'] in links:
                continue
            else:
                links.append(a['href'])
        links = [link for link in links if not link.startswith(('https://www.mubawab.ma/fr/app', 'https://www.mubawab.ma/fr/about')) and link.startswith(('https://www.mubawab.ma/fr/a', 'https://www.mubawab.ma/fr/pa'))]
        return list(set(links))
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return []

urls = [f'https://www.mubawab.ma/fr/sc/appartements-a-vendre:p:{i}' for i in range(1, 506 + 1)]


# Utilisation d'un thread pool avec 4 workers
with ThreadPoolExecutor(max_workers=4) as executor:
    future_to_url = {executor.submit(geturl, url): url for url in urls}
    liens = []
    for future in as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
            if data:
                liens.extend(data)
        except Exception as exc:
            print(f"{url} generated an exception: {exc}")

liens = list(set(liens))

# Enregistrement des liens dans un fichier CSV
df = pd.DataFrame(liens, columns=['URL'])
df.to_csv('Liens_Ach.csv', index=False)

