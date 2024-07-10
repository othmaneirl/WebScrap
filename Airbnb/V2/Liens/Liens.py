import requests
from bs4 import BeautifulSoup
import csv

def extract_links_and_articles(url):
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = session.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []
    soup = BeautifulSoup(response.text, 'html.parser')
    a_tags = soup.find_all('a', class_='sc-dadxi2-0 fCSoyD')
    links_and_articles = []
    links=[]
    for a in a_tags:
        link = a.get('href')
        if link and link.startswith('/room'):
            links_and_articles.append(link)
    return links

# liens = []
# for i in range(1, 10): # Nombre de pages à parcourir
#     url = f'https://www.avito.ma/fr/boutiques/maroc/market-%C3%A0_vendre?o={i}'
#     links_and_articles = extract_links_and_articles(url)
#     for link, num_articles in links_and_articles:
#         liens.append((link, num_articles))
#
# with open('/Users/othmaneirhboula/WebScrap/Avito/Liens/LiensBoutiquesArticles.csv', mode='w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(['URL', 'Nombre d\'articles'])
#     for line in liens:
#         if line[0]!="https://www.avito.ma/fr/boutiques/maroc" or line[0]!="https://www.avito.ma/fr/boutiques/maroc/":
#             writer.writerow(line)
#
# print(f"Les données ont été enregistrées dans LiensBoutiques.csv")
print(extract_links_and_articles("https://www.airbnb.fr/s/Morocco/homes?place_id=ChIJjcVRlmGICw0Rw_8sxIGT09k&refinement_paths%5B%5D=%2Fhomes&tab_id=home_tab&query=Morocco&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-08-01&monthly_length=3&monthly_end_date=2024-11-01&search_mode=regular_search&price_filter_input_type=0&channel=EXPLORE&search_type=user_map_move&price_filter_num_nights=5&ne_lat=33.542768989335556&ne_lng=-6.112791161120981&sw_lat=31.160052913419356&sw_lng=-7.997955857931771&zoom=8.575025608326142&zoom_level=8.575025608326142&search_by_map=true"))
