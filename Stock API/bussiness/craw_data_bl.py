from utils import call_api
from datetime import datetime, timedelta
from zipfile import ZipFile
import os
import pandas
from data.dl import dl_base


def craw_data(current_date):
    try:
        yesterday = current_date
        yesterday_format = yesterday.strftime('%d%m%Y')
        yesterday_number = yesterday.strftime('%Y%m%d')
        yesterday_point = yesterday.strftime('%d.%m.%Y')
        url = f'https://cafef1.mediacdn.vn/data/ami_data/{yesterday_number}/CafeF.SolieuGD.Upto{yesterday_format}.zip'
        print(url)
        response = call_api.call_download(url, "data.zip")
        #If download success - Unzip data
        if response == 'data.zip':
            unzip_and_read_file(yesterday_point)
            dl_base.delete_many_data('stock', {})
            data_hnx = pandas.read_csv(f'CafeF.HNX.Upto{yesterday_point}.csv', sep=",")
            data_json_hnx = data_hnx.to_dict('records')
            dl_base.insert_data('stock', data_json_hnx)
            data_hose = pandas.read_csv(f'CafeF.HSX.Upto{yesterday_point}.csv', sep=",")
            data_json_hose = data_hose.to_dict('records')
            dl_base.insert_data('stock', data_json_hose)
            data_upcom = pandas.read_csv(f'CafeF.UPCOM.Upto{yesterday_point}.csv', sep=",")
            data_json_upcom = data_upcom.to_dict('records')
            dl_base.insert_data('stock', data_json_upcom)
    except Exception as e:
        print(e)
        current_date = current_date - timedelta(1)
        craw_data(current_date)


def unzip_and_read_file(current_date_point):
    with ZipFile('data.zip', 'r') as zObject:
        zObject.extractall()
    if os.path.exists("data.zip"):
        os.remove("data.zip")

    fin = open(f"CafeF.HNX.Upto{current_date_point}.csv", "rt")
    data = fin.read()
    data = data.replace('<', '').replace('>', '')
    fin.close()
    fin = open(f"CafeF.HNX.Upto{current_date_point}.csv", "wt")
    fin.write(data)
    fin.close()

    fin = open(f"CafeF.HSX.Upto{current_date_point}.csv", "rt")
    data = fin.read()
    data = data.replace('<', '').replace('>', '')
    fin.close()
    fin = open(f"CafeF.HSX.Upto{current_date_point}.csv", "wt")
    fin.write(data)
    fin.close()

    fin = open(f"CafeF.UPCOM.Upto{current_date_point}.csv", "rt")
    data = fin.read()
    data = data.replace('<', '').replace('>', '')
    fin.close()
    fin = open(f"CafeF.UPCOM.Upto{current_date_point}.csv", "wt")
    fin.write(data)
    fin.close()
    
