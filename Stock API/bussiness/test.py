import numpy as np
import pandas as pd
import polars as pl
from datetime import datetime


def MACD_Strategy(df, risk):
    MACD_Buy=[]
    MACD_Sell=[]
    position=False
    current_ticker = ''
    new_ticker = True
    for i in range(0, len(df)):
        if current_ticker !=  df['Ticker'][i]:
            new_ticker = True
            current_ticker = df['Ticker'][i]
        else:
            new_ticker = False
        if i == 0 or new_ticker:
            MACD_Buy.append(np.nan)
            MACD_Sell.append(np.nan)
        else:
            if df['macdhist'][i] > 0 and df['macdhist'][i-1] <= 0:
                MACD_Sell.append(np.nan)
                if position ==False:
                    MACD_Buy.append(df['Close'][i])
                    position=True
                else:
                    MACD_Buy.append(np.nan)
            elif df['macdhist'][i] < 0 and df['macdhist'][i-1] >= 0:
                MACD_Buy.append(np.nan)
                if position == True:
                    MACD_Sell.append(df['Close'][i])
                    position=False
                else:
                    MACD_Sell.append(np.nan)
            else:
                MACD_Buy.append(np.nan)
                MACD_Sell.append(np.nan)
    return MACD_Buy, MACD_Sell
    # print(MACD_Buy)
    # print(MACD_Sell)

#Data Layer
import os
import pymongo

client = pymongo.MongoClient(os.getenv('URL_MONGODB'))
db = client['stock']

list_json = list(db['indicators'].find({'Ticker':'VPB'}))

def get_list_macd_signal_buy(date_before=3):
    # date_query = date_before + 1
    current_Date = datetime.now()
    current_date_number = current_Date.year * 10000 + current_Date.month * 100 + current_Date.day
    date_query = current_date_number - date_before - 2
    list_data = list(db['indicators'].find({'DateTime': {
        '$gte': date_query
    }}).sort([['Ticker', 1],('DateTime', 1)]))
    # print(list_data)
    df = pl.DataFrame(list_data)
    macd_buy, macd_sell = MACD_Strategy(df, 0.025)
    new_df = df.select(
        pl.col("Ticker"),
        pl.col("DateTime"),
        pl.Series('macd_buy', macd_buy),
        pl.Series('macd_sell', macd_sell),
    ).filter(pl.col('macd_buy') != np.nan)
    # df['macd_buy'] = macd_buy
    # df['macd_sell'] = macd_sell
    print(new_df)

get_list_macd_signal_buy()

# df = pd.DataFrame(list_json)
# MACD_Strategy(df, 0.025)
