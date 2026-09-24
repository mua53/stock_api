from fastapi import APIRouter
import bussiness.bl as bl

charts = APIRouter(prefix="/charts", tags=["charts"])
