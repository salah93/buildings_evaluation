import csv
import sys
import os
from invisibleroads_macros.disk import make_folder


TEST_FOLDER = os.path.dirname(os.path.abspath(__file__))
# insert module in sys path so you can import
sys.path.insert(0, os.path.dirname(TEST_FOLDER))
from nearby import get_nearby_places, get_nearby_transit, geomap


def test_get_nearby_places():
    address = "1724 church avenue brooklyn, ny"
    search_query = "grocery_or_supermarket"
    stores_in_area = get_nearby_places(address, search_query)
    # a lot of stores in area, TODO: think of better test
    assert len(stores_in_area) > 5
    unfiltered_search = get_nearby_places(address)
    assert len(unfiltered_search) > len(stores_in_area)


def test_get_nearby_transit():
    address = "1724 church avenue brooklyn, ny"
    transit_stops_in_area = get_nearby_transit(address)
    # train station and bus stop by location
    assert len(transit_stops_in_area) >= 2


def test_geomap():
    address = "1724 church avenue brooklyn, ny"
    target_path = 'results'
    make_folder(target_path)
    search_query = 'grocery_or_supermarket'
    geomap(address, search_query, target_path)
    assert len(os.listdir(target_path)) == 1
    columns = ['latitude', 'longitude', 'fillcolor', 'radiusinpixels']
    target_file = os.path.join(target_path, os.listdir(target_path)[0])
    assert csv.reader(open(target_file, 'r')).next() == columns
