#Fliter stock
from datetime import datetime
from data.fliter_dl import fliter_dl
from bussiness import calculate_bl
import pandas

def get_stock_by_macd(date_before=3):
    list_data = calculate_bl.caculate_macd_signal_buy(date_before)
    return list_data

def get_stock_by_ma(time, stock):
    return None

def get_stock_by_macd_and_ma(time, stock):
    return None

def get_stock_will_down(time, stock):
    return None