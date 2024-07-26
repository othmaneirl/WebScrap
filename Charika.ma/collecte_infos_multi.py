# Ce code permet d'extraire les informations des entreprises disponibles sur charika.ma en utilisant le module selenium et le multiprocessing pour accélérer le processus

# 100 sites scrapés en 1 minute 30
import csv
import multiprocessing
import os
from unidecode import unidecode
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def create_driver():
    geckodriver_path = '/Users/othmaneirhboula/webscraping/geckodriver'
    options = Options()
    options.headless = False
    profile = webdriver.FirefoxProfile()
    profile.set_preference('permissions.default.image', 2)           #
    profile.set_preference('network.proxy.type', 1)                  #
    profile.set_preference('network.proxy.socks', '127.0.0.1')       # activation du proxy sur le driver selenium
    profile.set_preference('network.proxy.socks_port', 9150)         # pour éviter les blocages du site
    profile.set_preference('network.proxy.socks_version', 5)         #
    profile.set_preference('network.proxy.socks_remote_dns', True)   #
    profile.update_preferences()
    options.profile = profile
    service = Service(geckodriver_path)
    driver = webdriver.Firefox(service=service, options=options)
    return driver



csv_file = 'filtered_url.csv'
output_csv_file1 = 'Output/test.csv'
output_csv_file = output_csv_file1[7:]
with open(csv_file, 'r') as file:
    csv_reader = csv.reader(file)
    urls = [row[0] for row in csv_reader]

#ici on divise la liste des urls en 4 parties en préparation pour le multiprocessing
quart = len(urls) // 4
urls_part1 = urls[:quart]
urls_part2 = urls[quart:2 * quart]
urls_part3 = urls[2 * quart:3 * quart]
urls_part4 = urls[3 * quart:]


def extract_info(driver, url):   #fonction qui permet d'extraire les informations d'une entreprise à partir de son url, toutes les informations sont extraites grace à l'xpath
    driver.get(url)
    wait = WebDriverWait(driver, 10)  # le driver attendra au maximum 10 secondes avant de renvoyer une erreur

    elems = [] # liste qui permettra de stocker les élements non identifiés
    try:
        nom = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div[1]/div[1]/div/div[2]/div[1]/h1/a'))).text
    except:
        nom = 'N/A'
    try:
        activite = driver.find_element(By.XPATH,'/html/body/div[3]/div/div/div[2]/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/span').text
        activite = unidecode(activite)
    except:
        activite = 'N/A'
    try:
        adresse = driver.find_element(By.XPATH,'/html/body/div[3]/div/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[3]/div[1]').text
        adresse = unidecode(adresse)
    except:
        adresse = 'N/A'
    try:
        elem1 = driver.find_element(By.XPATH,'/html/body/div[3]/div/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[4]/div/div[1]/table/tbody/tr[1]').text
        elem1 = unidecode(elem1)
        elems.append(elem1)
    except:
        elem1 = 'N/A'
        elems.append(elem1)
    try:
        elem2 = driver.find_element(By.XPATH,'/html/body/div[3]/div/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[4]/div/div[1]/table/tbody/tr[2]').text
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
        #ici on cherche à récuperer les coordonnées géographiques de chaque entreprise
        boutoncoordonnes = driver.find_element(By.XPATH,'/html/body/div[3]/div/div/div[2]/div/div[3]/div[2]/div/div/div[1]/div[4]/img') #le bouton qui permet d'afficher les coordonnées
        boutoncoordonnes.click()
        coordonnees = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div[3]/div[2]/div/div/div[1]/div[6]/div/div[1]/div'))).text #on attend que les coordonnées soient affichées et on les stocke dans la variable coordonnees
    except:
        coordonnees = 'N/A'

    RC, ICE, FJ, Capital = 'N/A', 'N/A', 'N/A', 'N/A'
    for elem in elems:  #on parcourt la liste des élements non identifiés pour les identifier grace des conditions simples
        if elem.startswith('RC'):
            RC = elem
        elif elem.startswith('ICE'):
            ICE = str(elem)
        elif elem.startswith('Forme Juridique'):
            FJ = elem
        elif elem.startswith('Capital'):
            Capital = elem

    activite = activite[10:] #
    adresse = adresse[7:]    #
    ICE = ICE[3:]            # on nettoie les données pour ne garder que les parties utiles
    FJ = FJ[16:]             #
    Capital = Capital[7:-3]  #
    try:  #on essaye de séparer le numéro RC du tribunal
        num, text = RC.split(" (")
        RC = num
        tribunal = text[:-1]
        tribunal = 'N/A'
    except:
        tribunal = 'N/A'
    try:   #on essaye de séparer l'adresse de la ville
        adresse_part, ville = adresse.split(" - ")
        adresse = adresse_part
    except:
        ville = 'N/A'
        adresse = 'N/A'
    return [nom, activite, adresse, ville, coordonnees, RC, tribunal, ICE, FJ, Capital]   #on retourne les informations dans une liste


