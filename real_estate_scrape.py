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

def property_scrape():
    # Opens up an instance of firefox, to access the html of the page
    browser = webdriver.Firefox()
    browser.get('https://www.onthemarket.com/for-sale/property/gravesend/')
    page_source = browser.page_source
    soup = BeautifulSoup(page_source, 'lxml')

    # For each listing on the site, gets the description, price and link, then prints this information
    property_cards = soup.find_all('li', class_ ='otm-PropertyCard')
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

            #print(f'{title_text}: {price} \n {link} \n')

        else:
            pass
    
    # Turning the dictionary into a dataframe, then exporting to excel
    df = pd.DataFrame(data)
    current_datetime = datetime.now() # Adding datetime to each file so each is unique
    current_datetime = str(current_datetime).replace(" ", "_").replace(":", "_")
    df.to_excel(f'Listings/Listings_{str(current_datetime.strip(" "))}.xlsx', index=False)

    # Exits the browser once all the information has been collected
    browser.quit()

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
            time_wait = 60
            print(f'Complete, Waiting {time_mins} minutes')
            time.sleep(time_mins * time_wait)


