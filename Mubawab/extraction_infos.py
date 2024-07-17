from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor, as_completed
import bs4
import pandas as pd
from lxml import etree
import time
lienscsv = '/Users/othmaneirhboula/WebScrap/Mubawab/Liens/Liens_Ach.csv'
df = pd.read_csv(lienscsv)
urls = df.values.tolist()

# Options pour le navigateur
chrome_options = Options()
chrome_options.add_argument('--headless=new')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--blink-settings=imagesEnabled=false')

def extract_info(url):
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(1)
    try:
        content = driver.page_source
        soup = bs4.BeautifulSoup(content, 'html.parser')
        dom = etree.HTML(str(soup))

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
        def get_element_after(tag, attrs):
            try:
                element = soup.find(tag, attrs)
                return element.find_next('span').text.strip() if element else "N/A"
            except Exception:
                return "N/A"
        title = extract_text('h1', {'class': 'searchTitle'})
        price = extract_text('h3', {'class': 'orangeTit'})
        place = extract_text('h4', {'class': 'titBlockProp inBlock'})
        surface = get_element_after('i', {'class': 'icon-triangle adDetailFeatureIcon'})
        chambres = get_element_after('i', {'class': 'icon-bed adDetailFeatureIcon'})
        pieces = get_element_after('i', {'class': 'icon-house-boxes adDetailFeatureIcon'})
        bains = get_element_after('i', {'class': 'icon-bath adDetailFeatureIcon'})
        colonnes = [x.text.strip() for x in soup.findAll('p', attrs={'class': 'adMainFeatureContentLabel'})]
        lignes = [x.text.strip() for x in soup.findAll('p', attrs={'class': 'adMainFeatureContentValue'})]
        owner = extract_text('span', {'class': 'link businessName'})
        data={ 'URL':url,'Titre': title, 'Prix': price, 'Lieu': place, 'Owner': owner, 'Surface': surface, 'Pièces': pieces, 'Chambres': chambres, 'Salles de bain': bains}
        data.update(dict(zip(colonnes, lignes)))
        # owner         non disponible sur le site
        bouton_tel = driver.find_element(By.XPATH, '//*[@id="stickyDiv"]/div/div[2]/div[1]/div/div')
        driver.execute_script("arguments[0].click();", bouton_tel)
        time.sleep(0.5)
        tel = driver.execute_script("return document.querySelector('p.phoneText.dirLtr.darkblue').textContent;")
        data.update({"Numero de telephone": tel})
        return data
    except Exception as e:
        return None
    finally:
        driver.quit()



urls_total = []

# Utilisation de ThreadPoolExecutor pour le multithreading
data = []
with ThreadPoolExecutor(max_workers=4) as executor:    #il y aura au plus 4 executions en parallèle
    results = executor.map(extract_info, [url[0] for url in urls[:100]])  #on execute le code seulement sur les 200 premières entreprises pour cet échantillon de test
for result in results:
    if result is not None:
        data.append(result)


df = pd.DataFrame(data)
df.replace('\xa0', ' ', regex=True, inplace=True)
df.replace('\n', '', regex=True, inplace=True)
df.replace('\t', '', regex=True, inplace=True)
df.to_excel('/Users/othmaneirhboula/WebScrap/Mubawab/ScrapingMubawab.xlsx', index=False)
# print(extract_info('https://www.mubawab.ma/fr/pa/7837256/vend-appartement-en-centre-superficie-114-m²'))