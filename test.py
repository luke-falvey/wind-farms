import os

import requests

# To get a GOOGLE_API_KEY:
# 1. Visit: https://developers.google.com/maps/documentation/javascript/place-autocomplete-data
# 2. Open developer console and go to the network tab
# 3. Type an address into the search box on the page
# 4. Click on any POST request to `places.googleapis.com`, and look for the `X-Goog-Api-Key` in the request headers
GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]

address_query = "5 Fahey Street"

response = requests.post(
    "https://places.googleapis.com/$rpc/google.maps.places.v1.Places/AutocompletePlaces",
    headers={
        "X-Goog-Api-Key": GOOGLE_API_KEY,
        "Content-Type": "application/json+protobuf",
        "referer": "https://geo-devrel-javascript-samples.web.app/",
    },
    json=[address_query, None, None, None, None, "en-US"],
)

json_body = response.json()

for auto_complete in json_body[0]:
    address_query = auto_complete[0][2][0]
    print(address_query)
