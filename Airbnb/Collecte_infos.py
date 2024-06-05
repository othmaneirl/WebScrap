import csv
from unidecode import unidecode
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
output_csv_file = 'infos2.csv'

with open(csv_file, 'r') as file:
    csv_reader = csv.reader(file)
    urls = [row[0] for row in csv_reader]

def extract_info(driver, url):
    driver.get(url)
    time.sleep(8)  # Augmentez le délai si nécessaire
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
        prix = driver.find_element(By.CSS_SELECTOR, '._1y74zjx').text
        prix = unidecode(prix)
    except:
        prix = 'N/A'

    try:
        adresse = driver.find_element(By.CSS_SELECTOR, '._152qbzi').text
        adresse = unidecode(adresse)
    except:
        adresse = 'N/A'

    try:
        nom_hote = driver.find_element(By.CLASS_NAME, 't1pxe1a4').text
        nom_hote = unidecode(nom_hote)
    except:
        nom_hote = 'N/A'

    try:
        note = driver.find_element(By.CLASS_NAME, '_18khxk1').text
        note = unidecode(note)
    except:
        note = 'N/A'

    return [nom_annonce, nom_hote, prix, adresse, note]

if __name__ == "__main__":
    driver = create_driver()
    data = []
    for url in urls:
        info = extract_info(driver, url)
        data.append(info)
    with open(output_csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Annonce", 'Nom Hote', 'Prix', 'Adresse', 'Note sur 5'])
        writer.writerows(data)

    print(f"Les informations ont été sauvegardées dans {output_csv_file}")
    driver.quit()
