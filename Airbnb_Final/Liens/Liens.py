# Ce script permet de récupérer les liens des annonces Airbnb à partir d'une liste de liens de recherche
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor, as_completed
import bs4
import time
import pandas as pd


def enlever_doublons(liste_de_listes):
    # Utiliser un ensemble pour garder la trace des sous-listes déjà vues
    ensemble_tuples = set()
    liste_sans_doublons = []

    for sous_liste in liste_de_listes:
        tuple_sous_liste = tuple(sous_liste)
        if tuple_sous_liste not in ensemble_tuples:
            ensemble_tuples.add(tuple_sous_liste)
            liste_sans_doublons.append(sous_liste)

    return liste_sans_doublons

lienscsv = 'Liens/test.csv'
df = pd.read_csv(lienscsv)
urls = df.values.tolist()

# Options pour le navigateur
chrome_options = Options()
chrome_options.add_argument('--headless=new')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--blink-settings=imagesEnabled=false')  # Désactiver les images

def geturl(url):
    driver = webdriver.Chrome(options=chrome_options)
    urls = [url]
    links = []
    try:
        driver.get(url[0])
        # Extraire les URLs des 15 premières pages
        for i in range(14):
            try:
                content = driver.page_source
                soup = bs4.BeautifulSoup(content, 'html.parser')
                div_elements = soup.find_all('div',
                                             class_='c14whb16 atm_8w_je46wd atm_90_wqqh0j atm_93_16tozh0 atm_9s_11p5wf0 atm_d5_1bp4okc atm_d3_8n3s54 atm_cx_dfedth atm_e0_1fe5oxz atm_dy_kim48s atm_fc_1y6m0gg atm_gi_idpfg4 atm_j6_mtsehg atm_e2_1kjme8w atm_ks_ndwtr5 atm_l4_1f51e7f atm_ld_5ul63a atm_lc_djs5a5 atm_lj_wg387a atm_li_1y0adu4 atm_o3_1p5gfer atm_p9_glywfm atm_tl_19lnvtn atm_or_dhnz5w__ta18iu atm_9s_glywfm_14pyf7n atm_oa_2geptf_bqoj1z atm_oq_1vwytc5_bqoj1z dir dir-ltr')
                for div in div_elements:
                    a_tags = div.find_all('a', href=True)
                    for a in a_tags:
                        if a['href'] in links:
                            continue
                        else:
                            links.append(["https://airbnb.com" + a['href'], url[1], url[2]])
                # Trouver et cliquer sur le bouton "Page suivante"
                next_button = driver.find_element(By.CSS_SELECTOR,
                                                  "#site-content > div > div.pbmlr01.atm_h3_t9kd1m.atm_gq_n9wab5.dir.dir-ltr > div > div > div > nav > div > a.l1ovpqvx.atm_1he2i46_1k8pnbi_10saat9.atm_yxpdqi_1pv6nv4_10saat9.atm_1a0hdzc_w1h1e8_10saat9.atm_2bu6ew_929bqk_10saat9.atm_12oyo1u_73u7pn_10saat9.atm_fiaz40_1etamxe_10saat9.c1ytbx3a.atm_mk_h2mmj6.atm_9s_1txwivl.atm_h_1h6ojuz.atm_fc_1h6ojuz.atm_bb_idpfg4.atm_26_1j28jx2.atm_3f_glywfm.atm_7l_hkljqm.atm_gi_idpfg4.atm_l8_idpfg4.atm_uc_10d7vwn.atm_kd_glywfm.atm_gz_8tjzot.atm_uc_glywfm__1rrf6b5.atm_26_zbnr2t_1rqz0hn_uv4tnr.atm_tr_kv3y6q_csw3t1.atm_26_zbnr2t_1ul2smo.atm_3f_glywfm_jo46a5.atm_l8_idpfg4_jo46a5.atm_gi_idpfg4_jo46a5.atm_3f_glywfm_1icshfk.atm_kd_glywfm_19774hq.atm_70_glywfm_1w3cfyq.atm_uc_aaiy6o_9xuho3.atm_70_18bflhl_9xuho3.atm_26_zbnr2t_9xuho3.atm_uc_glywfm_9xuho3_1rrf6b5.atm_70_glywfm_pfnrn2_1oszvuo.atm_uc_aaiy6o_1buez3b_1oszvuo.atm_70_18bflhl_1buez3b_1oszvuo.atm_26_zbnr2t_1buez3b_1oszvuo.atm_uc_glywfm_1buez3b_1o31aam.atm_7l_1wxwdr3_1o5j5ji.atm_9j_13gfvf7_1o5j5ji.atm_26_1j28jx2_154oz7f.atm_92_1yyfdc7_vmtskl.atm_9s_1ulexfb_vmtskl.atm_mk_stnw88_vmtskl.atm_tk_1ssbidh_vmtskl.atm_fq_1ssbidh_vmtskl.atm_tr_pryxvc_vmtskl.atm_vy_1vi7ecw_vmtskl.atm_e2_1vi7ecw_vmtskl.atm_5j_1ssbidh_vmtskl.atm_mk_h2mmj6_1ko0jae.dir.dir-ltr")
                next_button.click()
                time.sleep(1)  # Attendre que la page se charge
                print(f"Page {i + 1}")
                # Ajouter l'URL actuelle à la liste
                current_url = driver.current_url
                urls.append(current_url)
            except Exception as e:
                print(f"Erreur: {e}")
                break
    finally:
        content = driver.page_source
        soup = bs4.BeautifulSoup(content, 'html.parser')
        div_elements = soup.find_all('div',
                                     class_='c14whb16 atm_8w_je46wd atm_90_wqqh0j atm_93_16tozh0 atm_9s_11p5wf0 atm_d5_1bp4okc atm_d3_8n3s54 atm_cx_dfedth atm_e0_1fe5oxz atm_dy_kim48s atm_fc_1y6m0gg atm_gi_idpfg4 atm_j6_mtsehg atm_e2_1kjme8w atm_ks_ndwtr5 atm_l4_1f51e7f atm_ld_5ul63a atm_lc_djs5a5 atm_lj_wg387a atm_li_1y0adu4 atm_o3_1p5gfer atm_p9_glywfm atm_tl_19lnvtn atm_or_dhnz5w__ta18iu atm_9s_glywfm_14pyf7n atm_oa_2geptf_bqoj1z atm_oq_1vwytc5_bqoj1z dir dir-ltr')
        for div in div_elements:
            a_tags = div.find_all('a', href=True)
            for a in a_tags:
                if a['href'] in links:
                    continue
                else:
                    links.append(["https://airbnb.com" + a['href'], url[1], url[2]])
        driver.quit()

    return links


urls_total = []

# Utilisation de ThreadPoolExecutor pour le multithreading
with ThreadPoolExecutor(max_workers=4) as executor:
    future_to_url = {executor.submit(geturl, url): url for url in urls}
    for future in as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
            urls_total.extend(data)
        except Exception as exc:
            print(f'URL {url[0]} generated an exception: {exc}')
# urls_total=list(set(urls_total))
# print(len(urls_total))
urls_total = enlever_doublons(urls_total)
csv = pd.DataFrame(urls_total, columns=['URL', 'Quartier', 'Ville'])
csv.to_csv('Liens/test2.csv', index=False)
