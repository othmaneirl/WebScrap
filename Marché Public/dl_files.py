import csv
from unidecode import unidecode
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import multiprocessing
import os

def create_driver():
    chrome_options = Options()
    #chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    return webdriver.Chrome(options=chrome_options)

csv_file = '/Users/othmaneirhboula/webscraping/Stage/links.csv'
with open(csv_file, 'r') as file:
    csv_reader = csv.reader(file)
    urls = [row[0] for row in csv_reader]

def extract_info(driver, url):
    driver.get(url)
    time.sleep(2)
    dl=driver.find_element(By.XPATH, '/html/body/form/div[3]/div[2]/div[10]/div[2]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/ul/li[1]/a')
    dl.click()
    time.sleep(2)
driver = create_driver()
for url in urls:
    extract_info(driver, url)
driver.quit()

