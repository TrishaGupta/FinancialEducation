import pandas as pd
import numpy as np
from sklearn import preprocessing
from keras.preprocessing.sequence import TimeseriesGenerator

#stores all the stock data and the derived indicator data
df_full = pd.read_pickle("./data_frame.pkl")



#slicing only the stock data
df_stock_data = df_full.iloc[:, 1: 13]

# for some reason i cant use dropping a column
# have to use del instead
#del df_stock_data['Date']
print(df_stock_data.columns)

'''
	Generate training set
	@param data: the dataframe
	@param value_num: window size
'''

def generate_series(data, value_num):
	close = df_stock_data['Close']
	dividends = data['Total Turnover']
	tsg = TimeseriesGenerator(close, close, length=value_num, batch_size=len(close))
	global_index = value_num
	i, t = tsg[0]
	has_dividends = np.zeros(len(i))	
	for b_row in range(len(t)):
		assert(abs(t[b_row] - close[global_index] <= 0.001))
		has_dividends[b_row] = dividends[global_index] > 0
		global_index += 1
	return np.concatenate((i, np.transpose([has_dividends])), axis=1), t

inputs, targets = generate_series(df_stock_data, 4)

print(df_stock_data.head(10))


#normalizing values using minmax
min_array = df_stock_data.values
min_max_scaler = preprocessing.MinMaxScaler()
scaled = min_max_scaler.fit_transform(min_array)
df_stock_data = pd.DataFrame(scaled)

inputs, targets = generate_series(df_stock_data, 4)
#print(inputs)


