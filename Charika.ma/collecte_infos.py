import csv
from unidecode import unidecode
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os

# Options pour le navigateur
chrome_options = Options()
chrome_options.add_argument('--headless=new')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')

driver = webdriver.Chrome(options=chrome_options)
n = 2020
csv_file = 'Input/entreprises' + str(n) + '.csv'

# Lire le fichier CSV en ignorant la première ligne
with open(csv_file, 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Ignorer la première ligne
    urls = [row[1] for row in csv_reader]  # Lire seulement la deuxième colonne

data = []
batch_size = 100  # Taille du lot pour les sauvegardes périodiques
batch_counter = 0


def save_to_csv(data, n, batch_num):
    output_csv_file = f'Output/entreprises_{str(n)}_batch_{batch_num}.csv'
    with open(output_csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            ["Nom de l'entreprise", 'Activite', 'Adresse', 'Ville', 'Coordonnees geographiques', 'RC', 'Tribunal',
             'ICE', 'Forme Juridique', 'URL', 'Capital'])
        for row in data:
            writer.writerow(row)
    print(f"Les informations ont été sauvegardées dans {output_csv_file}")


def extract_info(driver, url):
    driver.get('https://charika.ma/' + url)
    wait = WebDriverWait(driver, 10)

    elems = []
    try:
        nom = wait.until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div[1]/div[1]/div/div[2]/div[1]/h1/a'))).text
    except:
        nom = 'N/A'
    try:
        activite = driver.find_element(By.XPATH,
                                       '/html/body/div[3]/div/div/div[2]/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/span').text
        activite = unidecode(activite)
    except:
        activite = 'N/A'
    try:
        adresse = driver.find_element(By.XPATH,
                                      '/html/body/div[3]/div/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[3]/div[1]').text
        adresse = unidecode(adresse)
    except:
        adresse = 'N/A'
    try:
        elem1 = driver.find_element(By.XPATH,
                                    '/html/body/div[3]/div/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[4]/div/div[1]/table/tbody/tr[1]').text
        elem1 = unidecode(elem1)
        elems.append(elem1)
    except:
        elem1 = 'N/A'
        elems.append(elem1)
    try:
        elem2 = driver.find_element(By.XPATH,
                                    '/html/body/div[3]/div/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[4]/div/div[1]/table/tbody/tr[2]').text
        elem2 = unidecode(elem2)
        elems.append(elem2)
    except:
        elem2 = 'N/A'
        elems.append(elem2)
    try:
        elem3 = driver.find_element(By.XPATH,
                                    '/html/body/div[3]/div/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[4]/div/div[1]/table/tbody/tr[3]').text
        elem3 = unidecode(elem3)
        elems.append(elem3)
    except:
        elem3 = 'N/A'
        elems.append(elem3)
    try:
        elem4 = driver.find_element(By.XPATH,
                                    '/html/body/div[3]/div/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[4]/div/div[1]/table/tbody/tr[4]').text
        elem4 = unidecode(elem4)
        elems.append(elem4)
    except:
        elem4 = 'N/A'
        elems.append(elem4)
    try:
        boutoncoordonnes = driver.find_element(By.XPATH,
                                               '/html/body/div[3]/div/div/div[2]/div/div[3]/div[2]/div/div/div[1]/div[4]/img')
        boutoncoordonnes.click()
        time.sleep(1)
        coordonnees = wait.until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div[3]/div[2]/div/div/div[1]/div[6]/div/div[1]/div'))).text
    except:
        coordonnees = 'N/A'

    RC, ICE, FJ, Capital = 'N/A', 'N/A', 'N/A', 'N/A'
    for elem in elems:
        if elem.startswith('RC'):
            RC = elem
        elif elem.startswith('ICE'):
            ICE = str(elem)
        elif elem.startswith('Forme'):
            FJ = elem
        elif elem.startswith('Capital'):
            Capital = elem

    activite = activite[10:]
    adresse = adresse[7:]
    RC = RC[2:]
    ICE = ICE[3:]
    FJ = FJ[16:]
    Capital = Capital[7:-3]
    try:
        num, text = RC.split(" (")
    except:
        num, text = 'N/A', 'N/A'
    RC = num
    tribunal = text[:-1]
    try:
        adresse_part, ville = adresse.split(" - ")
        adresse = adresse_part
    except:
        ville = 'N/A'
        adresse = 'N/A'
    return [nom, activite, adresse, ville, coordonnees, RC, tribunal, ICE, FJ, url, Capital]


try:
    driver.get('https://charika.ma/')
    time.sleep(6)

    premier_bouton = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div[1]/ul/li[4]/a/b')
    premier_bouton.click()
    time.sleep(4)
    deuxieme_bouton = driver.find_element(By.XPATH,
                                          '/html/body/div[1]/div/div/div[2]/div/div[1]/ul/li[4]/ul/div/div/div/div[1]/a/button')
    deuxieme_bouton.click()
    time.sleep(4)

    id = driver.find_element(By.XPATH, '/html/body/div[10]/div/div/div/div/div[1]/div[2]/div/div/form/div[1]/input')
    id.click()
    id.send_keys('yoyotirpsn4@gmail.com')

    mdp = driver.find_element(By.XPATH, '/html/body/div[10]/div/div/div/div/div[1]/div[2]/div/div/form/div[2]/input')
    mdp.click()
    mdp.send_keys('webscraping1')

    troisieme_bouton = driver.find_element(By.XPATH,
                                           '/html/body/div[10]/div/div/div/div/div[1]/div[2]/div/div/form/button')
    troisieme_bouton.click()

    time.sleep(5)

    cookies = driver.get_cookies()
    batch_num = 1

    for i, url in enumerate(urls):
        driver.delete_all_cookies()
        for cookie in cookies:
            driver.add_cookie(cookie)
        info = extract_info(driver, url)
        data.append(info)
        batch_counter += 1
        print(f"Entreprise {i + 1}/{len(urls)}: {info[0]}")

        if batch_counter >= batch_size:
            save_to_csv(data, n, batch_num)
            data.clear()
            batch_counter = 0
            batch_num += 1

    # Sauvegarde des données restantes
    if data:
        save_to_csv(data, n, batch_num)

finally:
    driver.quit()
    print("Scraping terminé et les informations ont été sauvegardés.")

# Combinaison des fichiers CSV en un seul fichier
output_file = f'Output/classement{str(n)}.csv'

# Liste pour stocker les DataFrames de chaque fichier CSV
dfs = []

# Parcourir les fichiers CSV dans le répertoire Output
for file_name in os.listdir('Output'):
    if file_name.endswith('.csv') and file_name.startswith('entreprises_'):
        file_path = os.path.join('Output', file_name)
        df = pd.read_csv(file_path)

        # Affichez les colonnes pour vérifier
        print(f"Fichier : {file_name}, Colonnes : {df.columns.tolist()}")

        # Ajoutez le DataFrame à la liste
        dfs.append(df)

# Combiner tous les DataFrames en un seul
combined_df = pd.concat(dfs, ignore_index=True)

# Vérifiez les colonnes du DataFrame combiné
print(f"Colonnes du DataFrame combiné : {combined_df.columns.tolist()}")

# Sauvegarder le DataFrame combiné dans un nouveau fichier CSV
combined_df.to_excel(f'annee{str(n)}')

print(f"Les fichiers ont été combinés avec succès en {output_file}")
