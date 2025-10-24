from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
import psycopg2
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://127.0.0.1:8080"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Database connection
conn = psycopg2.connect(
    host="localhost",
    database="ev_db",
    user="postgres",
    password="postgres"
)

# Pydantic model
class ChargingStation(BaseModel):
    id: int
    osm_id: int
    name: str
    operator: str
    address: str
    location: dict  # <-- GeoJSON parsed as dict
    access_type: str
    opening_hours: str
    is_active: bool
    last_updated: str
    data_source: str

@app.get("/charging_stations/", response_model=List[ChargingStation])
async def get_charging_stations():
    cur = conn.cursor()
    cur.execute("""
        SELECT id, osm_id, name, operator, address,
               ST_AsGeoJSON(location) AS location,
               access_type, opening_hours, is_active,
               last_updated, data_source
        FROM charging_stations
    """)
    rows = cur.fetchall()
    cur.close()

    charging_stations = []
    for row in rows:
        charging_station = ChargingStation(
            id=row[0],
            osm_id=row[1],
            name=row[2],
            operator=row[3],
            address=row[4],
            location=json.loads(row[5]),  # Parse GeoJSON string
            access_type=row[6],
            opening_hours=row[7],
            is_active=row[8],
            last_updated=row[9].isoformat(),
            data_source=row[10]
        )
        charging_stations.append(charging_station)
    return charging_stations

# Serve index.html
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
