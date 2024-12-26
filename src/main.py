import math
import copy
import os

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

import uvicorn

from clients.maps import GoogleMapsClient, Coordinate

QUALIFYING_DISTANCE_METERS = 10_000
FACILITIES = [
    {
        "name": "Wonthaggi Windfarms",
        "type": "WIND_FARM",
        "address": "165 Campbell St, Wonthaggi VIC 3995",
        "geometry": {"lat": -38.610439, "long": 145.565371},
    }
]
GOOGLE_MAPS_API_KEY = os.environ["GOOGLE_MAPS_API_KEY"]


def measure_distance(point1: Coordinate, point2: Coordinate):
    # Radius of earth in kilometers
    R = 6378.137
    # Convert degrees to radians
    lat1_rad = math.radians(point1.lat)
    lon1_rad = math.radians(point1.long)
    lat2_rad = math.radians(point2.lat)
    lon2_rad = math.radians(point2.long)
    # Differences in latitude and longitude
    dLat = lat2_rad - lat1_rad
    dLon = lon2_rad - lon1_rad
    # Haversine formula
    a = (
        math.sin(dLat / 2) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dLon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    # Distance in kilometers
    d = R * c
    # Convert distance to meters
    return d * 1000


async def qualify_address(request: Request):
    json_body = await request.json()
    address = json_body.get("address")
    if address is None:
        return JSONResponse({"error": "An address was not supplied"})

    # TODO: Factor our client initializer to a startup function
    client = GoogleMapsClient(GOOGLE_MAPS_API_KEY)
    address_coordinate = client.geocode(address)

    qualifying_facilities = []
    for facility in FACILITIES:
        geometry = facility["geometry"]
        facility_coordinate = Coordinate(geometry["lat"], geometry["long"])
        distance_meters = measure_distance(facility_coordinate, address_coordinate)
        if distance_meters < QUALIFYING_DISTANCE_METERS:
            qualifying_facility = copy.deepcopy(facility)
            qualifying_facility["distance_meters"] = distance_meters
            qualifying_facilities.append(qualifying_facility)

    return JSONResponse(
        {
            "address": address,
            "facilities": qualifying_facilities,
        }
    )


routes = [Route("/address/qualify", endpoint=qualify_address, methods=["POST"])]

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
]


if __name__ == "__main__":
    app = Starlette(routes=routes, middleware=middleware)
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
