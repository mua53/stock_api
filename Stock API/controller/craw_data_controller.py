from flask import Blueprint, request, Response
from bussiness import craw_data_bl
from datetime import datetime

craw_data = Blueprint('craw_data', __name__, url_prefix='/craw')

@craw_data.route('/craw-data', methods=['GET'])
def craw_data_cafef():
    craw_data_bl.craw_data(datetime.now())
    return 'Success'
