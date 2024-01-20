# import pandas 
# import numpy
# import math
import polars_talib as pl_ta
import polars as pl
from data.calculate_dl import calculate_dl

def calculate_sma(stock_code, length):
    query = {
        'stock': stock_code
    }
    sort = {
        'date': -1
    }
    lst_stock_code = calculate_dl.get_data_limit('stock', query, sort, length)
    sma = float(sum(stock['close'] for stock in lst_stock_code)) / len(lst_stock_code)
    return sma

def calculate_macd(stock_code, fast_length, slow_length, signal_length):
    query = {
        'stock': stock_code
    }
    sort = {
        'date': -1
    }
    lst_stock_code = calculate_dl.get_data_limit('stock', query, sort)
    return None

def calculate_rsi(stock_code, length):
    return None

def calculate_update_technical_analysis():
    field = 'Ticker'
    list_stock_code = calculate_dl.get_distint('stock',field)
    calculate_dl.delete_many_data('indicators', {})
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
            print(data_frame)
            pl_ta.get_functions()
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
    calculate_dl.insert_data('indicators', data_json)
    return 'Success'