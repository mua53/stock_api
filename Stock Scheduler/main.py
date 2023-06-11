import schedule
import time

def update_info_technical_analysis():
    print("Run update Technical Analysis")

def update_report():
    print("Run update Report")

schedule.every().day().at("00:00").do(update_info_technical_analysis)
schedule.every().day().at("03:00").do(update_report)

while True:
    schedule.run_pending()
    time.sleep(1)