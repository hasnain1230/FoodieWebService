import Secrets

GEO_API_URL = 'https://api.geocod.io/v1.7/geocode'
INVALID_REQUEST_FORMAT = 'invalid_request_format'
LATITUDE_LONGITUDE_BAD_REQUEST_ERROR = 'latitude/longitude_bad_request'
LATITUDE_LONGITUDE_NOT_FOUND_ERROR = 'latitude/longitude_not_found'
LATITUDE_LONGITUDE_INTERNAL_SERVER_ERROR = 'latitude/longitude_internal_server_error'
YELP_SEARCH_BAD_REQUEST_ERROR = 'yelp_search_bad_request'
YELP_SEARCH_NOT_FOUND_ERROR = 'yelp_search_not_found'
YELP_SEARCH_INTERNAL_SERVER_ERROR = 'yelp_search_internal_server_error'
INVALID_HTTP_METHOD_ERROR = 'invalid_http_method'
ADDRESS_VALID_KEYS = ['street', 'city', 'state', 'postal_code']
ADDRESS_DEFAULT_VALUES = {'country': 'USA'}
RESTAURANT_VIEW_API = 'restaurant_api'
RESTAURANT_ENDPOINT = '/restaurant'

GEO_API_KEY_PARAMETER = 'api_key'
GEO_API_QUERY_PARAMETER = 'q'

GEO_API_RESULTS_KEY = 'results'
GEO_API_LOCATION_INDEX = 0
GEO_API_LOCATION_KEY = 'location'

GEO_TO_YELP_API_KEY_MAPPINGS = {
    'lat': 'latitude',
    'lng': 'longitude'
}

YELP_SEARCH_BASIC_PARAMETERS = {
    'latitude': None,
    'longitude': None,
    'radius': 40000,
    'categories': 'Food',
    'sort_by': 'best_match',
    'limit': 50
}
YELP_API_URL = 'https://api.yelp.com/v3/businesses/search'
YELP_API_CATEGORY = 'Food'
YELP_API_HEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {Secrets.YELP_API_KEY}"
}


HOST = 'localhost'
PORT = 5000

if __name__ == "__main__":
    my_dict = {"a": "b", "c": "d"}

    for key in my_dict.values():
        print(key)