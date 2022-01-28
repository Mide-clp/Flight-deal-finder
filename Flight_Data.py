import requests
import pprint


class FlightData:
    def __init__(self, price, city_from, city_to, fly_from, fly_to, flight_date, return_date, stop, via_city):
        self.price = price
        self.city_from = city_from
        self.city_to = city_to
        self.fly_from = fly_from
        self.fly_to = fly_to
        self.flight_date = flight_date
        self.return_date = return_date
        self.stop = stop
        self.via_city = via_city

        pass
