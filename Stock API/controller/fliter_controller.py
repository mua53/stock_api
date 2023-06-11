from flask import Blueprint
import bussiness.bl as bl

fliter = Blueprint('fliter', __name__, url_prefix='/fliter')

@filter.router('/stock_will_up', methods=['GET'])
def get_stock_will_up():
    return None