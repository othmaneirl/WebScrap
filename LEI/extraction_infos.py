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
lienscsv = '/Users/othmaneirhboula/WebScrap/LEI/Liens/Liens.csv'
df = pd.read_csv(lienscsv)
urls = df.values.tolist()

def extract_info(url):  #fonction qui extrait les informations d'une entreprise à partir de son URL
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = session.get(url, headers=headers)

    if response.status_code == 200:   #si la page est accessible on extrait les informations
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

        LEI = url[17:]  #on extrait le LEI code à partir de l'URL
        Entity_Name = extract_xpath_text('/html/body/div[2]/div[1]/div[1]/div[1]/h1')
        Entity_Status = extract_xpath_text('/html/body/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[1]/div/div[11]')
        #on extrait les informations de la page grace à la classe des colonnes et des valeurs
        colonnes = [x.text.strip() for x in soup.findAll('div', attrs={'class': 'col-md-5 col-sm-5 col-xs-12 definition'}) if x.text.strip().startswith('Initial registration') == False and x.text.strip().startswith('Last update') == False and x.text.strip().startswith('Next renewal') == False]
        lignes = [x.text.strip() for x in soup.findAll('div', attrs={'class': 'col-md-7 col-sm-7 col-xs-12 value'}) if x.text.strip().startswith('20') == False]

        lei_data = dict(zip(colonnes, lignes)) #on crée un dictionnaire contenant les informations de l'entreprise
        lei_data.update({     #on ajoute les informations supplémentaires
            'entity name': Entity_Name,
            'entity_status': Entity_Status,
            'url': url,
            'lei code': LEI,
            'detail_supp': extract_text('div', {'class': 'seo-block margin-top-40'})
        })
        return lei_data
    else:  #si la page n'est pas accessible on retourne des valeurs par défaut
        return None

#on crée un dataframe contenant les informations de toutes les entreprises
data = []
with ThreadPoolExecutor(max_workers=4) as executor:    #il y aura au plus 4 executions en parallèle
    results = executor.map(extract_info, [url[0] for url in urls[:2000]])  #on execute le code seulement sur les 200 premières entreprises pour cet échantillon de test
for result in results:
    if result is not None:
        data.append(result)

df = pd.DataFrame(data)
df.to_excel('/Users/othmaneirhboula/WebScrap/LEI/Scrapingbis.xlsx', index=False)

#pour tester le code sur une seule entreprise
# print(extract_info(urls[0][0]))

