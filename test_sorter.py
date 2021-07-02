import csv
import pandas as pd
from natsort import natsort_keygen

df = pd.read_csv("let_ie.csv")
sorted_df = df.sort_values('€ monthly',ascending=True)
sorted_df.to_csv("let_ie_sorted.csv")


