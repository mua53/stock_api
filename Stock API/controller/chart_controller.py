from flask import Blueprint
import bussiness.bl as bl

charts = Blueprint('charts', __name__, url_prefix='/charts')
