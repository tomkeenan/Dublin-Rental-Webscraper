import re
from bs4 import BeautifulSoup
import csv
import requests


# gets the source html from the webpage
def find_property_myhome():
    webpage = 'https://www.myhome.ie/rentals/dublin/property-to-rent'
    source_html = requests.get(webpage).text
    soup = BeautifulSoup(source_html, 'lxml')

    # container for all search results
    properties = soup.find('div', class_='SearchResults__Properties').find('div', class_='ng-star-inserted').find_all('div', class_='mb-3 ng-star-inserted')

    # container to find last page number
    page_container = soup.find('ul', class_='ngx-pagination ng-star-inserted').find_all('li', class_='ng-star-inserted')

    # total number of pages to loop through
    last_page = page_container[len(page_container) - 2].text.split(' ')
    pages = list(range(int(last_page[1])))

    append_to_url = ''

    for page in pages:
        data_csv = 'my_home_ie.csv'
        if page == 0:
            file = open(data_csv, 'w')
            writer = csv.writer(file)
            writer.writerow(['Address', 'Prices', 'Capacity', 'Link'])
        else:
            append_to_url = f'?page={page + 1}'
            file = open(data_csv, 'a')
            writer = csv.writer(file)
            webpage = f'https://www.myhome.ie/rentals/dublin/property-to-rent{append_to_url}'
            source_html = requests.get(webpage).text
            soup = BeautifulSoup(source_html, 'lxml')
            properties = soup.find('div', class_='SearchResults__Properties').find('div',class_='ng-star-inserted').find_all('div', class_='mb-3 ng-star-inserted')

        for house in properties:
            container = house.find('div', class_="PropertyListingCard__Content")
            # price = container.find('div', class_='PropertyListingCard__Price ng-tns-c205-136').text
            address = container.a.text.strip()
            link = 'https://www.myhome.ie' + container.a['href']
            price = container.find('div', class_=re.compile('PropertyListingCard__Price')).text.replace('/','per').strip()
            if 'ft²' in price:
                price.replace(' per ft²', '')

            test_post = container.find('div', class_=re.compile('PropertyInfoStrip ng-star-inserted'))

            # check for test posts that are released occasionally
            if test_post is not None:
                capacity_info = test_post.find_all('span', class_='PropertyInfoStrip__Detail PropertyInfoStrip__Detail--dark ng-star-inserted')
                capacity = ''
                for info in capacity_info:
                    if info == capacity_info[len(capacity_info)-1]:
                        capacity += info.text.strip()
                    else:
                        capacity += info.text.strip() + ', '
                writer.writerow([address, price, capacity, link])


find_property_myhome()
