from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
from datetime import datetime

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

# Turning the dictionary into a dataframe, then exporting to excel
def export_excel(data):
    df = pd.DataFrame(data)
    current_datetime = datetime.now() # Adding datetime to each file so each is unique
    current_datetime = str(current_datetime).replace(" ", "_").replace(":", "_")
    df.to_excel(f'Listings/Listings_{str(current_datetime.strip(" "))}.xlsx', index=False)

def property_scrape():
    # Opens up an instance of firefox, to access the html of the page
    browser = webdriver.Firefox()
    browser.get('https://www.onthemarket.com/for-sale/property/gravesend/')
    page_source = browser.page_source
    soup = BeautifulSoup(page_source, 'lxml')

    # Retrieves each of the property cards on the page, then closes the browser
    property_cards = soup.find_all('li', class_ ='otm-PropertyCard')
    browser.quit()
    # Creating a dictionary to be able to export to a dataframe later, allowing exporting to excel
    data = {'Listing Description': [],
            'Price': [],
            'Link': []}
    
    for card in property_cards:
        description = card.find('span', class_ = 'title')
        if description:
            title_text = get_title(description)
            price = get_price(card)
            link = get_link(card)
            # Adding the items to the previously created dictionary
            data['Listing Description'].append(title_text)
            data['Price'].append(price)
            data['Link'].append(link)
        else:
            pass

    # Exits the browser once all the information has been collected, exports results to excel
    export_excel(data) 
    
if __name__ == '__main__':
    # Prompting to give option to run repeatedly
    time_mins = int(input('How many minutes between each run. Press 0 to only run once: '))
    if time_mins == 0:
        property_scrape()
        print('Complete')
    else:
        while True:
            # Multiplying the time input by 60, so time.sleep sleeps in seconds
            property_scrape()
            print(f'Complete, Waiting {time_mins} minutes')
            time.sleep(time_mins * 60)


