from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service

# Path to your web driver
def create_driver():
    geckodriver_path = '/Users/othmaneirhboula/webscraping/geckodriver'
    options = FirefoxOptions()
    options.headless = False

    profile = webdriver.FirefoxProfile()
    options.profile = profile
    service = Service(geckodriver_path)

    driver = webdriver.Firefox(service=service, options=options)
    return driver
driver=create_driver()

# Open the Airbnb page
url = 'https://airbnb.fr/rooms/53750106?adults=1&category_tag=Tag%3A8102&children=0&enable_m3_private_room=true&infants=0&pets=0&photo_id=1301218069&search_mode=regular_search&check_in=2024-06-09&check_out=2024-06-14&source_impression_id=p3_1717495627_P3Ma2GIgj6J-Qg3n&previous_page_section_name=1000&federated_search_id=c3f4e6d5-700c-4e8e-b1ff-818a53217a47'
driver.get(url)

# Give the page some time to load
time.sleep(5)

# Extract information
try:
    tradOk = driver.find_element(By.XPATH, '/html/body/div[9]/div/div/section/div/div/div[2]/div/div[1]/button')
    tradOk.click()
    time.sleep(2)
    # Extract title
    title_element = driver.find_element(By.XPATH, '//h1[contains(@class, "_14i3z6h")]')
    title = title_element.text
    print(f"Title: {title}")

    # Extract price
    price_element = driver.find_element(By.XPATH, '//span[contains(@class, "_tyxjp1")]')
    price = price_element.text
    print(f"Price: {price}")

    # Extract description
    description_element = driver.find_element(By.XPATH, '//div[contains(@class, "_1d784r7")]')
    description = description_element.text
    print(f"Description: {description}")

    # Extract key amenities
    amenities_elements = driver.find_elements(By.XPATH,
                                              '//div[contains(@class, "_kqh46o")]/div[contains(@class, "_vzrbjl")]')
    amenities = [amenity.text for amenity in amenities_elements]
    print("Amenities:")
    for amenity in amenities:
        print(f"- {amenity}")

    # Extract location
    location_element = driver.find_element(By.XPATH, '//div[contains(@class, "_9xiloll")]/span')
    location = location_element.text
    print(f"Location: {location}")

    # Extract rating
    rating_element = driver.find_element(By.XPATH, '//span[contains(@class, "_17p6nbba")]')
    rating = rating_element.text
    print(f"Rating: {rating}")

    # Extract host name
    host_element = driver.find_element(By.XPATH, '//a[contains(@class, "_1q2lt74")]/div')
    host_name = host_element.text
    print(f"Host Name: {host_name}")

except Exception as e:
    print(f"An error occurred: {e}")

# Close the WebDriver
driver.quit()
