import csv
from unidecode import unidecode
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import bs4

chrome_options = Options()
#chrome_options.add_argument('--headless=new')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')


driver = webdriver.Chrome(options=chrome_options)
time.sleep(4)
links = []
# Scroll to 70% of the page height
urls=['https://www.airbnb.fr/s/Maroc/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-07-01&monthly_length=3&monthly_end_date=2024-10-01&price_filter_input_type=0&channel=EXPLORE&query=Maroc&place_id=ChIJjcVRlmGICw0Rw_8sxIGT09k&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click&search_mode=regular_search&price_filter_num_nights=5&federated_search_session_id=ed682609-e85b-4889-9472-bc79b4291b70&pagination_search=true&cursor=eyJzZWN0aW9uX29mZnNldCI6MCwiaXRlbXNfb2Zmc2V0IjowLCJ2ZXJzaW9uIjoxfQ%3D%3D',
      'https://www.airbnb.fr/s/Maroc/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-07-01&monthly_length=3&monthly_end_date=2024-10-01&price_filter_input_type=0&channel=EXPLORE&query=Maroc&place_id=ChIJjcVRlmGICw0Rw_8sxIGT09k&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click&search_mode=regular_search&price_filter_num_nights=5&federated_search_session_id=ed682609-e85b-4889-9472-bc79b4291b70&pagination_search=true&cursor=eyJzZWN0aW9uX29mZnNldCI6MCwiaXRlbXNfb2Zmc2V0IjoxOCwidmVyc2lvbiI6MX0%3D',
      'https://www.airbnb.fr/s/Maroc/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-07-01&monthly_length=3&monthly_end_date=2024-10-01&price_filter_input_type=0&channel=EXPLORE&query=Maroc&place_id=ChIJjcVRlmGICw0Rw_8sxIGT09k&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click&search_mode=regular_search&price_filter_num_nights=5&federated_search_session_id=ed682609-e85b-4889-9472-bc79b4291b70&pagination_search=true&cursor=eyJzZWN0aW9uX29mZnNldCI6MCwiaXRlbXNfb2Zmc2V0IjozNiwidmVyc2lvbiI6MX0%3D',
      'https://www.airbnb.fr/s/Maroc/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-07-01&monthly_length=3&monthly_end_date=2024-10-01&price_filter_input_type=0&channel=EXPLORE&query=Maroc&place_id=ChIJjcVRlmGICw0Rw_8sxIGT09k&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click&search_mode=regular_search&price_filter_num_nights=5&federated_search_session_id=ed682609-e85b-4889-9472-bc79b4291b70&pagination_search=true&cursor=eyJzZWN0aW9uX29mZnNldCI6MCwiaXRlbXNfb2Zmc2V0Ijo1NCwidmVyc2lvbiI6MX0%3D',
      'https://www.airbnb.fr/s/Maroc/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-07-01&monthly_length=3&monthly_end_date=2024-10-01&price_filter_input_type=0&channel=EXPLORE&query=Maroc&place_id=ChIJjcVRlmGICw0Rw_8sxIGT09k&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click&search_mode=regular_search&price_filter_num_nights=5&federated_search_session_id=ed682609-e85b-4889-9472-bc79b4291b70&pagination_search=true&cursor=eyJzZWN0aW9uX29mZnNldCI6MCwiaXRlbXNfb2Zmc2V0Ijo3MiwidmVyc2lvbiI6MX0%3D',
      'https://www.airbnb.fr/s/Maroc/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-07-01&monthly_length=3&monthly_end_date=2024-10-01&price_filter_input_type=0&channel=EXPLORE&query=Maroc&place_id=ChIJjcVRlmGICw0Rw_8sxIGT09k&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click&search_mode=regular_search&price_filter_num_nights=5&federated_search_session_id=ed682609-e85b-4889-9472-bc79b4291b70&pagination_search=true&cursor=eyJzZWN0aW9uX29mZnNldCI6MCwiaXRlbXNfb2Zmc2V0Ijo5MCwidmVyc2lvbiI6MX0%3D',
      'https://www.airbnb.fr/s/Maroc/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-07-01&monthly_length=3&monthly_end_date=2024-10-01&price_filter_input_type=0&channel=EXPLORE&query=Maroc&place_id=ChIJjcVRlmGICw0Rw_8sxIGT09k&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click&search_mode=regular_search&price_filter_num_nights=5&federated_search_session_id=ed682609-e85b-4889-9472-bc79b4291b70&pagination_search=true&cursor=eyJzZWN0aW9uX29mZnNldCI6MCwiaXRlbXNfb2Zmc2V0IjoxMDgsInZlcnNpb24iOjF9',
      'https://www.airbnb.fr/s/Maroc/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-07-01&monthly_length=3&monthly_end_date=2024-10-01&price_filter_input_type=0&channel=EXPLORE&query=Maroc&place_id=ChIJjcVRlmGICw0Rw_8sxIGT09k&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click&search_mode=regular_search&price_filter_num_nights=5&federated_search_session_id=ed682609-e85b-4889-9472-bc79b4291b70&pagination_search=true&cursor=eyJzZWN0aW9uX29mZnNldCI6MCwiaXRlbXNfb2Zmc2V0IjoxMjYsInZlcnNpb24iOjF9',
      'https://www.airbnb.fr/s/Maroc/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-07-01&monthly_length=3&monthly_end_date=2024-10-01&price_filter_input_type=0&channel=EXPLORE&query=Maroc&place_id=ChIJjcVRlmGICw0Rw_8sxIGT09k&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click&search_mode=regular_search&price_filter_num_nights=5&federated_search_session_id=ed682609-e85b-4889-9472-bc79b4291b70&pagination_search=true&cursor=eyJzZWN0aW9uX29mZnNldCI6MCwiaXRlbXNfb2Zmc2V0IjoxNDQsInZlcnNpb24iOjF9',
      'https://www.airbnb.fr/s/Maroc/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-07-01&monthly_length=3&monthly_end_date=2024-10-01&price_filter_input_type=0&channel=EXPLORE&query=Maroc&place_id=ChIJjcVRlmGICw0Rw_8sxIGT09k&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click&search_mode=regular_search&price_filter_num_nights=5&federated_search_session_id=ed682609-e85b-4889-9472-bc79b4291b70&pagination_search=true&cursor=eyJzZWN0aW9uX29mZnNldCI6MCwiaXRlbXNfb2Zmc2V0IjoxNjIsInZlcnNpb24iOjF9',
      'https://www.airbnb.fr/s/Maroc/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-07-01&monthly_length=3&monthly_end_date=2024-10-01&price_filter_input_type=0&channel=EXPLORE&query=Maroc&place_id=ChIJjcVRlmGICw0Rw_8sxIGT09k&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click&search_mode=regular_search&price_filter_num_nights=5&federated_search_session_id=ed682609-e85b-4889-9472-bc79b4291b70&pagination_search=true&cursor=eyJzZWN0aW9uX29mZnNldCI6MCwiaXRlbXNfb2Zmc2V0IjoxODAsInZlcnNpb24iOjF9',
      'https://www.airbnb.fr/s/Maroc/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-07-01&monthly_length=3&monthly_end_date=2024-10-01&price_filter_input_type=0&channel=EXPLORE&query=Maroc&place_id=ChIJjcVRlmGICw0Rw_8sxIGT09k&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click&search_mode=regular_search&price_filter_num_nights=5&federated_search_session_id=ed682609-e85b-4889-9472-bc79b4291b70&pagination_search=true&cursor=eyJzZWN0aW9uX29mZnNldCI6MCwiaXRlbXNfb2Zmc2V0IjoxOTgsInZlcnNpb24iOjF9',
      'https://www.airbnb.fr/s/Maroc/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-07-01&monthly_length=3&monthly_end_date=2024-10-01&price_filter_input_type=0&channel=EXPLORE&query=Maroc&place_id=ChIJjcVRlmGICw0Rw_8sxIGT09k&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click&search_mode=regular_search&price_filter_num_nights=5&federated_search_session_id=ed682609-e85b-4889-9472-bc79b4291b70&pagination_search=true&cursor=eyJzZWN0aW9uX29mZnNldCI6MCwiaXRlbXNfb2Zmc2V0IjoyMTYsInZlcnNpb24iOjF9',
      'https://www.airbnb.fr/s/Maroc/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-07-01&monthly_length=3&monthly_end_date=2024-10-01&price_filter_input_type=0&channel=EXPLORE&query=Maroc&place_id=ChIJjcVRlmGICw0Rw_8sxIGT09k&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click&search_mode=regular_search&price_filter_num_nights=5&federated_search_session_id=ed682609-e85b-4889-9472-bc79b4291b70&pagination_search=true&cursor=eyJzZWN0aW9uX29mZnNldCI6MCwiaXRlbXNfb2Zmc2V0IjoyMzQsInZlcnNpb24iOjF9',
      'https://www.airbnb.fr/s/Maroc/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-07-01&monthly_length=3&monthly_end_date=2024-10-01&price_filter_input_type=0&channel=EXPLORE&query=Maroc&place_id=ChIJjcVRlmGICw0Rw_8sxIGT09k&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click&search_mode=regular_search&price_filter_num_nights=5&federated_search_session_id=ed682609-e85b-4889-9472-bc79b4291b70&pagination_search=true&cursor=eyJzZWN0aW9uX29mZnNldCI6MCwiaXRlbXNfb2Zmc2V0IjoyNTIsInZlcnNpb24iOjF9'
      ]
