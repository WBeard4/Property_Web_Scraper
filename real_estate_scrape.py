from bs4 import BeautifulSoup
import requests
from selenium import webdriver

def get_title(description):
    title_element = description.find('a')
    if title_element:
        title_text = title_element.text.strip()
        return title_text


browser = webdriver.Firefox()

browser.get('https://www.onthemarket.com/for-sale/property/gravesend/')
page_source = browser.page_source
soup = BeautifulSoup(page_source, 'lxml')

property_cards = soup.find_all('li', class_ ='otm-PropertyCard')
for card in property_cards:
    description = card.find('span', class_ = 'title')
    if description:
        title_text = get_title(description)
        # if title_text:
            # Find the price that for property here
                # if price exists
                    # Get link to property
        # Else
            # Move on to next property




browser.quit()
