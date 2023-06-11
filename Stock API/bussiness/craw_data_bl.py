from utils import call_api
from datetime import datetime
from zipfile import ZipFile
import os
import pandas
from data import dl


def craw_data():
    current_date = datetime.today().strftime('%Y-%m-%d')
    url = f'https://bvsc.com.vn/Handlers/DownloadMetaStockDataEx.ashx?format=Text&data=All&period=EOD&symbol=&fromDate=1997-06-11&toDate={current_date}'
    response = call_api.call_download(url, "data.zip")
    #If download success - Unzip data
    if response == 'data.zip':
        with ZipFile('data.zip', 'r') as zObject:
            zObject.extractall()
    if os.path.exists("data.zip"):
        os.remove("data.zip")

    total_lst = []
    data_hnx = pandas.read_csv('HNX.txt', sep=",", header=None).values.tolist()
    data_hose = pandas.read_csv('HOSE.txt', sep=",", header=None).values.tolist()
    data_upcom = pandas.read_csv('UPCOM.txt', sep=",", header=None).values.tolist()
    total_lst = data_hnx + data_hose + data_upcom
    for idx,lst_info_stock in enumerate(total_lst):
        if idx > 0:
            query = {
                'stock_code': lst_info_stock[0],
                'date': lst_info_stock[1]
            }
            data = dl.get_data_one('stock', query)
            if data:
                data_update = {
                    'open': lst_info_stock[2],
                    'high': lst_info_stock[3],
                    'low': lst_info_stock[4],
                    'close': lst_info_stock[5],
                    'vol': lst_info_stock[6]
                }
                dl.update_data('stock', query, data_update)
            else:
                data_insert = {
                    'stock_code': lst_info_stock[0],
                    'date': lst_info_stock[1],
                    'open': lst_info_stock[2],
                    'high': lst_info_stock[3],
                    'low': lst_info_stock[4],
                    'close': lst_info_stock[5],
                    'vol': lst_info_stock[6]
                }
                dl.insert_data('stock', data_insert)
    if os.path.exists("HNX.txt"):
        os.remove("HNX.txt")
    if os.path.exists("HOSE.txt"):
        os.remove("HOSE.txt")
    if os.path.exists("UPCOME.txt"):
        os.remove("UPCOME.txt")