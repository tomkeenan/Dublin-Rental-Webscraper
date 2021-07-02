import re
from bs4 import BeautifulSoup
import csv
import requests
from decimal import Decimal


def strip_to_decimal(decimal):
    return Decimal(re.sub(r'[^\d.]', '', decimal))


def has_numbers(string):
    return any(char.isdigit() for char in string)


class MyHome:
    def __init__(self, csv_file):
        self.csv_file = csv_file

    # gets the source html from the webpage
    def find_properties(self):
        webpage = 'https://www.myhome.ie/rentals/dublin/property-to-rent'
        source_html = requests.get(webpage).text
        soup = BeautifulSoup(source_html, 'lxml')

        # container to find last page number
        page_container = soup.find('ul',class_='ngx-pagination ng-star-inserted') \
            .find_all('li', class_='ng-star-inserted')

        # total number of pages to loop through
        last_page = page_container[len(page_container) - 2].text.split(' ')
        pages = list(range(int(last_page[1])))

        for page in pages:
            file = open(self.csv_file, 'a')
            writer = csv.writer(file)
            if page != 0:
                append_to_url = f'?page={page + 1}'
                webpage = f'https://www.myhome.ie/rentals/dublin/property-to-rent{append_to_url}'
                source_html = requests.get(webpage).text
                soup = BeautifulSoup(source_html, 'lxml')

            # container for all search results
            properties = soup.find('div', class_='SearchResults__Properties') \
                .find('div',class_='ng-star-inserted') \
                .find_all('div', class_='mb-3 ng-star-inserted')

            for house in properties:
                container = house.find('div', class_="PropertyListingCard__Content")
                test_post = container.find('div', class_=re.compile('PropertyInfoStrip ng-star-inserted'))

                # check for test posts that are released occasionally
                if test_post is not None:
                    # price = container.find('div', class_='PropertyListingCard__Price ng-tns-c205-136').text
                    address = container.a.text.strip()
                    link = 'https://www.myhome.ie' + container.a['href']
                    price = container.find('div', class_=re.compile('PropertyListingCard__Price')) \
                        .text.replace('/','per').strip()

                    if has_numbers(price):
                        if 'week' in price:
                            price_decimal = 4 * strip_to_decimal(price)
                        else:
                            price_decimal = strip_to_decimal(price)
                    else:
                        price_decimal = 0
                    capacity_info = test_post \
                        .find_all('span',class_='PropertyInfoStrip__Detail PropertyInfoStrip__Detail--dark ng-star-inserted')
                    capacity = ''
                    for info in capacity_info:
                        if info == capacity_info[len(capacity_info) - 1]:
                            capacity += info.text.strip()
                        else:
                            capacity += info.text.strip() + ', '
                    writer.writerow([address, price_decimal, capacity, link])
        file.close()
