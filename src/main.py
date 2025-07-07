from fastapi import FastAPI, Response, HTTPException
from shapely import Polygon

from dto import BaseResponse
from service import HexIndexService
from settings import settings


service = HexIndexService(
    longitude=settings.center_point_lon,
    latitude=settings.center_point_lat,
    radius=settings.base_area_radius
)
app = FastAPI()

@app.get('/hex')
async def fetch_by_parent_hex(parent_hex: str):
    try:
        content = BaseResponse(data=service.hex(parent_hex))
        return Response(content=content.model_dump_json())
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Exception: {exc}")

@app.get('/bbox')
async def fetch_from_border(border: str):
    try:
        # Polygon принимает lonlat, а h3 latlon
        points = tuple(tuple(pair.split('/')[::-1] for pair in border.split(',')))
        content = BaseResponse(data=service.bbox(Polygon(points)))
        return Response(content=content.model_dump_json())
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Exception: {exc}")

@app.get('/avg')
async def get_avg_level(resolution: int):
    try:
        content = BaseResponse(data=service.avg(resolution))
        return Response(content=content.model_dump_json())
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Exception: {exc}")
