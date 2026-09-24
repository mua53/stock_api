import json

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
from starlette.exceptions import HTTPException as StarletteHTTPException

from controller.stock_info_controller import stock_info
from controller.chart_controller import charts
from controller.fliter_controller import fliter
from controller.craw_data_controller import craw_data

app = FastAPI()

app.include_router(stock_info)
app.include_router(charts)
app.include_router(fliter)
app.include_router(craw_data)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return Response(
            content=json.dumps({"message": "NOT HAVE API"}),
            status_code=404,
            media_type="application/json",
        )
    if exc.status_code == 400:
        return JSONResponse(status_code=404, content={"message": "Bad request"})
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="127.0.0.1", port=5000, reload=True)
