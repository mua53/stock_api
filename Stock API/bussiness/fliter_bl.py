#Fliter stock
from datetime import datetime
from data.fliter_dl import fliter_dl
import pandas

def get_stock_by_macd():
    last_date = fliter_dl.get_last_date()
    print(last_date)
    #Lay co phieu co his > 0 va co volume > 50000
    query = {
        'DTYYYYMMDD': last_date[0]['DTYYYYMMDD'],
        'His': {
            '$gt': 0
        },
        'Volume5': {
            '$gt': 50000
        },
        'MacdUp': True
    }
    list_stock_fliter = fliter_dl.get_data('indicators',query)
    data_response = []
    for item in list_stock_fliter:
        if len(item['Ticker']) <= 3:
            data_response.append(item)
    return data_response

def get_stock_by_ma(time, stock):
    return None

def get_stock_by_macd_and_ma(time, stock):
    return None

def get_stock_will_down(time, stock):
    return None