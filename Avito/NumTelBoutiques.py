# Ce code permet d'associer un numero de téléphone a chaque boutique pour nous éviter d'avoir à utiliser selenium pour le scraping de toutes les annonces
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

path='/Users/othmaneirhboula/WebScrap/Avito/Liens/LiensBoutiquesArticles.csv'

df = pd.read_csv(path)
urls = df.values.tolist()

chrome_options = Options()
chrome_options.add_argument('--headless=new') # headless mode
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=chrome_options)
data=[]
for url in urls: #boucle pour parcourir les URL
    driver.get(url[0])
    wait = WebDriverWait(driver, 10)
    try:  #on veut récuperer le nom de la boutique et son numero de telephone, qui n'est accessible qu'après un clic sur un bouton
        nom=wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div/div/main/div/div[1]/div[2]/div[1]/div[1]/p'))).text
        bouton_num=wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div/div/main/div/div[1]/div[2]/div[2]/div[2]/div[3]/button[2]')))
        bouton_num.click()
        time.sleep(0.5)
        numero=wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div/div/main/div/div[1]/div[2]/div[2]/div[2]/div[3]/div/div/div/div/div/a/span/span'))).text
    except:
        numero = 'N/A'
    data.append([nom,numero])  #ajouter les données à la liste data
df=pd.DataFrame(data,columns=['Nom','Numero'])
df.to_csv('/Users/othmaneirhboula/WebScrap/Avito/Liens/NumTelBoutiques.csv',index=False) #enregistrer les données dans un fichier csv
