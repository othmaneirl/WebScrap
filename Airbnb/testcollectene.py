import requests
from bs4 import BeautifulSoup

# URL du site web
url = 'https://www.airbnb.fr/s/Maroc/homes?place_id=ChIJjcVRlmGICw0Rw_8sxIGT09k&refinement_paths%5B%5D=%2Fhomes&date_picker_type=monthly_stay&search_type=user_map_move&tab_id=home_tab&query=Maroc&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-07-01&monthly_length=1&monthly_end_date=2024-10-01&search_mode=regular_search&price_filter_input_type=0&channel=EXPLORE&source=structured_search_input_header&price_filter_num_nights=31&ne_lat=34.96590420464777&ne_lng=-6.584552050869888&sw_lat=32.21966057766953&sw_lng=-8.808944168726725&zoom=8.349822115491813&zoom_level=8.349822115491813&search_by_map=true'

# Faire une requête HTTP pour obtenir le contenu de la page
response = requests.get(url)
html_content = response.text

# Analyser le contenu HTML avec BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Trouver toutes les balises <a> qui contiennent les annonces
# Généralement les liens des annonces Airbnb sont dans des balises <a> avec un href contenant 'rooms'
links = soup.find_all('a', href=True)
urls = [link['href'] for link in links if 'rooms' in link['href']]

# Ajouter le domaine de base s'il manque dans l'URL
base_url = "https://www.airbnb.fr"
full_urls = [url if url.startswith('http') else base_url + url for url in urls]

# Afficher les URLs
print(urls)
