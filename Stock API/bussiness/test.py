import requests
from datetime import datetime
import wget
from zipfile import ZipFile
import os
import pandas
import pymongo


client = pymongo.MongoClient(os.getenv('URL_MONGODB'))
db = client['stock']

current_date = datetime.today().strftime('%d-%m-%Y')
current_date_number = datetime.today().strftime('%Y%m%d')
current_date_point = datetime.today().strftime('%d.%m.%d')
current_date_point = '09.06.2023'
# url = f'https://cafef1.mediacdn.vn/data/ami_data/{current_date_number}/CafeF.SolieuGD.Upto{current_date}.zip'
url = f'https://cafef1.mediacdn.vn/data/ami_data/20230609/CafeF.SolieuGD.Upto09062023.zip'

response = wget.download(url, "data.zip")
if response == 'data.zip':
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

db.stock.delete_many({})
data_hnx = pandas.read_csv(f'CafeF.HNX.Upto{current_date_point}.csv', sep=",")
data_json_hnx = data_hnx.to_dict('records')
db.stock.insert_many(data_json_hnx)
data_hose = pandas.read_csv(f'CafeF.HSX.Upto{current_date_point}.csv', sep=",")
data_json_hose = data_hose.to_dict('records')
db.stock.insert_many(data_json_hose)
data_upcom = pandas.read_csv(f'CafeF.UPCOM.Upto{current_date_point}.csv', sep=",")
data_json_upcom = data_upcom.to_dict('records')
db.stock.insert_many(data_json_upcom)
print("Done")