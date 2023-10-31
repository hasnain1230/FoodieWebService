import requests, Constants, Secrets, Errors
from flask import Flask, jsonify, request
from flask.views import MethodView

app = Flask(__name__)


class Address:
    def __init__(self, street, city, state, postal_code, country):
        self.street = street.replace(' ', '+')
        self.city = city.replace(' ', '+')
        self.state = state.replace(' ', '+')
        self.postal_code = postal_code
        self.country = country.replace(' ', '+')

    def address_params(self):
        return {'street': self.street, 'city': self.city, 'state': self.state, 'postal_code': self.postal_code, 'country': self.country}

    def __str__(self):
        return f'{self.street}+{self.city}+{self.state}+{self.postal_code}+{self.country}'


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
        params = {'q': str(self.address), 'api_key': self.api_key}

        return requests.get(self.url, params=params)

    @staticmethod
    def get_lat_long_from_response(response: requests.Response):
        # Get the latitude and longitude from the response
        return response.json()['results'][0]['location']


class RestaurantAPI(MethodView):
    @staticmethod
    def get():
        if request.method != 'GET':
            return jsonify(Errors.errors.get("invalid_http_method")), 405

        address_json = request.get_json()

        if not RestaurantAPI.validate_address(address_json):
            return jsonify({'error': 'Invalid address'}), 400

        address = Address(address_json['street'], address_json['city'], address_json['state'],
                          address_json['postal_code'], address_json['country'])

        geo_api = GeoAPI(Constants.GEO_API_URL, Secrets.GEO_API_KEY, address)
        response = geo_api.make_query_address()

        if response.status_code != 200:
            return jsonify(Errors.errors.get("latitude/longitude")), 400
        else:
            return jsonify(geo_api.get_lat_long_from_response(response))

    @staticmethod
    def validate_address(address_json):
        valid_keys = ['street', 'city', 'state', 'postal_code', 'country']

        for key in valid_keys:
            if key not in address_json:
                return False

        return True


restaurant_api = RestaurantAPI.as_view('restaurant_api')
app.add_url_rule('/restaurant', view_func=restaurant_api, methods=['GET'])

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