for url in urls:
    driver.get(url)
    content = driver.page_source
    soup = bs4.BeautifulSoup(content, 'html.parser')
    div_elements = soup.find_all('div',class_='c14whb16 atm_8w_je46wd atm_90_wqqh0j atm_93_16tozh0 atm_9s_11p5wf0 atm_d5_1bp4okc atm_d3_8n3s54 atm_cx_dfedth atm_e0_1fe5oxz atm_dy_kim48s atm_fc_1y6m0gg atm_gi_idpfg4 atm_j6_mtsehg atm_e2_1kjme8w atm_ks_ndwtr5 atm_l4_1f51e7f atm_ld_5ul63a atm_lc_djs5a5 atm_lj_wg387a atm_li_1y0adu4 atm_o3_1p5gfer atm_p9_glywfm atm_tl_19lnvtn atm_or_dhnz5w__ta18iu atm_9s_glywfm_14pyf7n atm_oa_2geptf_bqoj1z atm_oq_1vwytc5_bqoj1z dir dir-ltr')
    for div in div_elements:
        a_tags = div.find_all('a', href=True)
        for a in a_tags:
            if a['href'] in links:
                continue
            else:
                links.append("https://airbnb.fr"+a['href'])
    time.sleep(5)

# Enregistrer les liens dans un fichier CSV
csv_filename = 'links_maroc.csv'
with open(csv_filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Link'])
    for link in links:
        writer.writerow([link])
driver.quit()
print(f"Les liens ont été enregistrés dans le fichier {csv_filename}")
