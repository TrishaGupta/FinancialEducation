import scipy
import requests
import json
from datetime import datetime
from datetime import date
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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
        Parameters -- data_fram: the data_frame of the data_frame
        Outputs -- adds values to the data_frame
        '''
        data_frame= self.data_frame

         #12 day EMA used in MACD calculation
        data_frame['ema_12']= data_frame['Close'].ewm(span=12,adjust=False, min_periods=0, ignore_na=False).mean()
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

    def MACD(self):
        '''Calculates the MACD line= 26 days EMA - 12 days EMA and the signal line which is 9 day EMA of MACD column_index
        Parameters -- data_fram: the data_frame of the data_frame
        Outputs -- adds values to the data_frame
        '''

        data_frame=self.data_frame

        data_frame['MACD_line']= data_frame['ema_12'] - data_frame['ema_26']
        data_frame['MACD_signal'] = data_frame['MACD_line'].ewm(span=9,adjust=False, min_periods=0, ignore_na=False).mean()

        #if the MACD line crosses over the signal line from below then buy, sell if the signal line crosses over the MACD line
        data_frame['Diff_MACD_line_signal']= data_frame['MACD_line'] - data_frame['MACD_signal']
        data_frame['MACD_cross'] = np.select([((data_frame.Diff_MACD_line_signal < 0) & (data_frame.Diff_MACD_line_signal.shift() > 0)), ((data_frame.Diff_MACD_line_signal > 0) & (data_frame.Diff_MACD_line_signal.shift() < 0))], ['0', '1'], 'None')




    def RSI(self):
        '''
        Calculates RSI
        Parameters -- data_fram: the data_frame of the data_frame
        Outputs -- adds values to the data_frame
        '''
        data_frame= self.data_frame

        # create a shifted data frame so we can calculate Price[i] - Price [i-1] to check if it is gain or loss
        data_frame['Close_shifted']= data_frame['Close'].shift(periods=1)
        #data_frame['Close_shifted'][len(data_frame['Close_shifted'])]=0
        data_frame['Close_shifted'] = data_frame['Close_shifted'].replace(np.nan , 0)
        data_frame['Diff_close_shifted']= data_frame['Close'] - data_frame['Close_shifted']
        data_frame.at[len(data_frame['Diff_close_shifted'])-1, 'Diff_close_shifted'] = 0

        data_frame['RSI_gain']= np.select([data_frame['Diff_close_shifted']>0, data_frame['Diff_close_shifted']<=0],[data_frame['Diff_close_shifted'],0])
        data_frame['RSI_loss']= np.select([data_frame['Diff_close_shifted']<0, data_frame['Diff_close_shifted']>=0],[abs(data_frame['Diff_close_shifted']),0])

        data_frame['RSI_gain_avg']= data_frame['RSI_gain'].rolling(window=14).mean()
        data_frame['RSI_loss_avg']= data_frame['RSI_loss'].rolling(window=14).mean()
        data_frame['RS_value']= data_frame['RSI_gain_avg']/ data_frame['RSI_loss_avg']
        data_frame['RSI_value'] = 100 - np.dot(100,(1/(1+data_frame['RS_value'])))


        #data_frame['RSI_oversold_overbought'] = np.select([data_frame['RSI_value']<=30, data_frame['RSI_value']>=70, 1==1],["Overbought", "Oversold","Resistance" ])

        # 1 == Oversold
        data_frame['RSI_oversold'] = np.select([data_frame['RSI_value']<=30],['1'], "None")
        # 1 == Crossed
        data_frame['RSI_crosses_over_30'] = np.select([( data_frame['RSI_value'] <=30 )& (data_frame['RSI_value'].shift(periods=1) > 30)],['1'], 'None')
        # 1 == Dip
        data_frame['RSI_dips'] = np.select([(data_frame['RSI_value'] > 30) & (data_frame['RSI_value'].shift(periods=-1) > data_frame['RSI_value']) & (data_frame['RSI_value'].shift(periods=1) > data_frame['RSI_value'])],['1'],"None")
        # 1 == Breaks recent Max
        data_frame['RSI_local_max'] = np.select([ (data_frame['RSI_value'] > 30) & (data_frame['RSI_value'] < 70) & (data_frame['RSI_value'] > data_frame['RSI_value'].shift(periods=-1)) & (data_frame['RSI_value'] < data_frame['RSI_value'].shift(periods=1))],['1'], "None")


        bullish_swing_signal= [0,0,0,0]
        #oversold_row= data_frame.apply(lambda row: RSI_helper_one())



        # RSI crosses above 30 buy, RSI crosses below 70 sell
        data_frame['RSI_bearish_bullish_signal'] = np.select([((data_frame['RSI_value'] >= 70 ) & (data_frame['RSI_value'].shift() < 70)), ((data_frame['RSI_value'] <= 30) & (data_frame['RSI_value'].shift() > 30))],["0", "1"], "None")
    '''bullish swing rejection -- buy
    1.RSI falls into oversold territory.
    2.RSI crosses back above 30%.
    3.RSI forms another dip without crossing back into oversold territory.
    4.RSI then breaks its most recent high.'''
        #bullish_swing_signal= [0,0,0,0]
        #data_frame['RSI_']

    def RSI_helper_one(test):
        # conditon 1 oversold
        if test == '1':
            return 1
        return 0


    def BollingerBand(self):

        data_frame = self.data_frame

        # typical price= (high+low+close)/3
        data_frame['Typical_price'] = (data_frame['Low']+ data_frame['High'] + data_frame['Close'])* 1/3
        #std deviation rolling 20 day windows
        data_frame['TP_std_dev_20']= data_frame['Typical_price'].rolling(20).std()
        data_frame['TP_MA_20'] = data_frame['Typical_price'].rolling(20).mean()
        m =2
        data_frame['BOLU'] = (data_frame['TP_MA_20'] + (m* data_frame['TP_std_dev_20']))
        data_frame['BOLD'] = (data_frame['TP_MA_20'] - (m* data_frame['TP_std_dev_20']))
        # band width= bolu- bold / middle
        data_frame['Band_width'] = (data_frame['BOLU'] - data_frame['BOLD'])/data_frame['sma_20']

        # if close > BOLU then sell
        data_frame['BOLU_buy_sell'] = np.select([data_frame['BOLU'] <= data_frame['Close'], data_frame['BOLD'] >= data_frame['Close']],['0','1'], 'None')



    #def KeltnerChannel(self):


#testing purposeso
symbol="BOM500820"
start_date="31-10-2017"
end_date_temp=""
end_date_temp+= str(date.today())
end_date_temp=str(end_date_temp)
end_date= datetime.strptime(end_date_temp, "%Y-%m-%d").strftime('%d-%m-%Y')
url = "https://www.quandl.com/api/v3/datasets/BSE/"+symbol+"/data.json?api_key=DJS3s5-qSxQRxf4KCwjW&start_date="+ start_date + "&end_date=" + end_date#+ "&column_index=4"
#"https://www.quandl.com/api/v3/datasets/BSE/BOM500820/data.json?api_key=DJS3s5-qSxQRxf4KCwjW&start_date=31-10-2017&end_date=31-10-2020"

response = requests.request("GET", url)
data_json = response.json()

data_frame = pd.DataFrame.from_dict(data_json['dataset_data']['data'])
data_frame.columns = ["Date","Open","High","Low","Close","WAP","No. of Shares","No. of Trades","Total Turnover","Deliverable Quantity","% Deli. Qty to Traded Qty","Spread H-L","Spread C-O"]
data_frame=data_frame.iloc[::-1]

test = Indicators(data_frame)
test.SMA()
test.EMA()
test.WMA()
test.MACD()
test.RSI()
test.BollingerBand()

with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    #print(data_frame['RSI_oversold'])
    #print(data_frame['RSI_crosses_over_30'])
    #print(data_frame['RSI_dips'])
    #print(data_frame['RSI_local_max'])
    #print(data_frame['Typical_price'])
    print(data_frame['BOLU'])
    #print(data_frame['BOLD'])
    #print(data_frame['sma_20'])

#print(data_frame['RSI_loss'])
