import dataclasses
from contextlib import asynccontextmanager
from os import environ
from typing import Annotated

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import zerorpc
from pydantic import Field

from postgres import database
import address
from coordinates import Coordinates

# TODO: optional postal based on ENV
libpostal_client = zerorpc.Client()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    libpostal_client.connect(f'tcp://{environ.get("LIBPOSTAL_HOST", "localhost")}:4242')
    yield
    libpostal_client.close()
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

#c.expandAndParse(q)

# TODO: move to model
@dataclasses.dataclass
class ReverseResponse:
    results: list[str] # TODO: type for "unnamed place"
    type: str = "reverse"

@dataclasses.dataclass
class ForwardResponse:
    results: list[Coordinates]
    type: str = "forward"

class NotImplementedException(Exception):
    def __init__(self, name: str):
        self.name = name

async def forward(q: str, limit: int) -> list[Coordinates]:
    # TODO: how to normalize country name (CZ,Cesko, CR,cz, ...)
    # how to normalize names in different languages - Prague, Praha
    # normalize zip code 60200, 602 00?
    libpostal_addr = {e['component']:e['value'] for e in libpostal_client.parse(q)}
    # print(libpostal_addr)
    if 'house_number' in libpostal_addr and 'road' in libpostal_addr: # these should be most of the time according to https://wiki.openstreetmap.org/wiki/Key:addr:*
        # to use libpostal_addr['city'] import would need to handle boundary area somehow or lookup into some postcode database
        query = """
            SELECT ST_X(geom) AS lat, ST_Y(geom) as lon
            FROM addrs
            WHERE housenumber = $1 AND lower(street) = $2
            LIMIT $3;"""
        async with database.pool.acquire() as connection:
            rows = await connection.fetch(query, libpostal_addr['house_number'], libpostal_addr['road'], limit)
            return [Coordinates(lon=record['lon'],lat=record['lat']) for record in rows]
    elif 'road' in libpostal_addr:
        query = """
            SELECT ST_X(geom) AS lat, ST_Y(geom) as lon
            FROM addrs
            WHERE lower(street) = $1
            LIMIT $2;"""
        async with database.pool.acquire() as connection:
            rows = await connection.fetch(query, libpostal_addr['road'], limit)
            return [Coordinates(lon=record['lon'], lat=record['lat']) for record in rows]
    # 'house' in libpostal_addr place? name
    elif 'city' in libpostal_addr or 'country' in libpostal_addr or 'suburb' in libpostal_addr:
        raise NotImplementedException("City/Suburb/Country/... lookup not implemented")
    else:
        return []

async def reverse(coords: Coordinates, limit) -> list[str]:
    query = """WITH point AS (
      SELECT ST_SetSRID(ST_Point($2, $1), 4326) AS geom
    )
    SELECT a.*
    FROM addrs a, point p
    ORDER BY a.geom <-> p.geom
    LIMIT $3;"""

    async with database.pool.acquire() as connection:
        rows = await connection.fetch(query, coords.lat, coords.lon, limit)
        return [address.format_address(record) for record in rows]

@app.get("/")
async def root(q: Annotated[str, Field(max_length=255)], limit: Annotated[int, Field(gt=0, lt=21)] = 1) -> ReverseResponse | ForwardResponse:
    coordinates = Coordinates.from_str(q)
    if coordinates:
        return ReverseResponse(results=await reverse(coordinates, limit))
    else:
        return ForwardResponse(results=await forward(q, limit))

# not for production, just for showcase
@app.exception_handler(NotImplementedException)
async def unicorn_exception_handler(request: Request, exc: NotImplementedException):
    return JSONResponse(
        status_code=405,
        content={"message": f"{exc}"},
    )