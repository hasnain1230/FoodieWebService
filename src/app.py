import werkzeug
from flask import Flask, jsonify, request
from flask.views import MethodView
from util import Address
from werkzeug.exceptions import BadRequest
from client import GeoAPI, YelpAPI

import Constants
import Errors
from src import Secrets

app = Flask(__name__)


class RestaurantAPI(MethodView):
    @staticmethod
    def get():
        if request.method != 'GET':
            return jsonify(Errors.errors.get(Constants.LATITUDE_LONGITUDE_BAD_REQUEST_ERROR)), 405

        if not RestaurantAPI.validate_request(request):
            return jsonify(Errors.errors.get(Constants.INVALID_REQUEST_FORMAT)), 400

        address = RestaurantAPI.create_address(request.get_json())
        latitude_longitude = RestaurantAPI.process_address_request(address).get_json()

        return RestaurantAPI.process_yelp_response(RestaurantAPI.process_yelp_search(latitude_longitude).json())

    @staticmethod
    def handle_response_errors(response, error_type): # TODO: Hasnain, fix this
        if 400 <= response.status_code < 500 and response.status_code != 404:
            return jsonify(Errors.errors.get(f"{error_type}_BAD_REQUEST_ERROR")), 400
        elif response.status_code == 404:
            return jsonify(Errors.errors.get(f"{error_type}_NOT_FOUND_ERROR")), 404
        elif 500 <= response.status_code < 600:
            return jsonify(Errors.errors.get(f"{error_type}_INTERNAL_SERVER_ERROR")), 500
        else:
            return response

    @staticmethod
    def validate_request(request):
        # Check if request contains JSON data
        if not request.is_json:
            return False

        # Attempt to parse JSON data
        try:
            data = request.get_json()
        except BadRequest:
            return False

        # Ensure data is a dictionary
        if not isinstance(data, dict):
            return False

        # Check for None values
        for key, value in data.items():
            if not isinstance(key, str) or value is None:
                return False

        # If all checks pass
        return True

    @staticmethod
    def process_yelp_response(yelp_response_json):
        formatted_response = {
            'restaurants': []
        }

        for business in yelp_response_json['businesses']:
            restaurant = {
                'name': business['name'],
                'address': ', '.join(business['location']['display_address']),
                'rating': business['rating']
            }

            formatted_response['restaurants'].append(restaurant)

        return formatted_response

    @staticmethod
    def process_yelp_search(latitude_longitude):
        params = Constants.YELP_SEARCH_BASIC_PARAMETERS

        for key, value in latitude_longitude.items():
            if value is None:
                return jsonify(Errors.errors.get(Constants.LATITUDE_LONGITUDE_BAD_REQUEST_ERROR)), 400

            params[Constants.GEO_TO_YELP_API_KEY_MAPPINGS[key]] = value

        yelp_api = YelpAPI(Constants.YELP_API_URL, Secrets.YELP_API_KEY, params)
        response = yelp_api.make_query()

        if 400 <= response.status_code < 500 and response.status_code != 404:
            return jsonify(Errors.errors.get(Constants.YELP_SEARCH_BAD_REQUEST_ERROR)), 400
        elif response.status_code == 404:
            return jsonify(Errors.errors.get(Constants.YELP_SEARCH_NOT_FOUND_ERROR)), 404
        elif 500 <= response.status_code < 600:
            return jsonify(Errors.errors.get(Constants.YELP_SEARCH_INTERNAL_SERVER_ERROR)), 500
        else:
            return response

        return yelp_api.make_query()

    @staticmethod
    def process_address_request(address: Address):
        geo_api = GeoAPI(Constants.GEO_API_URL, Secrets.GEO_API_KEY, address)
        response = geo_api.make_query_address()

        if 400 <= response.status_code < 500 and response.status_code != 404:
            return jsonify(Errors.errors.get(Constants.LATITUDE_LONGITUDE_BAD_REQUEST_ERROR)), 400
        elif response.status_code == 404:
            return jsonify(Errors.errors.get(Constants.LATITUDE_LONGITUDE_NOT_FOUND_ERROR)), 404
        elif 500 <= response.status_code < 600:
            return jsonify(Errors.errors.get(Constants.LATITUDE_LONGITUDE_INTERNAL_SERVER_ERROR)), 500
        else:
            return response

    @staticmethod
    def create_address(address_json):
        if not RestaurantAPI.validate_address(address_json):
            return jsonify(Errors.errors[Constants.LATITUDE_LONGITUDE_BAD_REQUEST_ERROR]), 400

        address_attributes = [address_json[key] for key in
                              Constants.ADDRESS_VALID_KEYS + list(Constants.ADDRESS_DEFAULT_VALUES.keys())]

        return Address(*address_attributes)

    @staticmethod
    def validate_address(address_json):
        valid_keys = Constants.ADDRESS_VALID_KEYS
        default_values = Constants.ADDRESS_DEFAULT_VALUES

        # Ensure required keys are present
        if not all(key in address_json for key in valid_keys):
            return False

        # Add default values for missing optional keys
        for key, value in default_values.items():
            address_json.setdefault(key, value)

        # Ensure there are no extra keys
        all_valid_keys = valid_keys + list(default_values.keys())

        if len(address_json.keys()) != len(all_valid_keys):
            return False

        return True


restaurant_api = RestaurantAPI.as_view(Constants.RESTAURANT_VIEW_API)
app.add_url_rule(Constants.RESTAURANT_ENDPOINT, view_func=restaurant_api, methods=['GET'])

if __name__ == '__main__':
    app.run(host=Constants.HOST, port=Constants.PORT, debug=True)

