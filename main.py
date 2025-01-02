from bs4 import BeautifulSoup
import requests
import time
import random

# Functions for getting user values and putting them in the right format
def get_search():
    print("What are you searching for?")
    search_term = input(">").replace(" ", "-")
    if search_term != "":
        return search_term
    else:
        print("Please enter a search term.")
        return get_search()

def get_max_price():
    print("What is the maximum price? (leave blank for no limit)")
    max_price = input(">")
    if max_price == "":
        return ""
    else:
        try:
            return round(int(max_price))
        except (ValueError,TypeError):
            print("Please enter a valid number")
            return get_max_price()

def get_min_price():
    print("What is the minimum price? (leave blank for no limit)")
    min_price = input(">")
    if min_price == "":
        return ""
    else:
        try:
            return round(int(min_price))
        except (ValueError,TypeError):
            print("Please enter a valid number")
            return get_min_price()

def get_sampling_interval():
    default = 120
    print(f"What's your preferred sampling interval? (in seconds, leave blank for {default} seconds)")
    sampling_interval = input(">")
    if sampling_interval == "":
        return default
    else:
        try:
            return int(sampling_interval)
        except (ValueError,TypeError):
            print("Please enter a valid number")
            return get_sampling_interval()

# Mainly used scraping function using BeautifulSoup, requests and lxml libraries,
def scrape(url):
    site = requests.get(url)
    if site.status_code == 200:
        content = site.text
        scraper = BeautifulSoup(content, "lxml")

        listings = scraper.find_all("article", class_="aditem")
        for index, listing in enumerate(listings):
            index += 1
            title = listing.find("a", class_ = "ellipsis").text.strip()
            hyperlink = "https://www.kleinanzeigen.de" + listing.find("a", class_ = "ellipsis").get("href").strip()
            price = listing.find("p", class_="aditem-main--middle--price-shipping--price").text.strip()

            print(f"Listing {index}:")
            print(f"Title: {title}")
            print(f"Price: {price}")
            print(f"Link: {hyperlink}")
            print("--------------------------------")

    else:
        print("Error: Site could not be reached")

if __name__ == "__main__":
    print("KLEINANZEIGEN LISTING SCRAPING TOOL")
    print("--------------------------------")

    # Calls all the get functions for the user-defined values
    search_term = get_search()
    min_price = get_min_price()
    max_price = get_max_price()
    full_scrape_delay = get_sampling_interval()

    # Main loop for the whole scrape, consisting of iterations for each page
    while True:
        for current_page in range(1,2):
            base_url = f"https://www.kleinanzeigen.de/s-anzeige:angebote/preis:{min_price}:{max_price}/seite:{current_page}/{search_term}/k0"
            print(f"Scraping page {current_page} ({base_url})...")
            print("--------------------------------")
            scrape(base_url)
            time.sleep(random.uniform(1,3))
        print("Scraping done!")
        time.sleep(full_scrape_delay)

