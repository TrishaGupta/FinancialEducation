import scipy
import requests
import json
from datetime import datetime
from datetime import date
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


investment_dates=()
symbol="BOM500820"
start_date="31-10-2017"
end_date_temp=""
end_date_temp+= str(date.today())
end_date_temp=str(end_date_temp)
end_date=""
temp=""
timeframe = date.today() - date(2017, 10, 31) 

#print(timeframe)


end_date = datetime.strptime(end_date_temp, "%Y-%m-%d").strftime('%d-%m-%Y')
#print(end_date)		


url = "https://www.quandl.com/api/v3/datasets/BSE/"+symbol+"/data.json?api_key=DJS3s5-qSxQRxf4KCwjW&start_date="+ start_date + "&end_date=" + end_date+ "&column_index=4"
#start_date="+ start_date + "&end_date=" + end_date + "api_key=DJS3s5-qSxQRxf4KCwjW"



response = requests.request("GET", url)

data_json = response.json()

'''
Did a lot of fiddling to realize how to navigate through a list
of keys
print(data_json['dataset_data'].keys())

price data
print(data_json['dataset_data']['data'])
'''

#extracting list of relevant price data
df = pd.DataFrame.from_dict(data_json['dataset_data']['data'])

#renaming columns from rangeIndex to legible words
df.columns = ['Date', 'Price']
df = df.iloc[::-1]

#Calculating various simple moving averages and adding to dataframe
df['sma(5)'] = df['Price'].rolling(window = 5).mean()
df['sma(10)'] = df['Price'].rolling(window = 10).mean()

df_test = df.tail(30)

df_test['sma(5)'] = df['Price'].rolling(window = 5).mean()
df_test['sma(30)'] = df['Price'].rolling(window = 30).mean()

print(df.tail(30))
#Plotting sma on the same graph 
'''
ax = plt.gca()
df.plot(kind='line',x='Date', y='Price', color = 'blue', ax=ax)
df.plot(kind='line',x='Date', y='sma(5)' , color = 'red', ax=ax)
df.plot(kind='line',x='Date', y='sma(10)' , color = 'green', ax=ax)

plt.show()
'''






