import re

from bs4 import BeautifulSoup
import csv
import requests
from decimal import Decimal


def strip_to_decimal(decimal):
    return Decimal(re.sub(r'[^\d.]', '', decimal))


class Rent:
    def __init__(self, csv_file):
        self.csv_file = csv_file

    def find_properties(self):
        webpage = 'https://www.rent.ie/houses-to-let/renting_dublin/'
        source_html = requests.get(webpage).text
        soup = BeautifulSoup(source_html, 'lxml')
        div_pages = soup.find_all('div', id='pages')
        page_in_html = []

        # I'm not sure why I have to do this but its the only way I can get it to work
        for page in div_pages:
            page_in_html = page.find_all('a')

        # last page number is always stored in the second last position of the pages array
        last_page = page_in_html[len(page_in_html) - 2].text

        # used to loop through all pages on rent.ie
        pages = list(range(int(last_page)))

        for page in pages:
            # append the relevant string to url to move to next page while not on the first page
            # data_csv = 'rent_ie.csv'

            if page == 0:
                file = open(self.csv_file, 'w')
                writer = csv.writer(file)
                writer.writerow(['Address', 'Price per month €', 'Beds', 'Capacity', 'Link'])
            else:
                append_to_url = f'page_{page + 1}'
                file = open(self.csv_file, 'a')
                writer = csv.writer(file)
                webpage = f'https://www.rent.ie/houses-to-let/renting_dublin/{append_to_url}'
                source_html = requests.get(webpage).text
                soup = BeautifulSoup(source_html, 'lxml')

            properties = soup.find_all('div', class_='search_result')
            # writer header row
            for house in properties:
                description = house.find('div', class_='sresult_description').text.replace('  ', '').split('\n\n')
                title = house.find('div', class_='sresult_address')
                # in position due to weird formatting from rent.ie
                price = description[1]
                if 'weekly' in price:
                    price_decimal = 4 * strip_to_decimal(price)
                else:
                    price_decimal = strip_to_decimal(price)

                capacity = description[2]
                address = title.a.text.strip()
                link = title.a['href']
                if 'studio' in capacity:
                    beds = 1
                else:
                    beds = capacity.split(' ')[0]

                writer.writerow(
                    [address, price_decimal, beds, capacity, link])
            file.close()
