from collections import namedtuple

import aiohttp

MAPS_URL = "https://maps.googleapis.com"
Coordinate = namedtuple("Coordinate", field_names=["lat", "long"])


class GoogleMapsClient:
    def __init__(self, api_key: str):
        self._api_key = api_key

    async def __aenter__(self):
        self._session = aiohttp.ClientSession(base_url=MAPS_URL)
        return self

    async def __aexit__(self, exc_type, exc_value, exc_tb):
        await self._session.close()

    async def geocode(self, address: str) -> Coordinate:
        # https://developers.google.com/maps/documentation/geocoding/requests-geocoding
        response = await self._session.get(
            "/maps/api/geocode/json",
            params={"address": address, "key": self._api_key},
        )
        json_body = await response.json()
        results = json_body["results"]
        if len(results) != 1:
            # TODO:
            # len(results) == 0 -> return address not found (404)
            # len(results) > 1 -> return ambigous address error ()
            raise NotImplementedError()

        address_response = results[0]
        location = address_response["geometry"]["location"]
        return Coordinate(location["lat"], location["lng"])
