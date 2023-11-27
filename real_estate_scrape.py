from bs4 import BeautifulSoup
from selenium import webdriver

# Function to retrieve the description of the listing
def get_title(description): 
    title_element = description.find('a')
    if title_element:
        title_text = title_element.text.strip()
        return title_text

# Function to get the price of the listing
def get_price(card):
    price_element = card.find('a', class_ = 'mb-0 text-lg font-bold text-denim price')
    if price_element:
        price = price_element.text.strip()
        return price

# Function to get the link to the listing
def get_link(card):
    link = card.find('a', href = True)
    link = 'https://www.onthemarket.com' + link['href']
    return link

# Opens up an instance of firefox, to access the html of the page
browser = webdriver.Firefox()
browser.get('https://www.onthemarket.com/for-sale/property/gravesend/')
page_source = browser.page_source
soup = BeautifulSoup(page_source, 'lxml')

# For each listing on the site, gets the description, price and link, then prints this information
property_cards = soup.find_all('li', class_ ='otm-PropertyCard')
for card in property_cards:
    description = card.find('span', class_ = 'title')
    if description:
        title_text = get_title(description)
        price = get_price(card)
        link = get_link(card)
        print(f'{title_text}: {price} \n {link} \n')
    else:
        pass
    
# Exits the browser once all the information has been collected
browser.quit()
