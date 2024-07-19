# Ce code permet de génerer les urls de recherche des entreprises par ordre alphabétique sur le site kerix-export.net
import requests
from bs4 import BeautifulSoup
from lxml import etree
import pandas as pd
l=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
def geturlpage(lettre):
    url = f'https://www.kerix-export.net/fr/recherche/entreprise-marque/{lettre}.html'
    session = requests.Session()
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    response = session.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
    # Charger le fichier HTML
    html_content = response.text

    # Créer une instance BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    dom = etree.HTML(str(soup))
    try:
        nombre_pages = dom.xpath('/html/body/div[6]/div/div/ul/li[13]/a')[0].text
    except:
        nombre_pages=1
    nombre_entreprises= dom.xpath('/html/body/div[5]/div/div/div[1]/div[1]/div/h5/span/span')[0].text
    return [url, nombre_entreprises.split(" ")[0],nombre_pages]
data=[]
for lettre in l:
    data.append(geturlpage(lettre))
df=pd.DataFrame(data,columns=['URL','Nombre d\'entreprises','Nombre de pages'])
df.to_excel('kerix-export.xlsx',index=False)
