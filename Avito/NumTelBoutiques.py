import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import csv
import time

path='/Users/othmaneirhboula/WebScrap/Avito/Liens/LiensBoutiquesArticles.csv'

df = pd.read_csv(path)
urls = df.values.tolist()

chrome_options = Options()
chrome_options.add_argument('--headless=new')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=chrome_options)
data=[]
for url in urls:
    driver.get(url[0])
    wait = WebDriverWait(driver, 10)
    try:
        nom=wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div/div/main/div/div[1]/div[2]/div[1]/div[1]/p'))).text
        bouton_num=wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div/div/main/div/div[1]/div[2]/div[2]/div[2]/div[3]/button[2]')))
        bouton_num.click()
        time.sleep(0.5)
        numero=wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div/div/main/div/div[1]/div[2]/div[2]/div[2]/div[3]/div/div/div/div/div/a/span/span'))).text
    except:
        numero = 'N/A'
    data.append([nom,numero])
df=pd.DataFrame(data,columns=['Nom','Numero'])
df.to_csv('/Users/othmaneirhboula/WebScrap/Avito/Liens/NumTelBoutiques.csv',index=False)
