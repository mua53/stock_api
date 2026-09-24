from fastapi import APIRouter, Response
import bussiness.calculate_bl as calculate_bl
import bussiness.fliter_bl as fliter_bl
from utils.utils import Common

fliter = APIRouter(prefix="/fliter", tags=["fliter"])


@fliter.get("/stock-will-up")
def get_stock_will_up():
    return None


@fliter.get("/update-technical-analysis")
def update_technical_analysis():
    calculate_bl.calculate_update_technical_analysis()
    return Response(content=None)


@fliter.get("/find-stock-by-macd/{day_before}")
def find_stock_by_macd(day_before: int):
    data = fliter_bl.get_stock_by_macd(day_before)
    response = Common.format_response(data)
    return Response(content=response, media_type="application/json", status_code=200)
