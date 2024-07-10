import requests
from bs4 import BeautifulSoup
from lxml import etree
import pandas as pd
from concurrent.futures import ThreadPoolExecutor


lienscsv = '/Users/othmaneirhboula/WebScrap/Kerix/Liens/Liens.csv'
df = pd.read_csv(lienscsv)
urls = df.values.tolist()


def extract_info(url):
    session = requests.Session()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = session.get(f'https://www.kerix.net{url}', headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        dom = etree.HTML(str(soup))

        def extract_text(soup_obj, tag, attrs):
            try:
                element = soup_obj.find(tag, attrs)
                return element.text.strip() if element else "N/A"
            except Exception:
                return "N/A"

        Entreprise = extract_text(soup, "h1", {"class": "card-title card-title-md mt-2"})
        Adresse = extract_text(soup, "p", {"class": "card-text"})
        try:
            Tel = dom.xpath('/html/body/div[2]/div[4]/div[2]/div/div[2]/div[1]/div[1]/div/p[1]')[0].text
        except Exception:
            Tel = "N/A"
        try:
            Tel2 = dom.xpath('/html/body/div[2]/div[4]/div[2]/div/div[2]/div[1]/div[1]/div/p[2]')[0].text
        except Exception:
            Tel2 = "N/A"
        try:
            Tel3 = dom.xpath('/html/body/div[2]/div[4]/div[2]/div/div[2]/div[1]/div[1]/div/p[3]')[0].text
        except Exception:
            Tel3 = "N/A"
        try:
            Fax = extract_text(soup, 'div' , {"id": "collapseExample2"})
        except Exception:
            Fax = "N/A"
        try:
            Site = soup.find('a', class_='btn btn-down website').get('href')
        except Exception:
            Site = "N/A"
        Infos= extract_text(soup, "div", {"class": "card-body pb-0"}).replace('\n', ' ')
        try:
            valeurs = Infos.split('-')

            while len(valeurs) < 6:
                valeurs.append("N/A")

            Effectif, ChiffreAffaire, Capital, RC, Creation, ICE = valeurs
            Effectif = Effectif.replace('EFFECTIF :', '')
            ChiffreAffaire = ChiffreAffaire.replace('CHIFFRE D\'AFFAIRES :', '')
            Capital = Capital.replace('CAPITAL :', '')
            Capital = Capital.replace(' DH  ', '')
            temp, temp2, FormeJuridique, Capital = Capital.split(' ')
            RC = RC.replace('RC :', '')
            RC= RC.replace('  ', '')
            try:
                RC, VilleTribunal = RC.split(' ')
            except:
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
        Dirigeant = extract_text(soup, "p", {"class": "par-list"}).replace('\n', ' ')
        try:
            Activite = dom.xpath('/html/body/div[2]/div[9]/div/div/div/p')[0].text.replace('\n', ' ')
        except Exception:
            Activite = "N/A"
        try:
            produits = soup.find_all('div', class_='card-body pb-0')[0]
            produits = produits.text.replace('\n', ' ')
            i=1
            while produits.startswith(' PRODUIT')==0 and i<len(soup.find_all('div', class_='card-body pb-0')):
                produits = soup.find_all('div', class_='card-body pb-0')[i].text.replace('\n', ' ')
                i+=1
            if produits.startswith('  ACTIVI'):
                produits = "N/A"
        except Exception:
            produits = "N/A"
        if produits!='N/A':
            produits = produits[22:]
        documents = [f"https://www.kerix.net{link['href']}" for link in soup.find_all('a', href=True) if link['href'].endswith('.pdf')]
        sitesupp = [f"https://www.kerix.net{link['href']}" for link in soup.find_all('a', href=True) if link['href'].startswith(url) ]
        return [f'https://www.kerix.net{url}',Entreprise, Adresse, Tel, Tel2, Tel3, Fax, Site, Effectif,FormeJuridique, ChiffreAffaire, Capital, RC, VilleTribunal, Creation, ICE, Dirigeant, Activite, produits, sitesupp, documents]
    else:
        print(f"Erreur lors de la requête: {response.status_code}")
        return None


data = []

# Utiliser ThreadPoolExecutor pour exécuter les tâches en parallèle
with ThreadPoolExecutor(max_workers=4) as executor:
    results = executor.map(extract_info, [url[0] for url in urls[:2000]])
for result in results:
    if result is not None:
        data.append(result)

df = pd.DataFrame(data,columns=['URL','Entreprise', 'Adresse', 'Tel', 'Tel2', 'Tel3', 'Fax', 'Site', 'Effectif', 'FormeJuridique', 'ChiffreAffaire', 'Capital', 'RC', 'VilleTribunal', 'Creation', 'ICE', 'Dirigeant', 'Activite', 'Produits', 'SitesSupp','Documents'])
df.to_excel('/Users/othmaneirhboula/WebScrap/Kerix/ScrapingKerix2.xlsx', index=False)
print(df['Produits'])

# print(extract_info('/fr/annuaire-entreprise/pacte'))