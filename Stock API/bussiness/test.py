import requests
from datetime import datetime
import wget
from zipfile import ZipFile
import os
import pandas

current_date = datetime.today().strftime('%Y-%m-%d')
url = f'https://bvsc.com.vn/Handlers/DownloadMetaStockDataEx.ashx?format=Text&data=All&period=EOD&symbol=&fromDate=1997-06-11&toDate={current_date}'
response = wget.download(url, "data.zip")
if response == 'data.zip':
    with ZipFile('data.zip', 'r') as zObject:
        zObject.extractall()
if os.path.exists("data.zip"):
    os.remove("data.zip")

data_hnx = pandas.read_csv('HNX.txt', sep=",", header=None).values.tolist()
print(data_hnx)
data_hose = pandas.read_csv('HOSE.txt', sep=",", header=None)
data_upcom = pandas.read_csv('UPCOM.txt')
print("Done")