#%%

import time
import requests
import sys
import json
import pandas as pd


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


def getCandleDate(symbol,chartTime,num):
    chartTimeNum = chartTimeToInteger(chartTime)
    if chartTimeNum == 0:
        print("時間足入力エラー[1m,5m,15m,1h,4h,1d]")
        sys.exit()
    # print(chartTimeNum)
    # print(chartTimeNum*num)
    stamps=int(time.time() - chartTimeNum*num)*1000
    url="https://fapi.binance.com/fapi/v1/klines?symbol="+symbol+"&interval="+chartTime+"&startTime="+str(stamps)
    res=requests.get(url)
    return res.json()

def getCurrentPrice():
    res = requests.get("https://api.binance.com/api/v1/ticker/allPrices")
    return res.json()


# リストの作成
df = pd.DataFrame(data=getCandleDate("BTCUSDT", "4h", 5), columns=['OpenTime', 'Open', 'High' , 'Low' , 'Close' , 'Volume' , 'CloseTime'])
print("開始します")

print(df)
# print(getCandleDate("BTCUSDT", "4h", 5))
# print(getCurrentPrice())
# %%
