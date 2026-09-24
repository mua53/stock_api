from typing import Any

from fastapi import APIRouter, Body, Response
import bussiness.bl as bl

stock_info = APIRouter(prefix="/stock", tags=["stock"])


@stock_info.get("/get-info-indicator-stock/{stockcode}")
def get_info_indicator_stock(stockcode: str):
    return bl.get_info_indicator_stock(stockcode)


@stock_info.post("/check-specs/{stockcode}")
def check_specs_stock(stockcode: str, lst_indicator: Any = Body(None)):
    return Response(content=None)
