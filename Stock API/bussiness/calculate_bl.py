import pandas 
import numpy
import math
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
    for stock_code in list_stock_code:
        query = {
            'Ticker': stock_code
        }
        sort = [('DTYYYYMMDD', 1)]
        data_records = calculate_dl.get_data('stock', query, sort)
        data_frame = pandas.DataFrame.from_records(data_records)
        data_frame = data_frame.drop(['_id'], axis=1)
        #Calculate sma20 and take data
        cma20 = data_frame['Close'].rolling(20).mean()
        cma50 = data_frame['Close'].rolling(50).mean()
        cma100 = data_frame['Close'].rolling(100).mean()
        volumn = data_frame['Volume'].rolling(5).mean()
        data_frame['Ma20'] = cma20
        data_frame['Ma50'] = cma50
        data_frame['Ma100'] = cma100
        data_frame['Volume5'] = volumn
        ema12 = data_frame['Close'].ewm(span=12, adjust=False, min_periods=12).mean()
        ema26 = data_frame['Close'].ewm(span=26, adjust=False, min_periods=26).mean()
        macd = ema12 - ema26
        signal = macd.ewm(span=9, adjust=False, min_periods=9).mean()
        his = macd - signal
        data_frame['Macd'] = macd
        data_frame['Signal'] =signal
        data_frame['His'] = his
        data_frame['MacdUp'] = macd.rolling(3).apply(lambda x: numpy.all(numpy.diff(x) > 0)).astype('boolean')
        data_frame['HisUp'] = his.rolling(3).apply(lambda x: numpy.all(numpy.diff(x) > 0)).astype('boolean')
        data_json = data_frame.to_dict('records')
        calculate_dl.insert_data('indicators', data_json)
    return 'Success'