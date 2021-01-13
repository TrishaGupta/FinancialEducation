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


url = "https://www.quandl.com/api/v3/datasets/BSE/"+symbol+"/data.json?api_key=DJS3s5-qSxQRxf4KCwjW&start_date="+ start_date + "&end_date=" + end_date+ "&column_index=1"
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
#print(df.head())

#Plotting the data on the same graph
ax = plt.gca()
df.plot(kind='line',x='Date',y='Price',color = 'blue', ax=ax)
df.plot(kind='line',x='Date',y='Price', color='red', ax=ax)

plt.show()



