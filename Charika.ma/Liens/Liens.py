# Ce code permet de scraper les urls de chaque entreprise disponible sur charika.ma avec bs4
import os
import csv
import requests
from bs4 import BeautifulSoup
import time

# Fonction pour charger les éléments déjà extraits
def load_elements(csv_file_path):
    if os.path.exists(csv_file_path):
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            return {row[0] for row in reader}
    return set()

# Fonction pour sauvegarder les résultats
def save_elements(csv_file_path, elements):
    with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for element in elements:
            writer.writerow([element])

# Fonction pour scrapper les URLs dans une plage d'IDs
def scrape_urls(start_id, end_id, csv_file_path, processed_ids):
    local_elements = set()
    for i in range(start_id, end_id):
        if str(i) in processed_ids:
            continue
        url = f"https://www.charika.ma/societes-{i}"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            links = soup.find_all('a', class_='goto-fiche')
            for link in links:
                element_id = link.get('id')
                if element_id and element_id not in processed_ids:
                    local_elements.add(element_id)
                    processed_ids.add(element_id)
            # Sauvegarder périodiquement les résultats locaux
            if len(local_elements) >= 10:
                save_elements(csv_file_path, local_elements)
                local_elements.clear()
        else:
            print(f"Erreur lors de l'accès à l'URL: {url}")
        print(i)

        # Attendre pour éviter de surcharger le serveur
        time.sleep(1)

    # Sauvegarder les résultats restants
    if local_elements:
        save_elements(csv_file_path, local_elements)

# Chemin du fichier CSV
csv_output_folder = "/Users/othmaneirhboula/webscraping/liste_entreprises/text"
os.makedirs(csv_output_folder, exist_ok=True)
csv_file_path = os.path.join(csv_output_folder, 'entreprises_marocaines_bs3.csv')

# Charger les éléments déjà extraits
processed_ids = load_elements(csv_file_path)

# Définir la plage d'IDs pour le scraping
start_id = 1
end_id = 87611

# Effectuer le scraping
scrape_urls(start_id, end_id, csv_file_path, processed_ids)

print(f"Extraction terminée. Les résultats sont enregistrés dans {csv_file_path}")
