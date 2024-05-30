import csv
from unidecode import unidecode
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
#chrome_options.add_argument('--headless=new')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')


driver = webdriver.Chrome(options=chrome_options)

csv_file = '/Users/othmaneirhboula/webscraping/liste_entreprises/text/entreprises_marocaines.csv'


with open(csv_file, 'r') as file:
    csv_reader = csv.reader(file)
    companyname = [row[0] for row in csv_reader]
    urls = ['https://www.charika.ma/' + name for name in companyname]

data = []


def extract_info(driver, url):
    driver.get(url)
    time.sleep(6)
    elems=[]
    try:
        nom=driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div[1]/div[1]/div/div[2]/div[1]/h1/a').text
    except:
        nom='N/A'
    try:
        activite= driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/span').text
        activite = unidecode(activite)
    except:
        activite = 'N/A'
    try:
        adresse = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[3]/div[1]').text
        adresse = unidecode(adresse)
    except:
        adresse = 'N/A'
    try:
        elem1 = driver.find_element(By.XPATH,'/html/body/div[3]/div/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[4]/div/div[1]/table/tbody/tr[1]').text
        elem1= unidecode(elem1)
        elems.append(elem1)
    except:
        elem1 = 'N/A'
        elems.append(elem1)
    try:
        elem2 = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[4]/div/div[1]/table/tbody/tr[2]').text
        elem2 = unidecode(elem2)
        elems.append(elem2)
    except:
        elem2 = 'N/A'
        elems.append(elem2)
    try:
        elem3 = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[4]/div/div[1]/table/tbody/tr[3]').text
        elem3 = unidecode(elem3)
        elems.append(elem3)
    except:
        elem3 = 'N/A'
        elems.append(elem3)
    try:
        elem4 = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[4]/div/div[1]/table/tbody/tr[4]').text
        elem4 = unidecode(elem4)
        elems.append(elem4)
    except:
        elem4 = 'N/A'
        elems.append(elem4)
    try:
        boutoncoordonnes=driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div[3]/div[2]/div/div/div[1]/div[4]/img')
        time.sleep(1)
        boutoncoordonnes.click()
        time.sleep(2)
        coordonnees=driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div[3]/div[2]/div/div/div[1]/div[6]/div/div[1]/div').text
    except:
        coordonnees='N/A'
    RC,ICE,FJ,Capital='N/A','N/A','N/A','N/A'
    for elem in elems:
        if elem[0] == 'R':
            RC = elem
        elif elem[0] == 'I':
            ICE = elem
        elif elem[0] == 'F':
            FJ = elem
        elif elem[0] == 'C':
            Capital = elem
    activite=activite[10:]
    adresse=adresse[7:]
    RC=RC[2:]
    ICE=ICE[3:]
    FJ=FJ[16:]
    Capital=Capital[7:-3]
    num, text = RC.split(" (")
    text = text[:-1]
    RC = num
    tribunal = text
    try:
        adresse_part, ville = adresse.split(" - ")
        adresse = adresse_part
    except:
        ville = 'N/A'
        adresse = 'N/A'
    return [nom, activite, adresse, ville, coordonnees, RC,tribunal, ICE, FJ, Capital]

try:
    driver.get('https://charika.ma/')
    time.sleep(3)

    premier_bouton = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div[1]/ul/li[4]/a/b')
    premier_bouton.click()
    time.sleep(1)
    deuxieme_bouton = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div[1]/ul/li[4]/ul/div/div/div/div[1]/a/button')
    deuxieme_bouton.click()
    time.sleep(1)

    id = driver.find_element(By.XPATH, '/html/body/div[10]/div/div/div/div/div[1]/div[2]/div/div/form/div[1]/input')
    id.click()
    id.send_keys('yoyotirpsn4@gmail.com')

    mdp = driver.find_element(By.XPATH, '/html/body/div[10]/div/div/div/div/div[1]/div[2]/div/div/form/div[2]/input')
    mdp.click()
    mdp.send_keys('webscraping1')

    troisieme_bouton = driver.find_element(By.XPATH, '/html/body/div[10]/div/div/div/div/div[1]/div[2]/div/div/form/button')
    troisieme_bouton.click()

    time.sleep(5)

    cookies = driver.get_cookies()
    i=0
    for url in urls:
        driver.delete_all_cookies()
        for cookie in cookies:
            driver.add_cookie(cookie)
        print(i)
        i+=1
        info = extract_info(driver, url)
        data.append(info)

finally:
    driver.quit()

    output_csv_file = 'infos_entreprises_bis.csv'
    with open(output_csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Nom de l'entreprise", 'Activite', 'Adresse','Ville','Coordonnees geographiques', 'RC','Tribunal', 'ICE', 'Forme Juridique', 'Capital'])
        for row in data:
            writer.writerow(row)

    print(f"Les informations ont été sauvegardées dans {output_csv_file}")
