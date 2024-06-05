from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import time
import re
import pandas as pd

# Initialize WebDriver for Firefox
firefox_options = Options()
#firefox_options.add_argument("--headless")  # Uncomment to run in headless mode
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)

# Base URL setup
base_url = "https://yakeey.com/fr/buy/properties?transactionType=SALE&isNew=ALL&cityId=65ce15c8648d1e6607858d79&page="
# driver.get(base_url)

# Store all extracted links
all_links = []

# Loop through all n pages
for page in range(1,2):
    current_url = base_url + str(page+1)
    driver.get(current_url)
    time.sleep(10)  # Wait for the page to load completely

    # Extract href attributes from the current page
    links = driver.find_elements(By.CSS_SELECTOR, "a.MuiBox-root.mui-1y4n71p")
    for link in links:
        href = link.get_attribute('href')
        if href:
            all_links.append(href)

# Cleanup: close the driver after the scraping is done
driver.quit()

# Output or process the collected links
print(all_links)

df = pd.DataFrame(all_links)
df.to_excel('yakeey.xlsx')

R = []
def authenticate():
    id="468799960"
    mdp='Webscraping1'
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)
    driver.get('https://yakeey.com/fr-ma/login')
    time.sleep(2)
    change_number = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/form/div/div[1]/div/div/div/div')
    change_number.click()
    time.sleep(2)
    select_be = driver.find_element(By.XPATH, '/html/body/div[4]/div[3]/ul/li[3]')
    select_be.click()
    time.sleep(2)
    phone_number = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/form/div/div[1]/div/input')
    phone_number.send_keys(id)
    time.sleep(1)
    mdp_input = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/form/div/div[2]/div/input')
    mdp_input.send_keys(mdp)
    bouton_connexion = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/form/div/button')
    time.sleep(1)
    bouton_connexion.click()
    time.sleep(3)

authenticate()
cookies = driver.get_cookies()
for x in all_links:
    driver.get(x)
    driver.delete_all_cookies()
    for cookie in cookies:
        driver.add_cookie(cookie)
    time.sleep(8)
    data = {}
    divs = driver.find_elements(By.CLASS_NAME, "MuiStack-root")
    for div in divs:
        try:
            texts = div.find_elements(By.XPATH, "./*")
            if len(texts) >= 2:
                key = texts[0].text.strip()
                value = texts[1].text.strip()
                data[key] = value
        except:
            pass
    # Add phone number to data
    bouton_numero=driver.find_element(By.CSS_SELECTOR, 'div.mui-13n1q7c:nth-child(2) > button:nth-child(2)')
    bouton_numero.click()
    time.sleep(2)
    data['Numero de telephone'] = driver.find_element(By.CSS_SELECTOR, 'button.mui-veier5:nth-child(1) > p:nth-child(2)').text
    R.append(data)
driver.quit()
def remove_keys_with_numbers(input_dict):
    pattern = re.compile(r'\d')
    cleaned_dict = {k: v for k, v in input_dict.items() if not pattern.search(k)}
    return cleaned_dict

Rs = []
for x in range(len(R)):
    try:
        Rs.append(remove_keys_with_numbers(R[x]))
    except:
        print('error in index', x)

Rs = [tuple(sorted(d.items())) for d in Rs]
Rs = list(set(Rs))

Rs = [dict(t) for t in Rs]

df = pd.DataFrame(Rs)
df.to_excel('sortie_yakeey.xlsx', index=False)
