from collections import namedtuple

import aiohttp

Coordinate = namedtuple("Coordinate", field_names=["lat", "long"])


class AddressNotFound(ValueError):
    pass


class MultipleAddressesFound(ValueError):
    pass


class GoogleMapsClient:
    def __init__(self, api_key: str):
        self._api_key = api_key

    async def __aenter__(self):
        self._session = aiohttp.ClientSession(base_url="https://maps.googleapis.com")
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
        if len(results) == 0:
            raise AddressNotFound
        elif len(results) == 1:
            address_response = results[0]
            location = address_response["geometry"]["location"]
            return Coordinate(location["lat"], location["lng"])
        else:
            raise MultipleAddressesFound
