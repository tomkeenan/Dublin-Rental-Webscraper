import re
from bs4 import BeautifulSoup
import csv
import requests
from decimal import Decimal


def strip_to_decimal(decimal):
    return Decimal(re.sub(r'[^\d.]', '', decimal))


class Let:
    def __init__(self, csv_file):
        self.csv_file = csv_file

    def find_properties(self):
        webpage = 'https://www.let.ie/property-to-rent/renting_dublin/'
        source_html = requests.get(webpage).text
        soup = BeautifulSoup(source_html, 'lxml')
        properties = soup.find_all('div', class_=re.compile('item ad_'))
        pages_html = soup.find('ul', class_='paging')
        pages_container = pages_html.find_all('a')
        last_page = pages_container[len(pages_container) - 1].text.strip()

        pages = list(range(int(last_page)))

        for page in pages:

            file = open(self.csv_file, 'a')
            writer = csv.writer(file)
            if page != 0:
                append_to_url = f'pg_{page + 1}/'
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
                        price_decimal = strip_to_decimal(price[0])
                        payment_type = price[1]
                        if payment_type == 'weekly':
                            price_decimal *= 4
                    capacity = header_info[1].text.strip()
                    if 'bedroom' in capacity:
                        beds = capacity[0]
                    elif 'studio' in capacity:
                        beds = 1
                    else:
                        beds = 0
                    writer.writerow([address, price_decimal,beds, capacity, link])
        file.close()




