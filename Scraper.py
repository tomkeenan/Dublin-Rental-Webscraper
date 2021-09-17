from daftscraper import Daft
from letscraper import Let
from myhomescraper import MyHome
from rentscraper import Rent
import pandas as pd
import time


# loads all new properties listed since the last time the program was run
def get_new_properties():
    df_viewed = pd.read_csv('resources/viewed_properties.csv')
    df_new = pd.read_csv('resources/all_properties_sorted.csv')

    cond = df_new['Address'].isin(df_viewed['Address'])
    df_new.drop(df_new[cond].index, inplace=True)
    df_new.to_csv('resources/new_properties.csv', index=False)


# makes a copy of a csv file
# used to filter new properties from old properties
def copy_csv(filename):
    df = pd.read_csv(filename)
    df.to_csv('resources/viewed_properties.csv', index=False)


# sorts the csv by beds and then by their price
def sort(csv):
    df = pd.read_csv(csv)
    sorted_df = df.groupby('Beds').apply(lambda x: x.sort_values('Price per month €', ascending=True))
    sorted_df.to_csv("resources/all_properties_sorted.csv", index=False)


class Scraper:

    def search(self):
        start_time = time.time()
        self.rent.find_properties()
        self.daft.find_properties()
        self.let.find_properties()
        self.my_home.find_properties()
        sort(self.file_name)
        get_new_properties()
        print("--- %s seconds ---" % (time.time() - start_time))

    def __init__(self):
        copy_csv('resources/all_properties_sorted.csv')
        self.file_name = 'resources/all_properties.csv'
        self.rent = Rent(self.file_name)
        self.daft = Daft(self.file_name)
        self.let = Let(self.file_name)
        self.my_home = MyHome(self.file_name)
