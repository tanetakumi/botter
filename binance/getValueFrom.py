import time
import requests
import sys
import json
import pandas as pd
import talib
import os

def chartTimeToInteger(chartTime):
    if chartTime == "1m":
        return 60
    elif chartTime == "5m":
        return 300
    elif chartTime == "15m":
        return 900
    elif chartTime == "1h":
        return 3600
    elif chartTime == "4h":
        return 14400
    elif chartTime == "1d":
        return 86400
    else:
        return 0


def getCandleData(symbol,chartTime,num):
    chartTimeNum = chartTimeToInteger(chartTime)
    if chartTimeNum == 0:
        print("時間足入力エラー[1m,5m,15m,1h,4h,1d]")
        sys.exit()
    # print(chartTimeNum)
    # print(chartTimeNum*num)
    stamps=int(time.time() - chartTimeNum*num)*1000
    url="https://api.binance.com/api/v3/klines?symbol="+symbol+"&interval="+chartTime+"&startTime="+str(stamps)
    res=requests.get(url)

    # DataFrameの作成
    df = pd.DataFrame(data=res.json(), columns=['OpenTime', 'Open', 'High' , 'Low' , 'Close' , 'Volume' , 'CloseTime' ,'A','B','C','D','E'])
    df.drop(columns=['Volume','CloseTime','A','B','C','D','E'], axis=1, inplace=True)

    # 時間のdatetime化
    df['OpenTime'] = (df['OpenTime']/1000).astype('int64')
    df['OpenTime'] = pd.to_datetime(df['OpenTime'],unit='s')

    # Objectをfloatに変換
    df['Open']  = df['Open'].astype(float, errors = 'raise')
    df['Close'] = df['Close'].astype(float, errors = 'raise')
    df['High']  = df['High'].astype(float, errors = 'raise')
    df['Low']   = df['Low'].astype(float, errors = 'raise')
    return df


def getCurrentPrices():
    res = requests.get("https://api.binance.com/api/v3/ticker/price")
    # DataFrameの作成
    df = pd.read_json(json.dumps(res.json()))
    df = df[df['symbol'].str.contains('USDT')]
    # print(df.columns)
    df.reset_index(drop=True ,inplace = True)
    # print(df.dtypes)
    return df

def getBrands():
    res = requests.get("https://api.binance.com/api/v3/ticker/price")
    # DataFrameの作成
    df = pd.read_json(json.dumps(res.json()))
    df = df[df['symbol'].str.contains('USDT')]
    df.drop(columns='price', axis=1, inplace=True)
    # print(df.columns)
    df.reset_index(drop=True ,inplace = True)
    # print(df.dtypes)
    return df

def csvFolder():
    path = "./csv"
    if not os.path.isdir(path):
        os.mkdir(path)
        print("csv folder not exist")
    else:
        print("csv folder exist")
# def saveAsCSV(df):



def test():
    res = requests.get("https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=4h")
    # DataFrameの作成
    df = pd.read_json(json.dumps(res.json()))
    # print(df.dtypes)
    return df

# calculate RSI
#               100
# RSI = 100 - --------
#              1 + RS
# def rsi(df):
    
csvFolder()

# データセットから終値のみ切り出して差分を計算

# dataFrame = getCandleData("BTCUSDT","1h",300)
# dataFrame = getCurrentPrices()
# print(getBrands())
brands = getBrands()
# print(brands.iat[2,0])
print(type(len(brands)))
print(len(brands))
num = len(brands)
for i in range(num):
    
    print(i, "  " + brands.iat[i,0])

# path = os.getcwd()
# print(path)

# vRsi = talib.RSI(dataFrame['Close'],14)

# print(vRsi)

"""

df = getCandleDate("BTCUSDT","1h",15)
close = df['Close']
diff = close.diff()
print(diff)
print("開始します")

print(df.dtypes)
print(df)

"""
# print(getCandleDate("BTCUSDT", "4h", 5))
# print(getCurrentPrice()

