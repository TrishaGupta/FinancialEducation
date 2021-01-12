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
	#print ("1")
	#print (num)
	if end_date_temp[num] is not '-' and end_date_temp[num] is not '#' :
		#print ("2")
		temp+=end_date_temp[num]
	else:
		#print ("3")
		rev_temp=""
		for num2 in range(len(temp)-1,-1,-1):
			rev_temp+= temp[num2]
		end_date+=rev_temp
		if num>1:
			end_date+="-"
		temp=""
			
url = "https://www.quandl.com/api/v3/datasets/BSE/"+symbol+"/data.json?api_key=DJS3s5-qSxQRxf4KCwjW&qtops.columns=Close&start_date="+ start_date + "&end_date=" + end_date
#start_date="+ start_date + "&end_date=" + end_date + "api_key=DJS3s5-qSxQRxf4KCwjW"



response = requests.request("GET", url)
todos=json.loads(response.text)
print(todos)

#todos_dataset=todos['dataset_data']
#print(todos_dataset[''])
#todos_column=todos_dataset['Close']
#print (todos_dataset['Column'])
#print(todos_column)
#print(response.text)
