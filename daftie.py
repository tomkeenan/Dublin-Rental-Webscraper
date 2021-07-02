import re
from bs4 import BeautifulSoup
import csv
import requests
from selenium import webdriver


# gets the source html from the webpage
def find_property_daft():
    webpage = 'https://www.daft.ie/property-for-rent/dublin?sort=priceAsc&pageSize=20'
    browser = webdriver.Chrome('/usr/local/bin/chromedriver')
    browser.get(webpage)
    soup = BeautifulSoup(browser.page_source, 'lxml')
    pages_in_html = soup.find('div', class_=re.compile("Pagination__StyledPagination-sc-")).find_all('span')

    # location of last page amount in source html
    last_page = pages_in_html[len(pages_in_html)-2].text

    # used to loop through all pages on website
    pages = list(range(int(last_page)))

    # initialize empty string
    append_to_url = ""

    for page in pages:
        data_csv = 'daft_ie.csv'
        first_page = page == 0

        if first_page:
            file = open(data_csv, 'w')
            writer = csv.writer(file)
            writer.writerow(['Address', 'Prices', 'Capacity', 'Link'])
        else:
            append_to_url = f'from={(page * 20)}'
            file = open(data_csv, 'a')
            writer = csv.writer(file)
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
                price.append(price_html)
            else:
                alternative_layout = True
                sub_prices = house.find_all("p", re.compile("SubUnit__Title-"))
                for sub_price in sub_prices:
                    price.append(sub_price.text)

            # there are multiple listings if there is more than one element in price
            multiple_listing = len(price) > 1

            if multiple_listing or alternative_layout:
                sub_capacities = house.find_all("div", re.compile("SubUnit__CardInfoItem"))
                for sub_capacities in sub_capacities:
                    capacity.append(sub_capacities.text.replace(" · ", ", "))

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

            for i in range(len(price)):
                #print(f"Address: {address}\nPrice: {price[i]}\nCapacity: {capacity[i]}\nLink: {link[i]}\n")
                writer.writerow([address, price[i], capacity[i], link[i]])

        browser.close()


find_property_daft()
