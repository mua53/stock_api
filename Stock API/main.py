from flask import Flask, Response
from controller.stock_info_controller import stock_info
from controller.chart_controller import charts
from controller.fliter_controller import fliter
import logging
import json

app = Flask(__name__)

app.register_blueprint(stock_info)
app.register_blueprint(charts)
app.register_blueprint(fliter)


@app.errorhandler(404)
def page_not_found(e):
    response = {
        'message': 'NOT HAVE API',
    }
    return Response(json.dumps(response),status=404)

@app.errorhandler(400)
def error_404(e):
    response = {
        'message': 'Bad request'
    }
    return Response(response,status=404)

if __name__ == '__main__':
    app.run(port=5000)