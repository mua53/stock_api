from flask import Blueprint, request, Response
import bussiness.bl as bl

stock_info = Blueprint('stock_info', __name__, url_prefix='/stock')

@stock_info.route('/get-info-indicator-stock/<string:stockcode>', methods=['GET'])
def get_info_indicator_stock(stockcode):
    return bl.get_info_indicator_stock(stockcode)

@stock_info.route('/check-specs/<string:stockcode>', methods=['POST'])
def check_specs_stock(stockcode):
    lst_indicator = request.get_json()
    return Response(None)

@stock_info.route('/get-data/<string:stockcode>')

@stock_info.route('/insert-info-career')
def insert_info_career():
    bl.insert_info_career()
    return 'Success'