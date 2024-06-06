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

csv_file = 'Res.csv'
output_csv_file = 'infos.csv'

with open(csv_file, 'r') as file:
    csv_reader = csv.reader(file)
    urls = [row[0] for row in csv_reader]

def extract_info(driver, url):
    driver.get(url)
    time.sleep(4)
    try:
        tradOk = driver.find_element(By.XPATH, '/html/body/div[9]/div/div/section/div/div/div[2]/div/div[1]/button')
        tradOk.click()
        time.sleep(2)
        boutonLangue = driver.find_element(By.XPATH,
                                           '/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/div/div/header/div/div[3]/nav/div[1]/div/button')
        boutonLangue.click()
        time.sleep(2)
        bouton_devise = driver.find_element(By.XPATH,
                                            '/html/body/div[9]/div/div/section/div/div/div[2]/div/div[2]/div/div[1]/div[1]/div/button[2]')
        bouton_devise.click()
        time.sleep(2)
        bouton_MAD = driver.find_element(By.XPATH,
                                         '/html/body/div[9]/div/div/section/div/div/div[2]/div/div[2]/div/div[2]/div[2]/section/div/ul/li[8]/button')
        bouton_MAD.click()
        time.sleep(6)
    except:
        pass
    try:
        nom_annonce = driver.find_element(By.XPATH, '//h1').text
        nom_annonce = unidecode(nom_annonce)
    except:
        nom_annonce = 'N/A'

    try:
        prix = driver.find_element(By.CSS_SELECTOR, '#site-content > div > div:nth-child(1) > div:nth-child(3) > div > div._1s21a6e2 > div > div > div:nth-child(1) > div > div > div > div > div > div > div > div._wgmchy > div._1k1ce2w > div > div > span > div > span._1y74zjx').text
        prix = unidecode(prix)
    except:
        prix = 'N/A'

    try:
        nom_hote = driver.find_element(By.CLASS_NAME, 't1pxe1a4').text
        nom_hote = unidecode(nom_hote)
    except:
        nom_hote = 'N/A'
    try:
        inscription_hote=driver.find_element(By.CSS_SELECTOR, '#site-content > div > div:nth-child(1) > div:nth-child(3) > div > div._16e70jgn > div > div:nth-child(2) > div:nth-child(2) > div > div > div > div.to1hkqq.atm_9s_1txwivl.atm_ar_1bp4okc.atm_fc_1h6ojuz.atm_cx_1y44olf.dir.dir-ltr > div.s1l7gi0l.atm_c8_km0zk7.atm_g3_18khvle.atm_fr_1m9t47k.atm_7l_1esdqks.dir.dir-ltr > ol > li').text
    except:
        inscription_hote = 'N/A'
    try:
        nb_comments= driver.find_element(By.CSS_SELECTOR, '#site-content > div > div:nth-child(1) > div._n0u29e9 > div > div > div > div:nth-child(2) > div > div > div > div > div > div > div._ixddx0 > div._176k0ns > span > span._1wl1dfc').text
    except:
        nb_comments = 'N/A'

    try:
        bouton_infos=driver.find_element(By.CSS_SELECTOR, "#site-content > div > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div > div > div > div > div > section > div > div._88xxct > div > div > div._c2acbp > button")
        bouton_infos.click()
        time.sleep(3)
        description=driver.find_element(By.XPATH, '/html/body/div[9]/div/div/section/div/div/div[2]/div/div[2]/section/div[1]/div').text
        description = unidecode(description)
    except:
        description = 'N/A'
    driver.get(url + '&modal=DESCRIPTION')
    time.sleep(3)
    try:
        infos_logement=driver.find_element(By.CSS_SELECTOR, 'body > div:nth-child(13) > div > div > section > div > div > div.p1psejvv.atm_9s_1bgihbq.dir.dir-ltr > div > div._1jza0fl > div > div > div > div > div > div > div > section > div:nth-child(3) > div > span').text
    except:
        try:
            infos_logement=driver.find_element(By.CSS_SELECTOR, 'body > div:nth-child(13) > div > div > section > div > div > div.p1psejvv.atm_9s_1bgihbq.dir.dir-ltr > div > div._1jza0fl > div > div > div > div > div > div > div > section > div._tp3sbt > div > span').text
        except:
            try:
                infos_logement=driver.find_element(By.XPATH, '/html/body/div[9]/div/div/section/div/div/div[2]/div/div[2]/div/div/div/div/div/div/div/section/div[3]/div').text
            except:
                infos_logement = 'N/A'

    type_annonce, ville,note,nb_chambres,nb_lits,nb_sdb= description.split('*')
    return [url, nom_hote,inscription_hote, ville,prix,nom_annonce,type_annonce,note,nb_comments,nb_chambres,nb_lits,nb_sdb,infos_logement]

if __name__ == "__main__":
    driver = create_driver()
    data = []
    for url in urls:
        info = extract_info(driver, url)
        data.append(info)
    with open(output_csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["url", 'Nom Hote', 'Inscrit depuis', 'Ville','Prix','Nom Annonce','Type Annonce','Note','Nombre de commentaires','Nombre Chambres','Nombre Lits','Nombre SDB','Description du logement'])
        writer.writerows(data)

    print(f"Les informations ont été sauvegardées dans {output_csv_file}")
    driver.quit()
