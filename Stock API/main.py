from flask import Flask
import bl

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, world!"

@app.route('/get_info_indicator_stock/<string:stockcode>')
def get_info_indicator_stock(stockcode):
    return bl.get_info_indicator_stock(stockcode)

@app.route('/insert_info_career')
def insert_info_career():
    bl.insert_info_career()
    return 'Success'