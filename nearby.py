import geopy
import requests
from api_keys import places_key


RADIUS = 300


def get_nearby_places(address, search_type):
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    google_geo = geopy.GoogleV3()
    location = google_geo.geocode(address)
    location = str(location.latitude) + ',' + str(location.longitude)
    params = dict(location=location, radius=RADIUS,
                  type=search_type, key=places_key)
    response = requests.get(url, params)
    return response.json()['results']


def get_nearby_transit(address):
    results = []
    types = ['bus_station', 'subway_station']
    for query in types:
        results.extend(get_nearby_places(address, query))
    return results
