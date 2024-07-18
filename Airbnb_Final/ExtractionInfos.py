from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor, as_completed
import bs4
import pandas as pd
from lxml import etree
import time
lienscsv = '/Users/othmaneirhboula/WebScrap/Airbnb_Final/Liens/LiensCorriges.csv'
df = pd.read_csv(lienscsv)
urls = df.values.tolist()

# Options pour le navigateur
chrome_options = Options()
chrome_options.add_argument('--headless=new')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--blink-settings=imagesEnabled=false')

def extract_info(url):
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(2)
    # Extraire les URLs des 15 premières pages
    try:
        content = driver.page_source
        soup = bs4.BeautifulSoup(content, 'html.parser')
        dom = etree.HTML(str(soup))

        def extract_text(tag, attrs):
            try:
                element = soup.find(tag, attrs)
                return element.text.strip() if element else "N/A"
            except Exception:
                return "N/A"

        # Utilisation d'une fonction pour réduire la répétition du code pour extraire le texte avec XPath
        def extract_xpath_text(path):
            try:
                return dom.xpath(path)[0].text.strip()
            except Exception:
                return "N/A"

        def extract_CSS_text(css_selector):
            try:
                element = soup.select_one(css_selector)
                return element.text.strip() if element else "N/A"
            except Exception:
                return "N/A"
        nom_annonce = extract_CSS_text('#site-content > div > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div > div > div > div > div > section > div > div:nth-child(1) > span > h1')
        type = extract_CSS_text("#site-content > div > div:nth-child(1) > div:nth-child(3) > div > div._16e70jgn > div > div:nth-child(1) > div > div > div > section > div.toieuka.atm_c8_2x1prs.atm_g3_1jbyh58.atm_fr_11a07z3.atm_cs_10d11i2.atm_c8_sz6sci__oggzyc.atm_g3_17zsb9a__oggzyc.atm_fr_kzfbxz__oggzyc.dir.dir-ltr > h2")
        hote = extract_text('div', {"class": "t1pxe1a4 atm_c8_2x1prs atm_g3_1jbyh58 atm_fr_11a07z3 atm_cs_10d11i2 dir dir-ltr"})
        type , ville = type.split('-')
        ville = ville.split(',')[0]
        nb_comment = extract_text('span', {"class": "_1wl1dfc"})
        if nb_comment =='N/A':
            nb_comment = extract_text('div', {"class": "r16onr0j atm_c8_vvn7el atm_g3_k2d186 atm_fr_1vi102y atm_gq_myb0kj atm_vv_qvpr2i atm_c8_sz6sci__14195v1 atm_g3_17zsb9a__14195v1 atm_fr_kzfbxz__14195v1 atm_gq_idpfg4__14195v1 dir dir-ltr"})
        else:
            nb_comment = nb_comment.split(' ')[0]
        if nb_comment =='N/A':
            nb_comment = extract_text('a', {"class": "l1ovpqvx atm_1he2i46_1k8pnbi_10saat9 atm_yxpdqi_1pv6nv4_10saat9 atm_1a0hdzc_w1h1e8_10saat9 atm_2bu6ew_929bqk_10saat9 atm_12oyo1u_73u7pn_10saat9 atm_fiaz40_1etamxe_10saat9 b1uxatsa atm_c8_1kw7nm4 atm_bx_1kw7nm4 atm_cd_1kw7nm4 atm_ci_1kw7nm4 atm_g3_1kw7nm4 atm_9j_tlke0l_1nos8r_uv4tnr atm_7l_1kw7nm4_pfnrn2 atm_rd_8stvzk_pfnrn2 c1qih7tm atm_1s_glywfm atm_26_1j28jx2 atm_3f_idpfg4 atm_9j_tlke0l atm_gi_idpfg4 atm_l8_idpfg4 atm_vb_1wugsn5 atm_7l_jt7fhx atm_rd_8stvzk atm_5j_1896hn4 atm_cs_10d11i2 atm_r3_1kw7nm4 atm_mk_h2mmj6 atm_kd_glywfm atm_9j_13gfvf7_1o5j5ji atm_7l_jt7fhx_v5whe7 atm_rd_8stvzk_v5whe7 atm_7l_177r58q_1nos8r_uv4tnr atm_rd_8stvzk_1nos8r_uv4tnr atm_7l_9vytuy_4fughm_uv4tnr atm_rd_8stvzk_4fughm_uv4tnr atm_rd_8stvzk_xggcrc_uv4tnr atm_7l_1he744i_csw3t1 atm_rd_8stvzk_csw3t1 atm_3f_glywfm_jo46a5 atm_l8_idpfg4_jo46a5 atm_gi_idpfg4_jo46a5 atm_3f_glywfm_1icshfk atm_kd_glywfm_19774hq atm_7l_jt7fhx_1w3cfyq atm_rd_8stvzk_1w3cfyq atm_uc_aaiy6o_1w3cfyq atm_70_1p56tq7_1w3cfyq atm_uc_glywfm_1w3cfyq_1rrf6b5 atm_7l_jt7fhx_pfnrn2_1oszvuo atm_rd_8stvzk_pfnrn2_1oszvuo atm_uc_aaiy6o_pfnrn2_1oszvuo atm_70_1p56tq7_pfnrn2_1oszvuo atm_uc_glywfm_pfnrn2_1o31aam atm_7l_9vytuy_1o5j5ji atm_rd_8stvzk_1o5j5ji atm_rd_8stvzk_1mj13j2 dir dir-ltr"})
            nb_comment = nb_comment.split(' ')[0]
        evaluation = extract_text('span', {"class": "_10nhpq7"}).split(' ')[0]
        if evaluation =='N/A':
            evaluation = extract_CSS_text('#site-content > div > div:nth-child(1) > div:nth-child(3) > div > div._16e70jgn > div > div:nth-child(2) > div > div > div > a > div > div.a8jhwcl.atm_c8_vvn7el.atm_g3_k2d186.atm_fr_1vi102y.atm_9s_1txwivl.atm_ar_1bp4okc.atm_h_1h6ojuz.atm_cx_t94yts.atm_le_14y27yu.atm_c8_sz6sci__14195v1.atm_g3_17zsb9a__14195v1.atm_fr_kzfbxz__14195v1.atm_cx_1l7b3ar__14195v1.atm_le_1l7b3ar__14195v1.dir.dir-ltr > div:nth-child(2)')
        if evaluation =='N/A':
            evaluation = extract_text('div', {"class": "r1lutz1s atm_c8_o7aogt atm_c8_l52nlx__oggzyc dir dir-ltr"})
        if evaluation.startswith('Pas'):
            evaluation, nb_comment = 'N/A', '0'
        if evaluation.startswith('Nouveau'):
            evaluation, nb_comment = 'N/A', '0'
        prix = extract_text('span', {"class": "_11jcbg2"})
        commentaires =[s.text.replace('\xa0', ' ') for s in soup.find_all("div", class_="_b7zir4z")]
        info_supp =soup.find_all("ol", class_="lgx66tx atm_gi_idpfg4 atm_l8_idpfg4 dir dir-ltr")[0].text
        photo_hote = soup.find('img', {"class": "i9if2t0 atm_e2_idpfg4 atm_vy_idpfg4 atm_mk_stnw88 atm_e2_1osqo2v__1lzdix4 atm_vy_1osqo2v__1lzdix4 atm_mk_pfqszd__1lzdix4 i1cqnm0r atm_jp_pyzg9w atm_jr_nyqth1 i1de1kle atm_vh_yfq0k3 dir dir-ltr"})['data-original-uri']
        infos_hote = extract_text("div", {"class": "h1gwm1nh atm_9s_1txwivl atm_ar_1bp4okc atm_gq_1fwxnve atm_cx_1tcgj5g atm_cx_1vi7ecw__oggzyc dir dir-ltr"})
        if infos_hote=='N/A':
            infos_hote = extract_text("div", {"class": "r1lutz1s atm_c8_o7aogt atm_c8_l52nlx__oggzyc dir dir-ltr"})
        # localisation = extract_text('div', {"class": "_152qbzi"})  pas utile car c'est juste une répétition de la ville
        # print(infos_hote)
        if int(nb_comment)<3:
            evaluation = "Nouveau"
        return {"Nom de l'annonce": nom_annonce, "Type": type, "Informations supplémentaires": info_supp, "Hôte": hote, "Photo Hôte":photo_hote, "Infos hôte":infos_hote ,"Ville": ville, "Nombre de commentaires": nb_comment, "Evaluation": evaluation, "Prix": prix,"Commentaires": commentaires,  "URL": url}
    except Exception as e:
        return None


# Utilisation de ThreadPoolExecutor pour le multithreading
data = []
with ThreadPoolExecutor(max_workers=4) as executor:    #il y aura au plus 4 executions en parallèle
    results = executor.map(extract_info, [url[0] for url in urls[:10]])  #on execute le code seulement  sur les 200 premières entreprises pour cet échantillon de test
for result in results:
    if result is not None:
        data.append(result)

df = pd.DataFrame(data)
df.replace('\xa0', ' ', regex=True, inplace=True)
df.replace('·  ·', '/', regex=True, inplace=True)
df.to_excel('/Users/othmaneirhboula/WebScrap/Airbnb_Final/ScrapingAirbnbbis.xlsx', index=False)
# extract_info("https://fr.airbnb.com/rooms/518105886245259262?adults=1&children=0&enable_m3_private_room=true&infants=0&pets=0&search_mode=regular_search&check_in=2024-10-15&check_out=2024-10-17&source_impression_id=p3_1721207008_P3y0GhNGFEL0EsJ1&previous_page_section_name=1000&federated_search_id=753d56dd-e651-461b-aa69-55db28791cf8&_set_bev_on_new_domain=1721132874_EANjNmZmExZDM1OG")