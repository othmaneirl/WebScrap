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
n = 2022
csv_file = f'Input/entreprises{n}.csv'

# Lire le fichier CSV en ignorant la première ligne
with open(csv_file, 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Ignorer la première ligne
    urls = [row[1] for row in csv_reader]  # Lire seulement la deuxième colonne

data = []
batch_size = 100  # Taille du lot pour les sauvegardes périodiques
batch_counter = 0


def save_to_csv(data, n, batch_num):
    output_csv_file = f'Output/entreprises_{n}_batch_{batch_num}.csv'
    with open(output_csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            ["Nom de l'entreprise", 'Activite', 'Adresse', 'Ville', 'Coordonnees geographiques', 'RC', 'Tribunal',
             'ICE', 'Forme Juridique', 'URL', 'Capital'])
        writer.writerows(data)
    print(f"Les informations ont été sauvegardées dans {output_csv_file}")


def extract_info(driver, url):
    driver.get(f'https://charika.ma/{url}')
    wait = WebDriverWait(driver, 10)

    def safe_extract(xpath, default='N/A', transform=lambda x: x):
        try:
            elem = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            return transform(elem.text)
        except:
            return default

    nom = safe_extract('/html/body/div[3]/div/div/div[2]/div/div[1]/div[1]/div/div[2]/div[1]/h1/a')
    activite = safe_extract('/html/body/div[3]/div/div/div[2]/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/span', transform=unidecode)
    adresse = safe_extract('/html/body/div[3]/div/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[3]/div[1]', transform=unidecode)
    elem1 = safe_extract('/html/body/div[3]/div/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[4]/div/div[1]/table/tbody/tr[1]', transform=unidecode)
    elem2 = safe_extract('/html/body/div[3]/div/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[4]/div/div[1]/table/tbody/tr[2]', transform=unidecode)
    elem3 = safe_extract('/html/body/div[3]/div/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[4]/div/div[1]/table/tbody/tr[3]', transform=unidecode)
    elem4 = safe_extract('/html/body/div[3]/div/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[4]/div/div[1]/table/tbody/tr[4]', transform=unidecode)
    coordonnees = safe_extract('/html/body/div[3]/div/div/div[2]/div/div[3]/div[2]/div/div/div[1]/div[6]/div/div[1]/div')

    elems = [elem1, elem2, elem3, elem4]
    RC, ICE, FJ, Capital = 'N/A', 'N/A', 'N/A', 'N/A'
    for elem in elems:
        if elem.startswith('RC'):
            RC = elem[2:]
        elif elem.startswith('ICE'):
            ICE = elem[3:]
        elif elem.startswith('Forme'):
            FJ = elem[16:]
        elif elem.startswith('Capital'):
            Capital = elem[7:-3]

    try:
        adresse_part, ville = adresse.split(" - ")
        adresse = adresse_part[7:]
    except:
        ville = 'N/A'
        adresse = 'N/A'

    try:
        num, text = RC.split(" (")
        tribunal = text[:-1]
        RC = num
    except:
        tribunal = 'N/A'

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

# Combinaison des fichiers CSV en un seul fichier Excel
output_file = f'Output/Classement{n}_ordo.xlsx'

dfs = []

file_names = sorted([file_name for file_name in os.listdir('../Output') if file_name.endswith('.csv') and file_name.startswith('entreprises_')])

for file_name in file_names:
    file_path = os.path.join('../Output', file_name)
    df = pd.read_csv(file_path, dtype=str)
    df['Tribunal'] = df['Tribunal'].str.replace('Tribunal de ', '')
    print(f"Fichier : {file_name}, Colonnes : {df.columns.tolist()}")
    dfs.append(df)

combined_df = pd.concat(dfs, ignore_index=True)
combined_df = combined_df[combined_df["Nom de l'entreprise"] != 'N/A']
print(f"Colonnes du DataFrame combiné : {combined_df.columns.tolist()}")

combined_df.to_excel(output_file, index=False)

print(f"Les fichiers ont été combinés avec succès en {output_file}")
