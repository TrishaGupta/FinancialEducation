import scipy
import requests
import json
from datetime import datetime
from datetime import date
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas_ta as ta #pip install -U git+https://github.com/twopirllc/pandas-ta

'''
1- buy Indicator
0- sell indicator
'''

class Indicators:

    def __init__(self, data_frame):
        self.data_frame = data_frame



    def SMA(self):
        ''' Calculates the sma_20, sma_200, the death and golden cross if possible
            Parameters -- data_frame: the data_frame of the data_frame
            Outputs -- adds values to the data_frame'''
        data_frame = self.data_frame
        data_frame['sma_20']= data_frame['Close'].rolling(window=20).mean()
        data_frame['sma_200']= data_frame['Close'].rolling(window=200).mean()
        #if sma[50]>sma[200] shows upward trending, sma[200]>sma[50] shows downward trending

        data_frame['Diff_sma20_sma200']= data_frame['sma_20'] - data_frame['sma_200']
        #if diff =a-b, this formula will choose the first option for when b>a
        data_frame['SMA_Cross_Golden_Death'] = np.select([((data_frame.Diff_sma20_sma200 < 0) & (data_frame.Diff_sma20_sma200.shift() > 0)), ((data_frame.Diff_sma20_sma200 > 0) & (data_frame.Diff_sma20_sma200.shift() < 0))], ['0', '1'], 'None')

        data_frame['Diff_sma200_price']= data_frame['sma_200'] - data_frame['Close']
        data_frame['SMA_Cross_Positive_Breakout_200'] = np.select([((data_frame.Diff_sma200_price < 0) & (data_frame.Diff_sma200_price.shift() > 0)), ((data_frame.Diff_sma200_price > 0) & (data_frame.Diff_sma200_price.shift() < 0))], ['1', '0'], 'None')

        data_frame['Diff_sma20_price']= data_frame['sma_20'] - data_frame['Close']
        data_frame['SMA_Cross_Positive_Breakout_20'] = np.select([((data_frame.Diff_sma20_price < 0) & (data_frame.Diff_sma20_price.shift() > 0)), ((data_frame.Diff_sma20_price > 0) & (data_frame.Diff_sma20_price.shift() < 0))], ['1', '0'], 'None')


    def EMA(self):
        '''Calculates the ema_26 and ema_200
        Parameters -- data_frame: the data_frame of the data_frame
        Outputs -- adds values to the data_frame
        '''
        data_frame= self.data_frame
        data_frame['ema_26']= data_frame['Close'].ewm(span=26, adjust=False, min_periods=0, ignore_na=False).mean()
        data_frame['ema_200']= data_frame['Close'].ewm(span=200, adjust=False).mean()

        data_frame['Diff_ema26_ema200'] = data_frame['ema_26'] -data_frame['ema_200']
        data_frame['EMA_Cross_Golden_Death'] = np.select([((data_frame.Diff_ema26_ema200 < 0) & (data_frame.Diff_ema26_ema200.shift() > 0)), ((data_frame.Diff_ema26_ema200 > 0) & (data_frame.Diff_ema26_ema200.shift() < 0))], ['0', '1'], 'None')

        data_frame['Diff_ema200_price']= data_frame['ema_200'] - data_frame['Close']
        data_frame['EMA_Cross_Positive_Breakout_200'] = np.select([((data_frame.Diff_ema200_price < 0) & (data_frame.Diff_ema200_price.shift() > 0)), ((data_frame.Diff_ema200_price > 0) & (data_frame.Diff_ema200_price.shift() < 0))], ['1', '0'], 'None')

        data_frame['Diff_ema20_price']= data_frame['ema_26'] - data_frame['Close']
        data_frame['EMA_Cross_Positive_Breakout_20'] = np.select([((data_frame.Diff_ema20_price < 0) & (data_frame.Diff_ema20_price.shift() > 0)), ((data_frame.Diff_ema20_price > 0) & (data_frame.Diff_ema20_price.shift() < 0))], ['1', '0'], 'None')

    def WMA(self):
        '''Calculates the wma_26 and wma_200
        Parameters -- data_fram: the data_frame of the data_frame
        Outputs -- adds values to the data_frame
        '''
        data_frame= self.data_frame

        weights_20= np.arange(1,21)
        weights_200= np.arange(1,201)
        data_frame['wma_20']= data_frame['Close'].rolling(20).apply(lambda prices: np.dot(prices,weights_20)/weights_20.sum())
        data_frame['wma_200']= data_frame['Close'].rolling(200).apply(lambda prices: np.dot(prices,weights_200)/weights_200.sum())

        data_frame['Diff_wma20_wma200'] = data_frame['wma_20'] -data_frame['wma_200']
        data_frame['WMA_Cross_Golden_Death'] = np.select([((data_frame.Diff_wma20_wma200 < 0) & (data_frame.Diff_wma20_wma200.shift() > 0)), ((data_frame.Diff_wma20_wma200 > 0) & (data_frame.Diff_wma20_wma200.shift() < 0))], ['0', '1'], 'None')

        data_frame['Diff_wma200_price']= data_frame['wma_200'] - data_frame['Close']
        data_frame['WMA_Cross_Positive_Breakout_200'] = np.select([((data_frame.Diff_wma200_price < 0) & (data_frame.Diff_wma200_price.shift() > 0)), ((data_frame.Diff_wma200_price > 0) & (data_frame.Diff_wma200_price.shift() < 0))], ['1', '0'], 'None')

        data_frame['Diff_wma20_price']= data_frame['wma_20'] - data_frame['Close']
        data_frame['WMA_Cross_Positive_Breakout_20'] = np.select([((data_frame.Diff_wma20_price < 0) & (data_frame.Diff_wma20_price.shift() > 0)), ((data_frame.Diff_wma20_price > 0) & (data_frame.Diff_wma20_price.shift() < 0))], ['1', '0'], 'None')

#testing purposes


symbol="BOM500820"
start_date="31-10-2017"
end_date_temp=""
end_date_temp+= str(date.today())
end_date_temp=str(end_date_temp)
end_date= datetime.strptime(end_date_temp, "%Y-%m-%d").strftime('%d-%m-%Y')
url = "https://www.quandl.com/api/v3/datasets/BSE/"+symbol+"/data.json?api_key=DJS3s5-qSxQRxf4KCwjW&start_date="+ start_date + "&end_date=" + end_date+ "&column_index=4"

response = requests.request("GET", url)
data_json = response.json()

data_frame = pd.DataFrame.from_dict(data_json['dataset_data']['data'])
data_frame.columns = ['Date', 'Close']
data_frame=data_frame.iloc[::-1]
data_frame.set_index(pd.DatetimeIndex(data_frame["Date"]), inplace=True)
data_frame.ta.sma(data_frame['close'], 10,append=True)

print(data_frame.head())

'''
test = Indicators(data_frame)
test.SMA()
test.EMA()
test.WMA()

with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(data_frame)
'''

'''
Preparing a data frame of random numbers 
and using pandas functions to verify


df = df = pd.DataFrame(np.random.randint(100, 1000, (3, 4)), columns=list('ABCD'))
df.set_index(pd.DatetimeIndex(df["datetime"]), inplace=True)
df.ta.log_return(cumulative=True, append=True)
df.ta.percent_return(cumulative=True, append=True)

print(df.head())
'''