import requests
from bs4 import BeautifulSoup
import csv

def extract_links_and_articles(url):
    # Créer une session
    session = requests.Session()

    # Définir les en-têtes HTTP pour imiter un navigateur
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Envoyer une requête GET à l'URL avec les en-têtes et la session
    response = session.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []

    # Parser le contenu HTML avec BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Trouver toutes les balises <a> correspondant aux boutiques
    a_tags = soup.find_all('a', class_='sc-dadxi2-0 fCSoyD')

    # Extraire les liens href et le nombre d'articles
    links_and_articles = []
    for a in a_tags:
        link = a.get('href')
        if link and link.startswith('https://www.avito.ma/fr/bou'):
            articles_div = a.find('p', class_='sc-1x0vz2r-0 jCAaeV sc-dadxi2-13 cJDqxX')
            num_articles = articles_div.text.strip() if articles_div else '0 Articles'
            links_and_articles.append((link, num_articles))
    return links_and_articles

liens = []
# URL à examiner
for i in range(1, 10):
    url = f'https://www.avito.ma/fr/boutiques/maroc/market-%C3%A0_vendre?o={i}'
    links_and_articles = extract_links_and_articles(url)
    for link, num_articles in links_and_articles:
        liens.append((link, num_articles))

# Afficher les liens et les nombres d'articles extraits
print(len(liens))

# Enregistrer les données dans un fichier CSV
with open('/Users/othmaneirhboula/WebScrap/Avito/Liens/LiensBoutiquesArticles.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['URL', 'Nombre d\'articles'])  # Ajouter les en-têtes des colonnes
    for line in liens:
        if line[0]!="https://www.avito.ma/fr/boutiques/maroc" or line[0]!="https://www.avito.ma/fr/boutiques/maroc/":
            writer.writerow(line)

print(f"Les données ont été enregistrées dans LiensBoutiques.csv")
