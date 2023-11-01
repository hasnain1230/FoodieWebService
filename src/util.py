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

