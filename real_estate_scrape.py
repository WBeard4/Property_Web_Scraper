from bs4 import BeautifulSoup
import requests
from selenium import webdriver

def get_title(description):
    title_element = description.find('a')
    if title_element:
        title_text = title_element.text.strip()
        return title_text

def get_price(card):
    price_element = card.find('a', class_ = 'mb-0 text-lg font-bold text-denim price')
    if price_element:
        price_text = price_element.text.strip()
        return price_text
    
def get_link(card):
    link = card.find('a', href = True)
    link = 'https://www.onthemarket.com' + link['href']
    return link

browser = webdriver.Firefox()

browser.get('https://www.onthemarket.com/for-sale/property/gravesend/')
page_source = browser.page_source
soup = BeautifulSoup(page_source, 'lxml')

property_cards = soup.find_all('li', class_ ='otm-PropertyCard')
for card in property_cards:
    description = card.find('span', class_ = 'title')
    if description:
        title_text = get_title(description)
        if title_text:
            price_text = get_price(card)
            if price_text:
                link = get_link(card)
                print(f'{title_text}: {price_text} \n {link} \n')
            else:
                pass
        else:
            pass
    else:
        pass
    



browser.quit()
