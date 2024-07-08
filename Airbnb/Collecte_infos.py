import csv
from unidecode import unidecode
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
import time

def create_driver():
    geckodriver_path = '/Users/othmaneirhboula/webscraping/geckodriver'
    options = FirefoxOptions()
    options.headless = False

    profile = webdriver.FirefoxProfile()
    options.profile = profile
    service = Service(geckodriver_path)

    driver = webdriver.Firefox(service=service, options=options)
    return driver

def extract_info(driver, url):
    driver.get(url)
    time.sleep(4)

    try:
        tradOk = driver.find_element(By.XPATH, '/html/body/div[9]/div/div/section/div/div/div[2]/div/div[1]/button')
        tradOk.click()
        time.sleep(2)

        boutonLangue = driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/div/div/header/div/div[3]/nav/div[1]/div/button')
        boutonLangue.click()
        time.sleep(2)

        bouton_devise = driver.find_element(By.XPATH, '/html/body/div[9]/div/div/section/div/div/div[2]/div/div[2]/div/div[1]/div[1]/div/button[2]')
        bouton_devise.click()
        time.sleep(2)

        bouton_MAD = driver.find_element(By.XPATH, '/html/body/div[9]/div/div/section/div/div/div[2]/div/div[2]/div/div[2]/div[2]/section/div/ul/li[8]/button')
        bouton_MAD.click()
        time.sleep(6)
    except Exception as e:
        print(f"Erreur lors de l'interaction avec les boutons: {e}")

    try:
        nom_annonce = driver.find_element(By.XPATH, '//h1').text
        nom_annonce = unidecode(nom_annonce)
    except:
        nom_annonce = 'N/A'

    try:
        nom_hote = driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/div/div/header/div/div[2]/div[1]/div/div/div/div/a/span').text
        nom_hote = unidecode(nom_hote)
    except:
        nom_hote = 'N/A'

    try:
        inscription_hote = driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/div/div/header/div/div[2]/div[1]/div/div/span').text
        inscription_hote = unidecode(inscription_hote)
    except:
        inscription_hote = 'N/A'

    try:
        ville = driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/div/div/header/div/div[2]/div[1]/div/div[1]/span').text
        ville = unidecode(ville)
    except:
        ville = 'N/A'

    try:
        prix = driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/div/div/header/div/div[2]/div[2]/div/div/div/span').text
        prix = unidecode(prix)
    except:
        prix = 'N/A'

    try:
        note = driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/div/div/header/div/div[3]/div/div/div/span[1]').text
        note = unidecode(note)
    except:
        note = 'N/A'

    try:
        nb_comments = driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/div/div/header/div/div[3]/div/div/div/span[2]').text
        nb_comments = unidecode(nb_comments)
    except:
        nb_comments = 'N/A'

    try:
        description = driver.find_element(By.XPATH, '/html/body/div[9]/div/div/section/div/div/div[2]/div/div[2]/section/div[1]/div').text
        description = unidecode(description)
    except:
        description = 'N/A'

    driver.get(url + '&modal=DESCRIPTION')
    time.sleep(3)

    try:
        infos_logement = driver.find_element(By.CSS_SELECTOR, 'body > div:nth-child(13) > div > div > section > div > div > div.p1psejvv.atm_9s_1bgihbq.dir.dir-ltr > div > div._1jza0fl > div > div > div > div > div > div > div > section > div:nth-child(3) > div > span').text
    except:
        try:
            infos_logement = driver.find_element(By.CSS_SELECTOR, 'body > div:nth-child(13) > div > div > section > div > div > div.p1psejvv.atm_9s_1bgihbq.dir.dir-ltr > div > div._1jza0fl > div > div > div > div > div > div > div > section > div._tp3sbt > div > span').text
        except:
            try:
                infos_logement = driver.find_element(By.XPATH, '/html/body/div[9]/div/div/section/div/div/div[2]/div/div[2]/div/div/div/div/div/div/div/section/div[3]/div').text
            except:
                infos_logement = 'N/A'

    type_annonce, nb_chambres, nb_lits, nb_sdb = description.split('*')
    return [nom_hote, inscription_hote, ville, prix, nom_annonce, type_annonce, note, nb_comments, nb_chambres, nb_lits, nb_sdb, infos_logement,url]

if __name__ == "__main__":
    csv_file = 'Res.csv'
    output_csv_file = 'infos.csv'

    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        urls = [row[0] for row in csv_reader]

    driver = create_driver()
    data = []
    for url in urls:
        info = extract_info(driver, url)
        data.append(info)

    with open(output_csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([ "Nom Hote", "Inscrit depuis", "Ville", "Prix", "Nom Annonce", "Type Annonce", "Note", "Nombre de commentaires", "Nombre Chambres", "Nombre Lits", "Nombre SDB", "Description du logement", "URL"])
        writer.writerows(data)

    print(f"Les informations ont été sauvegardées dans {output_csv_file}")
    driver.quit()
