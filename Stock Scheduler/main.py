import schedule
import time
import requests

BASE_HOST = "127.0.0.1:5000"

def craw_data_bvs():
    url = BASE_HOST + "/craw/craw-data"
    requests.request("GET", url)

def update_info_technical_analysis():
    print("Run update Technical Analysis")

def update_report():
    print("Run update Report")

schedule.every().day().at("17:00").do(craw_data_bvs)
schedule.every().day().at("00:00").do(update_info_technical_analysis)
schedule.every().day().at("03:00").do(update_report)

while True:
    schedule.run_pending()
    time.sleep(1)