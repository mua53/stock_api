import polars_talib as pl_ta
import polars as pl
from data.calculate_dl import calculate_dl
import polars as pl
from datetime import datetime

def calculate_update_technical_analysis():
    field = 'Ticker'
    list_stock_code = calculate_dl.get_distint('stock',field)
    calculate_dl.drop('indicators')
    data = []
    for stock_code in list_stock_code:
        try:
            print(stock_code)
            query = {
                'Ticker': stock_code
            }
            sort = [('DateTime', 1)]
            data_records = calculate_dl.get_data('stock', query, sort)
            data_frame = pl.DataFrame(data_records)
            new_data = data_frame.with_columns(
                pl.col("Close").ta.sma(20).alias("MA20"),
                pl.col("Close").ta.sma(50).alias("MA50"),
                pl.col("Close").ta.sma(100).alias("MA100"),
                pl.col("Close").ta.macd(12, 26, 9).struct.field("macd"),
                pl.col("Close").ta.macd(12, 26, 9).struct.field("macdsignal"),
                pl.col("Close").ta.macd(12, 26, 9).struct.field("macdhist"),
            )
            data_json = new_data.to_dicts()
            data = data + data_json
        except Exception as e:
            pass
    calculate_dl.insert_data('indicators', data)
    return 'Success'

def caculate_macd_signal_buy(date_before=3):
    if date_before > 100:
        date_before = 100
    current_Date = datetime.now()
    current_date_number = current_Date.year * 10000 + current_Date.month * 100 + current_Date.day
    date_query = current_date_number - date_before - 2
    list_data = calculate_dl.get_data('indicators', {'DateTime': {
        '$gte': date_query
    }}, [['Ticker', 1],('DateTime', 1)])
    df = pl.DataFrame(list_data)
    macd_buy, macd_sell = macd_signal(df)
    new_df = df.select(
        pl.col("Ticker"),
        pl.col("DateTime"),
        pl.Series('macd_buy', macd_buy, dtype=pl.Float32),
        pl.Series('macd_sell', macd_sell, dtype=pl.Float32),
    ).filter(pl.col('macd_buy') != -1)
    return new_df.to_dicts()

def macd_signal(df):
    macd_buy=[]
    macd_sell=[]
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
            macd_buy.append(-1)
            macd_sell.append(-1)
        else:
            if df['macdhist'][i] > 0 and df['macdhist'][i-1] <= 0:
                macd_sell.append(-1)
                if position ==False:
                    macd_buy.append(df['Close'][i])
                    position=True
                else:
                    macd_buy.append(-1)
            elif df['macdhist'][i] < 0 and df['macdhist'][i-1] >= 0:
                macd_buy.append(-1)
                if position == True:
                    macd_sell.append(df['Close'][i])
                    position=False
                else:
                    macd_sell.append(-1)
            else:
                macd_buy.append(-1)
                macd_sell.append(-1)
    return macd_buy, macd_sell


