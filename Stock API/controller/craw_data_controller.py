from datetime import datetime

from fastapi import APIRouter, Response
from bussiness import craw_data_bl

craw_data = APIRouter(prefix="/craw", tags=["craw"])


@craw_data.get("/craw-data")
def craw_data_cafef():
    craw_data_bl.craw_data(datetime.now())
    return Response(content="Success", media_type="text/plain")
