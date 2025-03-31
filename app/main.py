# wildfire-api/app/main.py

from fastapi import FastAPI, Query
import geopandas as gpd
from shapely.geometry import Point

app = FastAPI()

# SHP 파일 로드
forest_gdf = gpd.read_file("app/TB_FGDI_FS_JJ100.shp")
if forest_gdf.crs is None:
    forest_gdf.set_crs(epsg=5179, inplace=True)

@app.get("/")
def root():
    return {"message": "🌲 Welcome to Pine Tree Checker API"}

@app.get("/check_pine")
def check_pine(lat: float = Query(...), lon: float = Query(...)):
    point = gpd.GeoDataFrame(geometry=[Point(lon, lat)], crs='EPSG:4326').to_crs(forest_gdf.crs)
    matched = forest_gdf[forest_gdf.contains(point.geometry.iloc[0])]
    if matched.empty:
        return {"result": "해당 위치는 조림지도가 아님"}
    elif matched['KOFTR_NM'].str.contains('소나무').any():
        return {"result": "소나무 있음"}
    else:
        return {"result": "소나무 없음"}
