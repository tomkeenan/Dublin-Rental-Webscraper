import re
from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from decimal import Decimal


def strip_to_decimal(decimal):
    return Decimal(re.sub(r'[^\d.]', '', decimal))


class Daft:
    def __init__(self, csv_file):
        self.csv_file = csv_file

    # gets the source html from the webpage
    def find_properties(self):
        webpage = 'https://www.daft.ie/property-for-rent/dublin?sort=priceAsc&pageSize=20'
        browser = webdriver.Chrome('/usr/local/bin/chromedriver')
        browser.get(webpage)
        soup = BeautifulSoup(browser.page_source, 'lxml')
        pages_in_html = soup.find('div', class_=re.compile("Pagination__StyledPagination-sc-")).find_all('span')

        # location of last page amount in source html
        last_page = pages_in_html[len(pages_in_html)-2].text

        # used to loop through all pages on website
        pages = list(range(int(last_page)))

        for page in pages:
            file = open(self.csv_file, 'a')
            writer = csv.writer(file)
            if page != 0:
                append_to_url = f'&from={(page * 20)}'
                # add append string to navigate to next page of website
                webpage = f'https://www.daft.ie/property-for-rent/dublin?sort=priceAsc&pageSize=20{append_to_url}'
                browser = webdriver.Chrome('/usr/local/bin/chromedriver')
                browser.get(webpage)
                soup = BeautifulSoup(browser.page_source, 'lxml')

            # class_=re.compile(x) finds a class with the string containing x
            properties = soup.find_all("li", class_=re.compile("SearchPage__Result-"))

            for house in properties:
                price_html = house.find("div", re.compile("TitleBlock__Price")).span.text
                address = house.find("p", re.compile("TitleBlock__Address")).text
                if 'Dublin' not in address:
                    address += ', Dublin'
                capacity_html = house.find_all("p", re.compile("TitleBlock__CardInfoItem"))

                # list used as daft as an inconsistent style on its listings
                # must account for listing with multiple options
                price = []
                capacity = []
                link = []

                # set to true when daft uses the alternative listing style
                alternative_layout = False

                # per is included in the regular style price
                # if it is not included it is the alternative style
                if ' per ' in price_html:
                    if 'week' in price_html:
                        price_decimal = 4 * strip_to_decimal(price_html)
                    else:
                        price_decimal = strip_to_decimal(price_html)
                    price.append(price_decimal)
                else:
                    alternative_layout = True
                    sub_prices = house.find_all("p", re.compile("SubUnit__Title-"))
                    for sub_price in sub_prices:
                        if 'week' in sub_price.text:
                            price_decimal = 4 * strip_to_decimal(sub_price.text)
                        else:
                            price_decimal = strip_to_decimal(sub_price.text)
                        price.append(price_decimal)

                # there are multiple listings if there is more than one element in price
                multiple_listing = len(price) > 1
                beds = []
                if multiple_listing or alternative_layout:
                    sub_capacities = house.find_all("div", re.compile("SubUnit__CardInfoItem"))
                    for sub_capacity in sub_capacities:
                        capacity.append(sub_capacity.text.replace(" · ", ", "))

                    # trims empty white space from list
                    capacity = [elem for elem in capacity if elem.strip()]
                    all_links = house.find_all("li", class_=re.compile("SubUnits__Item"))
                    for sub_link in all_links:
                        link.append("https://www.daft.ie/" + sub_link.a['href'])
                else:
                    temp = ""
                    for feature in capacity_html:
                        if feature != capacity_html[len(capacity_html) - 1]:
                            temp += feature.text + ", "
                        else:
                            temp += feature.text
                    capacity.append(temp)
                    link.append("https://www.daft.ie/" + house.a['href'])

                beds = []
                for ele in capacity:
                    if 'Bed' in ele:
                        beds.append(ele[0])
                    elif 'Studio' in ele:
                        beds.append(1)
                    else:
                        beds.append(0)

                for i in range(len(price)):
                    writer.writerow([address, price[i],beds[i], capacity[i], link[i]])
            browser.close()
        file.close()
