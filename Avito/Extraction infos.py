import requests
from bs4 import BeautifulSoup
from lxml import etree
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import csv
def csv_to_dict(filename):
    result_dict = {}
    with open(filename, mode='r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if len(row) == 2:
                key, value = row
                result_dict[key] = value
    return result_dict

filename = '/Users/othmaneirhboula/WebScrap/Avito/Liens/NumTelBoutiques.csv'
numeros = csv_to_dict(filename)
lienscsv = '/Users/othmaneirhboula/WebScrap/Avito/Liens/Liens.csv'
df = pd.read_csv(lienscsv)
urls = df.values.tolist()


def extract_info(url):
    session = requests.Session()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = session.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        dom = etree.HTML(str(soup))

        def extract_text(soup_obj, tag, attrs):
            try:
                element = soup_obj.find(tag, attrs)
                return element.text.strip() if element else "N/A"
            except Exception:
                return "N/A"

        try:
            annonceur = extract_text(soup, "p", {"class": "sc-1x0vz2r-0 fUTtTl sc-1l0do2b-9 bkvpcU"})
        except Exception:
            annonceur = "N/A"

        try:
            article = extract_text(soup, "h1", {"class": "sc-1g3sn3w-12 jUtCZM"})
        except Exception:
            article = "N/A"

        try:
            prix = \
            dom.xpath('/html/body/div/div/main/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/p')[
                0].text
        except Exception:
            prix = \
            dom.xpath('/html/body/div/div/main/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[3]/div[1]/div[1]/div[2]/p')[
                0].text
        except:
            prix = "N/A"

        try:
            sous_categorie = dom.xpath('/html/body/div/div/main/div/div[3]/div[1]/div[1]/div[1]/ol/li[7]/a')[0].text
        except Exception:
            sous_categorie = "N/A"

        try:
            categorie = dom.xpath('/html/body/div/div/main/div/div[3]/div[1]/div[1]/div[1]/ol/li[6]/a')[0].text
        except Exception:
            categorie = "N/A"

        try:
            date_annonce = soup.find("time").get("datetime")
        except Exception:
            date_annonce = "N/A"

        try:
            ville = extract_text(soup, "span", {"class": "sc-1x0vz2r-0 iotEHk"})
        except Exception:
            ville = "N/A"

        try:
            numero=numeros[annonceur]
        except:
            numero='N/A'

        # Afficher les résultats
        return [annonceur, article, prix, categorie, sous_categorie, date_annonce, ville, numero,url]
    else:
        print(f"Erreur lors de la requête: {response.status_code}")
        return None


data = []

# Utiliser ThreadPoolExecutor pour exécuter les tâches en parallèle
with ThreadPoolExecutor(max_workers=3) as executor:
    results = executor.map(extract_info, [url[0] for url in urls[:2000]])

for result in results:
    if result is not None:
        data.append(result)

df = pd.DataFrame(data,columns=['annonceur', 'article', 'prix', 'categorie', 'sous-categorie', 'date_annonce', 'ville','tel','URL'])
df.to_excel('/Users/othmaneirhboula/WebScrap/Avito/ScrapingAvito.xlsx', index=False)
print(df)