def scrape_part(urls, output_file, start_index=0):   #fonction qui permet de scraper les urls à partir d'un index donné et d'enregistrer les données scrappées dans un fichier xlsx
    driver = create_driver()
    try: #on essaye de se connecter au site charika.ma
        driver.get('https://charika.ma/')
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div[1]/ul/li[4]/a/b'))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div[1]/ul/li[4]/ul/div/div/div/div[1]/a/button'))).click()
        id = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[10]/div/div/div/div/div[1]/div[2]/div/div/form/div[1]/input')))
        id.send_keys('yoyotirpsn4@gmail.com')  #on remplit les champs de connexion
        mdp = driver.find_element(By.XPATH, '/html/body/div[10]/div/div/div/div/div[1]/div[2]/div/div/form/div[2]/input')
        mdp.send_keys('webscraping1')  #on remplit les champs de connexion
        driver.find_element(By.XPATH, '/html/body/div[10]/div/div/div/div/div[1]/div[2]/div/div/form/button').click()
        cookies = driver.get_cookies() #on récupère les cookies de la session pour pouvoir les charger ensuite et rester connecté

        with open("Output/" + output_file, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if start_index == 0:
                writer.writerow(["Nom de l'entreprise", 'Activite', 'Adresse', 'Ville', 'Coordonnees geographiques', 'Numero RC','Tribunal', 'ICE', 'Forme Juridique', 'Capital'])
            for i, url in enumerate(urls[start_index:], start=start_index):
                driver.delete_all_cookies() #on supprime les cookies pour éviter les erreurs
                for cookie in cookies:
                    driver.add_cookie(cookie) #on charge les cookies pour rester connecté
                info = extract_info(driver, url)
                writer.writerow(info)
    finally:
        driver.quit()


def get_last_processed_index(output_file):  #fonction qui permet de récupérer l'index de la dernière entreprise traitée pour pouvoir reprendre le scraping sans recommencer depuis le début
    if not os.path.exists("Output/" + output_file):
        return 0
    with open("Output/" + output_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        return sum(1 for row in reader) - 1 #on retourne l'index de la dernière entreprise traitée


if __name__ == "__main__":
    manager = multiprocessing.Manager()    #on crée un manager pour gérer les processus
     #on récupère les derniers index traités par chaque instance
    start_index1 = get_last_processed_index(f'part1_{output_csv_file}')
    start_index2 = get_last_processed_index(f'part2_{output_csv_file}')
    start_index3 = get_last_processed_index(f'part3_{output_csv_file}')
    start_index4 = get_last_processed_index(f'part4_{output_csv_file}')
     #on crée 4 processus pour traiter les urls en parallèle
    process1 = multiprocessing.Process(target=scrape_part, args=(urls_part1, f'part1_{output_csv_file}', start_index1))
    process2 = multiprocessing.Process(target=scrape_part, args=(urls_part2, f'part2_{output_csv_file}', start_index2))
    process3 = multiprocessing.Process(target=scrape_part, args=(urls_part3, f'part3_{output_csv_file}', start_index3))
    process4 = multiprocessing.Process(target=scrape_part, args=(urls_part4, f'part4_{output_csv_file}', start_index4))
     #on démarre les processus
    process1.start()
    process2.start()
    process3.start()
    process4.start()
     #on attend que les processus se terminent pour fusionner les fichiers csv
    process1.join()
    process2.join()
    process3.join()
    process4.join()
        #on fusionne les fichiers csv
    with open(output_csv_file1, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(
            ["Nom de l'entreprise", 'Activite', 'Adresse', 'Ville', 'Coordonnees geographiques', 'Numero RC',
             'Tribunal', 'ICE', 'Forme Juridique', 'Capital'])
        for part_file in [f'Output/part1_{output_csv_file}', f'Output/part2_{output_csv_file}',
                          f'Output/part3_{output_csv_file}', f'Output/part4_{output_csv_file}']:
            with open(part_file, 'r', newline='', encoding='utf-8') as infile:
                reader = csv.reader(infile)
                next(reader)
                for row in reader:
                    writer.writerow(row)

    print(f"Les informations ont été sauvegardées dans {output_csv_file1}")
