import requests
from Flight_Data import FlightData
from pprint import pprint
from dotenv import load_dotenv
import os
load_dotenv()

API_KEY = os.getenv("KEY")
ENDPOINT = os.getenv("TEQUILA")


class FlightSearch:
    def get_destination_code(self, city_name):
        # defining the parameter to get IATA code
        data = {
            "term": city_name,
            "location_types": "city",
            "limit integer": 1,

        }

        headers = {
            "apikey": API_KEY,
        }
        # pulling IATA codes from endpoint
        response = requests.get(url=ENDPOINT, params=data, headers=headers)
        response.raise_for_status()
        data = response.json()
        # assigning IATA code
        code = data["locations"][0]["code"]

        return code

    def check_flight(self, origin, to_code, from_date, to_date):
        endpoint = os.getenv("TEQUILA_SEARCH")

        # stop over before location
        stop_over = 0

        # headers for authentication
        headers = {
            "apikey": API_KEY,
        }
        # parameter being passed to the flight search endpoint
        parameter = {
            "fly_from": origin,
            "fly_to": to_code,
            "date_from": from_date,
            "date_to": to_date,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": stop_over,
            "curr": "GBP",
        }

        # getting the data from the the API
        response = requests.get(url=endpoint, params=parameter, headers=headers)
        response.raise_for_status()

        # picking the first search data
        try:
            data = response.json()["data"][0]

        # if there's a city that has no data in "max:stop": 1., then parameters "max_stopovers": 1

        except IndexError:
            try:
                stop_over = 1
                parameter = {
                    "fly_from": origin,
                    "fly_to": to_code,
                    "date_from": from_date,
                    "date_to": to_date,
                    "nights_in_dst_from": 7,
                    "nights_in_dst_to": 28,
                    "flight_type": "round",
                    "one_for_city": 1,
                    "max_stopovers": stop_over,
                    "curr": "GBP",
                }

                # getting the data from the API
                response = requests.get(url=endpoint, params=parameter, headers=headers)
                response.raise_for_status()
                data = response.json()["data"][0]
            except IndexError:
                # print("no data1")
                return None

        # passing parameter needed for the flight data

        flight_data = FlightData(
            price=data["price"],
            city_from=data["cityFrom"],
            city_to=data["cityTo"],
            fly_from=data["flyFrom"],
            fly_to=data["flyTo"],
            flight_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0],
            stop=stop_over,
            via_city=data["route"][0]["cityTo"],

            )
        # print(f"{flight_data.city_to}: £{flight_data.price}")
        return flight_data

