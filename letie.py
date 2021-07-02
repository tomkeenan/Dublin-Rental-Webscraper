import re
from bs4 import BeautifulSoup
import csv
import requests
from decimal import Decimal


def find_property_let():
    webpage = 'https://www.let.ie/property-to-rent/renting_dublin/'
    source_html = requests.get(webpage).text
    soup = BeautifulSoup(source_html, 'lxml')
    properties = soup.find_all('div', class_=re.compile('item ad_'))
    pages_html = soup.find('ul', class_='paging')
    pages_container = pages_html.find_all('a')
    last_page = pages_container[len(pages_container) - 1].text.strip()

    pages = list(range(int(last_page)))

    for page in pages:
        data_csv = 'let_ie.csv'
        first_page = page == 0

        if first_page:
            file = open(data_csv, 'w')
            writer = csv.writer(file)
            writer.writerow(['Address', '€ monthly', 'Capacity', 'Link'])
        else:
            append_to_url = f'pg_{page+1}/'
            file = open(data_csv, 'a')
            writer = csv.writer(file)
            webpage = f'https://www.let.ie/property-to-rent/renting_dublin/{append_to_url}'
            source_html = requests.get(webpage).text
            soup = BeautifulSoup(source_html, 'lxml')
            properties = soup.find_all('div', class_=re.compile('item ad_'))

        for house in properties:
            header = house.find('div', class_='header')
            description = house.find('div', class_='description')
            if description is not None:
                header_info = header.find_all('a')
                address = header_info[0].text.strip()
                link = header_info[0]['href']
                price_test = description.find('strong')
                if price_test is not None:
                    price = price_test.text.strip().split(' ')
                    euros = Decimal(re.sub(r'[^\d.]', '', price[0]))
                    payment_type = price[1]
                    if payment_type == 'weekly':
                        euros = euros*4
                capacity = header_info[1].text.strip()
                writer.writerow([address, euros, capacity, link])


find_property_let()




