import scipy
import requests
import json
from datetime import date
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


investment_dates=()
symbol="BOM500820"
start_date="31-10-2017"
end_date_temp="#"
end_date_temp+= str(date.today())
end_date_temp=str(end_date_temp)
end_date="" 
temp=""


#flip the date to dd/mm/yyyy
for num in range(len(end_date_temp)-1,-1,-1):
	if end_date_temp[num] is not '-' and end_date_temp[num] is not '#' :
		temp+=end_date_temp[num]
	else:
		rev_temp=""
		for num2 in range(len(temp)-1,-1,-1):
			rev_temp+= temp[num2]
		end_date+=rev_temp
		if num>1:
			end_date+="-"
		temp=""

url = "https://www.quandl.com/api/v3/datasets/BSE/"+symbol+"/data.json?api_key=DJS3s5-qSxQRxf4KCwjW&start_date="+ start_date + "&end_date=" + end_date+ "&column_index=4"
#start_date="+ start_date + "&end_date=" + end_date + "api_key=DJS3s5-qSxQRxf4KCwjW"




response = requests.request("GET", url)
todos=json.loads(response.text)
todos_dataset= todos['dataset_data']
todos_data=todos_dataset['data']

x = np.arange(0,len(todos_data),1)
xTicks = [] #dates
y_close = [] #closing values

#[date,value]
for i in range(0,len(todos_data)):
	xTicks.append(todos_data[i][0])
	y_close.append(todos_data[i][1])
	y_close_sma10=[]
#calculate 10 day sma; we take the average of 10 days from y_close
#temp=1
#avg=0

#for i in range(0,len(todos_data)):





#plot graph here
plt.xticks(x, xTicks)
plt.xticks(range(int(len(todos_data))), xTicks, rotation=90, fontsize=1) #writes strings with 45 degree angle
plt.plot(x,y_close,'-ok')
plt.show()




#print(json.dumps(todos_data,indent=4,sort_keys=True))

#for x in range(5):
	#for y in todos_data[x]:
		#print (y)

#print(todos)

#todos_dataset=todos['dataset_data']
#print(todos_dataset[''])
#todos_column=todos_dataset['Close']
#print (todos_dataset['Column'])
#print(todos_column)
#print(response.text)
