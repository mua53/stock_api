from utils import call_api
from datetime import datetime
from zipfile import ZipFile
import os
import pandas
from data import dl


def craw_data():
    current_date = datetime.today().strftime('%d-%m-%Y')
    current_date_number = datetime.today().strftime('%Y%m%d')
    current_date_point = datetime.today().strftime('%d.%m.%d')
    url = f'https://cafef1.mediacdn.vn/data/ami_data/{current_date_number}/CafeF.SolieuGD.Upto{current_date}.zip'
    response = call_api.call_download(url, "data.zip")
    #If download success - Unzip data
    if response == 'data.zip':
        unzip_and_read_file()
        dl.delete_many_data('stock', {})
        data_hnx = pandas.read_csv(f'CafeF.HNX.Upto{current_date_point}.csv', sep=",")
        data_json_hnx = data_hnx.to_dict('records')
        dl.insert_data('stock', data_json_hnx)
        data_hose = pandas.read_csv(f'CafeF.HSX.Upto{current_date_point}.csv', sep=",")
        data_json_hose = data_hose.to_dict('records')
        dl.insert_data('stock', data_json_hose)
        data_upcom = pandas.read_csv(f'CafeF.UPCOM.Upto{current_date_point}.csv', sep=",")
        data_json_upcom = data_upcom.to_dict('records')
        dl.insert_data('stock', data_json_upcom)

def unzip_and_read_file():
    current_date_point = datetime.today().strftime('%d.%m.%d')
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
