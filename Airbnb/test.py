import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_airbnb_listings(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to retrieve the web page.")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    listings = []
    for listing in soup.find_all('div', class_='_gig1e7'):
        title = listing.find('span', class_='text').get_text()
        price = listing.find('span', class_='_olc9rf0').get_text()
        details = listing.find_all('div', class_='text')[1].get_text()
        listings.append({
            'title': title,
            'price': price,
            'details': details
        })

    return listings


def scrape_airbnb_maroc():
    base_url = "https://www.airbnb.com/s/Maroc/homes"
    listings = get_airbnb_listings(base_url)

    if not listings:
        print("No listings found.")
        return

    df = pd.DataFrame(listings)
    df.to_csv('airbnb_maroc_listings.csv', index=False)
    print("Data has been written to airbnb_maroc_listings.csv")


if __name__ == "__main__":
    scrape_airbnb_maroc()
