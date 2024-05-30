import csv
from unidecode import unidecode
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import multiprocessing
import os

def create_driver():
    chrome_options = Options()
    #chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    return webdriver.Chrome(options=chrome_options)

csv_file = 'Input/liste_des_entreprises.csv'
output_csv_file = 'Output/infos_entreprises_final.csv'

with open(csv_file, 'r') as file:
    csv_reader = csv.reader(file)
    urls = [row[0] for row in csv_reader]

# Split the URLs into five parts
fifth_index = len(urls) // 4
urls_part1 = urls[:fifth_index]
urls_part2 = urls[fifth_index:2*fifth_index]
urls_part3 = urls[2*fifth_index:3*fifth_index]
urls_part4 = urls[3*fifth_index:]

def extract_info(driver, url):
    driver.get(url)
    time.sleep(2)
    elems = []
    try:
        nom = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div[1]/div[1]/div/div[2]/div[1]/h1/a').text
    except:
        nom = 'N/A'
    try:
        activite = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/span').text
        activite = unidecode(activite)
    except:
        activite = 'N/A'
    try:
        adresse = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[3]/div[1]').text
        adresse = unidecode(adresse)
    except:
        adresse = 'N/A'
    try:
        elem1 = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[4]/div/div[1]/table/tbody/tr[1]').text
        elem1 = unidecode(elem1)
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
        boutoncoordonnes = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div[3]/div[2]/div/div/div[1]/div[4]/img')
        boutoncoordonnes.click()
        time.sleep(2)
        coordonnees = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div[3]/div[2]/div/div/div[1]/div[6]/div/div[1]/div').text
    except:
        coordonnees = 'N/A'
    RC, ICE, FJ, Capital = 'N/A', 'N/A', 'N/A', 'N/A'
    for elem in elems:
        if elem[0] == 'R':
            RC = elem
        elif elem[0] == 'I':
            ICE = str(elem)
        elif elem[0] == 'F':
            FJ = elem
        elif elem[0] == 'C':
            Capital = elem

    activite = activite[10:]
    adresse = adresse[7:]
    RC = RC[2:]
    ICE = ICE[3:]
    FJ = FJ[16:]
    Capital = Capital[7:-3]
    num, text = RC.split(" (")
    RC = num
    tribunal = text[:-1]
    try:
        adresse_part, ville = adresse.split(" - ")
        adresse = adresse_part
    except:
        ville = 'N/A'
        adresse = 'N/A'
    return [nom, activite, adresse, ville, coordonnees, RC, tribunal, ICE, FJ, Capital]

def scrape_part(urls, output_file, start_index=0):
    driver = create_driver()
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

        with open("Output/"+output_file, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if start_index == 0:
                writer.writerow(["Nom de l'entreprise", 'Activite', 'Adresse', 'Ville', 'Coordonnees geographiques', 'Numero RC', 'Tribunal', 'ICE', 'Forme Juridique', 'Capital'])
            for i, url in enumerate(urls[start_index:], start=start_index):
                driver.delete_all_cookies()
                for cookie in cookies:
                    driver.add_cookie(cookie)
                print(f"Processing URL {i} in process {multiprocessing.current_process().name}")
                info = extract_info(driver, url)
                writer.writerow(info)
    finally:
        driver.quit()

def get_last_processed_index(output_file):
    if not os.path.exists("Output/"+output_file):
        return 0
    with open("Output/"+output_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        return sum(1 for row in reader) - 1  # Subtract 1 for the header row

if __name__ == "__main__":
    manager = multiprocessing.Manager()

    start_index1 = get_last_processed_index(f'part1_{output_csv_file}')
    start_index2 = get_last_processed_index(f'part2_{output_csv_file}')
    start_index3 = get_last_processed_index(f'part3_{output_csv_file}')
    start_index4 = get_last_processed_index(f'part4_{output_csv_file}')

    process1 = multiprocessing.Process(target=scrape_part, args=(urls_part1, f'part1_{output_csv_file}', start_index1))
    process2 = multiprocessing.Process(target=scrape_part, args=(urls_part2, f'part2_{output_csv_file}', start_index2))
    process3 = multiprocessing.Process(target=scrape_part, args=(urls_part3, f'part3_{output_csv_file}', start_index3))
    process4 = multiprocessing.Process(target=scrape_part, args=(urls_part4, f'part4_{output_csv_file}', start_index4))

    process1.start()
    process2.start()
    process3.start()
    process4.start()

    process1.join()
    process2.join()
    process3.join()
    process4.join()

    # Combine all parts into the final CSV file
    with open(output_csv_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["Nom de l'entreprise", 'Activite', 'Adresse', 'Ville', 'Coordonnees geographiques', 'RC', 'Tribunal', 'ICE', 'Forme Juridique', 'Capital'])
        for part_file in [f'Output/part1_{output_csv_file}', f'Output/part2_{output_csv_file}', f'Output/part3_{output_csv_file}', f'Output/part4_{output_csv_file}']:
            with open(part_file, 'r', newline='', encoding='utf-8') as infile:
                reader = csv.reader(infile)
                next(reader)  # Skip header row
                for row in reader:
                    writer.writerow(row)

    print(f"Les informations ont été sauvegardées dans {output_csv_file}")
