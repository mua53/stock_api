from flask import Blueprint, request, Response
from bussiness import craw_data_bl

craw_data = Blueprint('craw_data', __name__, url_prefix='/craw')

@craw_data.route('/craw-data', methods=['GET'])
def craw_data_bvs():
    craw_data_bl.craw_data()
    return 'Success'
