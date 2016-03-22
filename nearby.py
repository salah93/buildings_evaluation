import argparse
import csv
import geopy
import os
import requests
from api_keys import places_key
from invisibleroads_macros.disk import make_folder


RADIUS = 600


def get_nearby_places(address, search_query=None):
    # places search api
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    google_geo = geopy.GoogleV3()
    try:
        location = google_geo.geocode(address)
    except geopy.GeocoderTimedOut:
        return []
    location = str(location.latitude) + ',' + str(location.longitude)
    params = dict(location=location, radius=RADIUS,
                  key=places_key)
    if search_query:
        params['type'] = search_query
    response = requests.get(url, params=params)
    return response.json()['results']


def get_nearby_transit(address):
    results = []
    # only allowed one type search per query
    # (multiple-type searches is deprecated)
    types = ['bus_station', 'subway_station']
    for query in types:
        results.extend(get_nearby_places(address, query))
    return results


def get_nearby_schools(address):
    query = "school"
    results = get_nearby_places(address, query)
    return results


def geomap(address, search_query, target_folder=None):
    if not address.strip():
        return []
    search_query = search_query.strip()
    searches = get_nearby_places(address, search_query)
    transit = get_nearby_transit(address)
    schools = get_nearby_schools(address)
    google_geo = geopy.GoogleV3()
    # get lat/lng of given address
    coordinates = google_geo.geocode(address)
    building_descr = ("Queried Building", "red", 20)
    searches_descr = ("Nearby " + search_query, "green", 10)
    transit_descr = ("Nearby bus or subway", "blue", 10)
    school_descr = ("Nearby School", "yellow", 10)
    building = dict(description=building_descr[0],
                    latitude=coordinates.latitude,
                    longitude=coordinates.longitude,
                    color=building_descr[1],
                    radius=building_descr[2])
    points_list = [building]
    add_to_csv(searches, searches_descr, points_list)
    add_to_csv(transit, transit_descr, points_list)
    add_to_csv(schools, school_descr, points_list)
    if target_folder:
        path = os.path.join(target_folder, 'search.csv')
        with open(path, 'w') as csvfile:
            columns = ('description', 'latitude',
                       'longitude', 'FillColor', 'radius_in_pixels')
            writer = csv.writer(csvfile)
            writer.writerow(columns)
            writer.writerows([(row['description'],
                               row['latitude'],
                               row['longitude'],
                               row['color'],
                               row['radius'])
                              for row in points_list])
        # required print statement for crosscompute
        #   (http://crosscompute.com/docs)
        print('coordinates_geotable_path = ' + path)
    building = dict(latitude=building['latitude'],
                    longitude=building['longitude'])
    return dict(address=building, points=points_list)


def add_to_csv(item_list, description, csv_list=None):
    for query in item_list:
        location = dict(description=description[0],
                        latitude=query['geometry']['location']['lat'],
                        longitude=query['geometry']['location']['lng'],
                        color=description[1],
                        radius=description[2])
        csv_list.append(location)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--target_folder',
                        type=make_folder, default='results')
    parser.add_argument('--address',
                        type=str, required=True)
    parser.add_argument('--search_query',
                        type=str, default=None)
    args = parser.parse_args()
    geomap(args.address, args.search_query, args.target_folder)
