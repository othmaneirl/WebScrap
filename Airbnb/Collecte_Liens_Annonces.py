import csv
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
import requests
import bs4

url='https://www.airbnb.fr/?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&search_mode=flex_destinations_search&flexible_trip_lengths%5B%5D=one_week&location_search=MIN_MAP_BOUNDS&monthly_start_date=2024-06-01&monthly_length=3&monthly_end_date=2024-09-01&price_filter_input_type=0&channel=EXPLORE&search_type=category_change&price_filter_num_nights=5&category_tag=Tag%3A8536'

def create_driver():
    geckodriver_path = '/Users/othmaneirhboula/webscraping/geckodriver'
    options = Options()
    options.headless = False

    profile = webdriver.FirefoxProfile()
    # profile.set_preference('permissions.default.image', 2)
    # profile.set_preference('network.proxy.type', 1)
    # profile.set_preference('network.proxy.socks', '127.0.0.1')
    # profile.set_preference('network.proxy.socks_port', 9150)
    # profile.set_preference('network.proxy.socks_version', 5)
    # profile.set_preference('network.proxy.socks_remote_dns', True)
    # profile.update_preferences()

    options.profile = profile
    service = Service(geckodriver_path)

    driver = webdriver.Firefox(service=service, options=options)
    return driver

driver= create_driver()
driver.get(url)
time.sleep(4)

# Scroll to 70% of the page height
page_height = driver.execute_script("return document.body.scrollHeight")
scroll_height = page_height * 0.7
driver.execute_script(f"window.scrollTo(0, {page_height * 0.7});")
time.sleep(5)
driver.execute_script(f"window.scrollTo(0, {page_height * 0.3});")
time.sleep(7)
driver.execute_script(f"window.scrollTo(0, {page_height * 0.2});")
time.sleep(7)
driver.execute_script(f"window.scrollTo(0, {page_height * 0.4});")
time.sleep(5)
driver.execute_script(f"window.scrollTo(0, {page_height * 0.6});")
time.sleep(3)

bouton_plus=driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div[1]/div/div[3]/main/div[2]/div/div/div/div/div[3]/div[2]/button')
bouton_plus.click()
time.sleep(5)

# Use the driver to get the page content
content = driver.page_source

# Analyser le contenu HTML avec BeautifulSoup
soup = bs4.BeautifulSoup(content, 'html.parser')

# Sélectionner tous les éléments <div> avec la classe spécifiée
div_elements = soup.find_all('div', class_='c14whb16 atm_8w_je46wd atm_90_wqqh0j atm_93_16tozh0 atm_9s_11p5wf0 atm_d5_1bp4okc atm_d3_8n3s54 atm_cx_dfedth atm_e0_1fe5oxz atm_dy_kim48s atm_fc_1y6m0gg atm_gi_idpfg4 atm_j6_mtsehg atm_e2_1kjme8w atm_ks_ndwtr5 atm_l4_1f51e7f atm_ld_5ul63a atm_lc_djs5a5 atm_lj_wg387a atm_li_1y0adu4 atm_o3_1p5gfer atm_p9_glywfm atm_tl_19lnvtn atm_or_dhnz5w__ta18iu atm_9s_glywfm_14pyf7n atm_oa_2geptf_bqoj1z atm_oq_1vwytc5_bqoj1z dir dir-ltr')

# Extraire les liens des éléments <a> à l'intérieur des <div> sélectionnés
links = []
for div in div_elements:
    a_tags = div.find_all('a', href=True)
    for a in a_tags:
        if a['href'] in links:
            continue
        else:
            links.append(a['href'])

# Enregistrer les liens dans un fichier CSV
csv_filename = 'links.csv'
with open(csv_filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Link'])
    for link in links:
        writer.writerow([link])
driver.quit()
print(f"Les liens ont été enregistrés dans le fichier {csv_filename}")
