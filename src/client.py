import json

import requests

import Constants
import Secrets
from util import Address


class GeoAPI:
    def __init__(self, url, api_key, address: Address):
        self.url = url
        self.api_key = api_key
        self.address = address

    def make_query(self):
        params = self.address.address_params()
        params['api_key'] = self.api_key
        # Make a GET request to the API
        return requests.get(self.url, params=params)

    def make_query_address(self):
        params = {Constants.GEO_API_QUERY_PARAMETER: str(self.address), Constants.GEO_API_KEY_PARAMETER: self.api_key}

        return requests.get(self.url, params=params)

    @staticmethod
    def get_lat_long_from_response(response: requests.Response):
        # Get the latitude and longitude from the response
        return response.json()[Constants.GEO_API_RESULTS_KEY][Constants.GEO_API_LOCATION_INDEX][Constants.GEO_API_LOCATION_KEY]


class YelpAPI:
    def __init__(self, url, api_key, params):
        self.url = url
        self.api_key = api_key
        self.params = params

    def make_query(self):
        return requests.get(self.url, params=self.params, headers=Constants.YELP_API_HEADERS)


if __name__ == '__main__':
    address = Address('1600 Pennsylvania Ave NW', 'Washington', 'DC', '20500', 'USA')
    geo_api = GeoAPI('https://api.geocod.io/v1.7/geocode', Secrets.GEO_API_KEY, address)
    response = geo_api.make_query_address()
    longitude_latitude = geo_api.get_lat_long_from_response(response)

    params = {'longitude': longitude_latitude['lng'], 'latitude': longitude_latitude['lat'], 'radius': 40000, 'categories': 'Food',
              'sort_by': 'best_match', 'limit': 50}

    yelp_api = YelpAPI('https://api.yelp.com/v3/businesses/search', Secrets.YELP_API_KEY, params)
    response = yelp_api.make_query()
    # Print pretty JSON data with formatting
    print(json.dumps(response.json(), indent=4))
