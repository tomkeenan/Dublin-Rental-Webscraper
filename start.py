from daftie import Daft
from letie import Let
from myhome import MyHome
from rentie import Rent
import pandas as pd
import time


def sort(csv):
    df = pd.read_csv(csv)
    sorted_df = df.sort_values('Price per month €', ascending=True)
    sorted_df.to_csv("all_properties_sorted.csv", index=False)


start_time = time.time()

file_name = 'all_properties.csv'

rent = Rent(file_name)
rent.find_properties()

daft = Daft(file_name)
daft.find_properties()

let = Let(file_name)
let.find_properties()

my_home = MyHome(file_name)
my_home.find_properties()


sort(file_name)
print("--- %s seconds ---" % (time.time() - start_time))

