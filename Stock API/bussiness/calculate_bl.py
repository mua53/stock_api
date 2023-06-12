import pandas
import numpy
import math
from data import dl

def calculate_sma(stock_code, length):
    query = {
        'stock': stock_code
    }
    sort = {
        'date': -1
    }
    lst_stock_code = dl.get_data_limit('stock', query, sort, length)
    sma = float(sum(stock['close'] for stock in lst_stock_code)) / len(lst_stock_code)
    return sma

def calculate_macd(stock_code, fast_length, slow_length, signal_length):
    query = {
        'stock': stock_code
    }
    sort = {
        'date': -1
    }
    lst_stock_code = dl.get_data_limit('stock', query, sort)
    
    return None

def calculate_rsi(stock_code, length):
    return None