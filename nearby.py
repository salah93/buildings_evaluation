import argparse
import csv
from os import environ
from os.path import join

import geopy
import numpy as np
import pandas as pd
import requests
from invisibleroads_macros.disk import make_folder

types = ['accounting',
         'airport',
         'amusement_park',
         'aquarium',
         'art_gallery',
         'atm',
         'bakery',
         'bank',
         'bar',
         'beauty_salon',
         'bicycle_store',
         'book_store',
         'bowling_alley',
         'bus_station',
         'cafe',
         'campground',
         'car_dealer',
         'car_rental',
         'car_repair',
         'car_wash',
         'casino',
         'cemetery',
         'church',
         'city_hall',
         'clothing_store',
         'convenience_store',
         'courthouse',
         'dentist',
         'department_store',
         'doctor',
         'electrician',
         'electronics_store',
         'embassy',
         'fire_station',
         'florist',
         'funeral_home',
         'furniture_store',
         'gas_station',
         'gym',
         'hair_care',
         'hardware_store',
         'hindu_temple',
         'home_goods_store',
         'hospital',
         'insurance_agency',
         'jewelry_store',
         'laundry',
         'lawyer',
         'library',
         'liquor_store',
         'local_government_office',
         'locksmith',
         'lodging',
         'meal_delivery',
         'meal_takeaway',
         'mosque',
         'movie_rental',
         'movie_theater',
         'moving_company',
         'museum',
         'night_club',
         'painter',
         'park',
         'parking',
         'pet_store',
         'pharmacy',
         'physiotherapist',
         'plumber',
         'police',
         'post_office',
         'real_estate_agency',
         'restaurant',
         'roofing_contractor',
         'rv_park',
         'school',
         'shoe_store',
         'shopping_mall',
         'spa',
         'stadium',
         'storage',
         'store',
         'subway_station',
         'synagogue',
         'taxi_stand',
         'train_station',
         'transit_station',
         'travel_agency',
         'university',
         'veterinary_care',
         'zoo']


class InvalidSearchParameter(Exception):
    pass


def get_nearby_places(lat, lng, search_query, radius):
    if search_query not in types:
        raise InvalidSearchParameter
    location = str(lat) + ',' + str(lng)
    # places search api
    places_api = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    params = dict(location=location,
                  radius=radius,
                  type=search_query,
                  key=environ['GOOGLE_KEY'])
    results = requests.get(places_api, params=params).json()['results']
    return [(location['name'],
             location['types'][0],
             location['geometry']['location']['lat'],
             location['geometry']['location']['lng'])
            for location in results]


def get_n_distinct_colors(n):
    max_value = 255 ** 3
    colors = np.linspace(0, max_value, n, endpoint=True)
    return ['#{0}'.format(hex(I)[2:-1].zfill(6)) for I in colors]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--target_folder',
                        type=make_folder, default='results')
    parser.add_argument('--radius',
                        type=int, default=600)
    parser.add_argument('--address',
                        type=str, required=True)
    parser.add_argument('--search_queries', metavar='PATH',
                        required=True)
    args = parser.parse_args()
    queried_building_pixel_size = 20
    nearby_places_pixel_size = 10
    # geocode address
    google_geo = geopy.GoogleV3()
    location = google_geo.geocode(args.address)
    search_radius, lat, lng = args.radius, location.latitude, location.longitude
    with open(args.search_queries) as f:
        search_queries = [line.strip() for line in f.readlines()]
    colors = get_n_distinct_colors(len(search_queries) + 1)
    header = ('description', 'latitude', 'longitude', 'FillColor', 'radius_in_pixels')
    data =[]
    data.append(('queried building', lat, lng, colors[0], queried_building_pixel_size))
    for color, sq in zip(colors[1:], search_queries):
        places = get_nearby_places(lat, lng, sq, search_radius)
        for name, description, sq_lat, sq_lng in places:
            data.append((description, sq_lat, sq_lng, color, nearby_places_pixel_size))
    target_path = join(args.target_folder, 'places.csv')
    df = pd.DataFrame(data).to_csv(target_path, header=header, index=False)
    print('places_geotable_path = ' + target_path)
