from flask import Blueprint, Response
import bussiness.calculate_bl as calculate_bl
import bussiness.fliter_bl as fliter_bl
from utils.utils import Common

fliter = Blueprint('fliter', __name__, url_prefix='/fliter')

@fliter.route('/stock-will-up', methods=['GET'])
def get_stock_will_up():
    return None

@fliter.route('/update-technical-analysis', methods=['GET'])
def update_technical_analysis():
    calculate_bl.calculate_update_technical_analysis()
    return Response(None)

@fliter.route('/find-stock-by-macd', methods=['GET'])
def find_stock_by_macd():
    data = fliter_bl.get_stock_by_macd()
    response = Common.format_response(data)
    return Response(response=response, mimetype="application/json", status=200)
