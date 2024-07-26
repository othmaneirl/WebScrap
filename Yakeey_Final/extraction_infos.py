# Ce code permet de récuperer les informations des annonces du site Yakeey avec bs4

# 1000 Sites scrapés en 5 minutes
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
lienscsv = '/Users/othmaneirhboula/WebScrap/Yakeey_Final/Liens/Liens.csv'
df = pd.read_csv(lienscsv)
urls = df.values.tolist()

def extract_info(url):  #fonction qui extrait les informations d'une entreprise à partir de son URL
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = session.get(url, headers=headers)
    data = {}
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
        def extract_CSS_text(css_selector):
            try:
                element = soup.select_one(css_selector)
                return element.text.strip() if element else "N/A"
            except Exception:
                return "N/A"
        Article = extract_CSS_text(
            'body > div.mui-1xs344a > div > div > div > div > div > div > div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-24.MuiGrid-grid-lg-17.mui-6k8xca > div.MuiBox-root.mui-5vb4lz > div > h1')
        type_annonce = url.split('/')[4].split('-')[
            0]  # on extrait le type d'annonce à partir de l'URL (location ou vente
        Reference = url.split('-')[-1]
        Localisation = extract_xpath_text('/html/body/div[2]/div/div/div/div/div/div/div[1]/div[3]/div/h6')
        Prix = extract_CSS_text(
            'body > div.mui-1xs344a > div > div > div > div > div > div > div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-24.MuiGrid-grid-lg-7.mui-10yxvqi > div > div > div > div > div.MuiBox-root.mui-0 > div > div.MuiStack-root.mui-1bjfkal > p')
        Depot_garantie = extract_xpath_text(
            '/html/body/div[2]/div/div/div/div/div/div/div[1]/div[8]/div[2]/div/div/div/div[2]/div[2]/p')
        Frais_service = extract_xpath_text(
            '/html/body/div[2]/div/div/div/div/div/div/div[1]/div[8]/div[2]/div/div/div/div[3]/div[2]/p')
        Type_Batiment = Article.split(" ")[0]
        data.update({  # on ajoute les informations supplémentaires
            'url' : url,
            'Article': Article,
            'Type_annonce': type_annonce,
            'Reference': Reference,
            'Localisation': Localisation,
            'Prix': Prix,
            'Type_Batiment': Type_Batiment,
            'Depot_garantie': Depot_garantie,
            'Frais_service': Frais_service
        })
        colonnes = [x.text.strip() for x in soup.findAll('p', attrs={'class': 'MuiTypography-root MuiTypography-body1 MuiTypography-gutterBottom mui-roqi3n'})]
        lignes = [x.text.strip() for x in soup.findAll('p', attrs={'class': 'MuiTypography-root MuiTypography-body1 MuiTypography-gutterBottom mui-1atau07'})]
        data.update(dict(zip(colonnes, lignes)))
        return data
    else:  #si la page n'est pas accessible on retourne des valeurs par défaut
        return None

# on crée un dataframe contenant les informations de toutes les entreprises
data = []
with ThreadPoolExecutor(max_workers=4) as executor:    #il y aura au plus 4 executions en parallèle
    results = executor.map(extract_info, [url[0] for url in urls])  #on execute le code seulement sur les 200 premières entreprises pour cet échantillon de test
for result in results:
    if result is not None:
        data.append(result)

df = pd.DataFrame(data)
df.to_excel('/Users/othmaneirhboula/WebScrap/Yakeey_final/ScrapingYakeey.xlsx', index=False)

#pour tester le code sur une seule annonce
# print(extract_info('https://yakeey.com/fr-ma/programme/acheter-appartement-casablanca-oulfa-pc000152'))





