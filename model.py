import pandas as pd
import numpy as numpy

#stores all the stock data and the derived indicator data
df_full = pd.read_pickle("./data_frame.pkl")



#slicing only the stock data
df_stock_data = df_full.iloc[:, : 13]


