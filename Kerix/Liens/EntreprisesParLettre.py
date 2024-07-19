# Ce code permet de génerer les urls de recherche des entreprises par ordre alphabétique sur le site kerix.net
import requests
from bs4 import BeautifulSoup
from lxml import etree
import pandas as pd
l=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']  #liste des lettres de l'alphabet pour trouver le plus d'entreprises possible
def geturlpage(lettre):  #fonction pour récupérer le nombre d'entreprises et de pages pour chaque lettre
    url = f'https://www.kerix.net/fr/recherche/entreprise-marque/{lettre}.html'
    session = requests.Session()
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }  #headers pour imiter un navigateur
    response = session.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
    # Charger le fichier HTML
    html_content = response.text

    # Créer une instance BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    dom = etree.HTML(str(soup))
    xpathpage='/html/body/div[3]/div/div/ul/li[13]/a'    #xpath pour récupérer le nombre de pages
    try:
        nombre_pages = dom.xpath(xpathpage)[0].text  #récupérer le nombre de pages
    except:
        nombre_pages=1   #s'il y a une erreur c'est que le nombre de pages est 1
    nombre_entreprises= dom.xpath('/html/body/div[2]/div/div/div[2]/div[1]/div/h5/span')[0].text  #récupérer le nombre d'entreprises
    return [url, nombre_entreprises.split(" ")[1],nombre_pages]
data=[]
for lettre in l:
    data.append(geturlpage(lettre))
df=pd.DataFrame(data,columns=['URL','Nombre d\'entreprises','Nombre de pages']) #créer un dataframe avec les données récupérées
df.to_excel('kerix.xlsx',index=False)  #enregistrer le dataframe dans un fichier excel
