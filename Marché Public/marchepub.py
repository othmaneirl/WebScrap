import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select


import time
# Configurez le chemin vers le driver approprié pour votre navigateur
# Pour Chrome, par exemple, vous devez télécharger le chromedriver et spécifier son chemin
driver_path = 'path/to/chromedriver'  # Remplacez par le chemin réel vers chromedriver

# URL de la page à scraper
url = 'https://www.marchespublics.gov.ma/index.php?page=entreprise.EntrepriseAdvancedSearch&AllAnn'  # Remplacez par l'URL réelle

# Initialisez les options du navigateur
chrome_options = Options()
#chrome_options.add_argument("--headless")  # Optionnel : lance le navigateur en mode headless

# Initialisez le navigateur
driver = webdriver.Chrome(options=chrome_options)

# Ouvrez la page web
driver.get(url)
bouton=driver.find_element(By.XPATH, '//*[@id="ctl0_CONTENU_PAGE_AdvancedSearch_lancerRecherche"]')
bouton.click()
time.sleep(5)
select_element = driver.find_element(By.XPATH, '//*[@id="ctl0_CONTENU_PAGE_resultSearch_listePageSizeTop"]')
select = Select(select_element)
select.select_by_value('500')
time.sleep(10)
divs = driver.find_elements(By.CSS_SELECTOR, 'div.actions')

# Liste pour stocker les liens
links = []

# Parcourez chaque div et extrayez le premier lien
for div in divs:
    try:
        first_link = div.find_element(By.TAG_NAME, 'a').get_attribute('href')
        links.append(first_link)
    except Exception as e:
        print(f"Erreur lors de l'extraction du lien dans un div : {e}")

# Fermez le navigateur
driver.quit()

# Écrivez les liens dans un fichier CSV
with open('links.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Lien'])
    for link in links:
        writer.writerow([link])

print("Extraction des liens terminée et sauvegardée dans links.csv")
