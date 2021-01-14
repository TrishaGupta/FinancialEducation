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

#variables for x,y values of the graph
xTicks = [] #dates
y_close = [] #closing values
xTicks_close_sma10 = xTicks[((len(todos_data)-9)*-1):]
y_close_sma10=[]
xTicks_close_sma20 = xTicks[((len(todos_data)-19)*-1):]
y_close_sma20=[]

#variables for graph
x = np.arange(0,len(todos_data),1)
x_sma10=np.arange(0,len(todos_data)-9,1)
x_sma20=np.arange(0,len(todos_data)-19,1)

#[date,value]
for i in range(0,len(todos_data)):
	xTicks.append(todos_data[i][0])
	y_close.append(todos_data[i][1])

#calculate 10 day sma; we take the average of 10 days from y_close
count=1
sum=0
avg=0

for i in range(0,len(todos_data)):
	if i <10:
		sum+=todos_data[i][1]
		if i==9:
			avg=sum/10.0
			y_close_sma10.append(avg)
			xTicks_close_sma10.append(xTicks.append(xTicks[i]))
	else:
		sum= sum - todos_data[i-10][1]
		sum= sum + todos_data [i][1]
		avg= sum/10.0
		y_close_sma10.append(avg)
		xTicks_close_sma10.append(xTicks.append(xTicks[i]))


#calculate 20 day sma; we take the average of 20 days from y_close
count=1
sum=0
avg=0

for i in range(0,len(todos_data)):
	if i <20:
		sum+=todos_data[i][1]
		if i==19:
			avg=sum/20.0
			y_close_sma20.append(avg)
			xTicks_close_sma20.append(xTicks.append(xTicks[i]))
	else:
		sum= sum - todos_data[i-20][1]
		sum= sum + todos_data [i][1]
		avg= sum/20.0
		y_close_sma20.append(avg)
		xTicks_close_sma20.append(xTicks.append(xTicks[i]))

#plot graph here

#print (len(x))
#print(len(y_close_sma10))


plt.xticks(x, xTicks)
plt.xticks(range(int(len(todos_data))), xTicks, rotation=90, fontsize=1)
plt.plot(x,y_close,'-ok',label= "closing price", color="red")

plt.xticks(x_sma10, xTicks_close_sma10)
plt.xticks(range(int(len(xTicks_close_sma10))), xTicks_close_sma10, rotation=90, fontsize=1)
plt.plot(x_sma10,y_close_sma10,'-ok',label= "10 day sma", color="blue")

plt.xticks(x_sma20, xTicks_close_sma20)
plt.xticks(range(int(len(xTicks_close_sma20))), xTicks_close_sma20, rotation=90, fontsize=1)
plt.plot(x_sma20,y_close_sma20,'-ok',label= "20 day sma", color="green")

plt.show()
