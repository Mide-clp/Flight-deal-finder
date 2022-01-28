import requests
from dotenv import load_dotenv
import os
load_dotenv()

AUTH = os.getenv("AUTHORIZATION")
ENDPOINT = os.getenv("URL_SHEETY_P")


class DataManager:

    def __init__(self):
        self.destination_data = {}

    def get_data(self):
        response = requests.get(url=ENDPOINT, auth=AUTH)
        response = response.json()
        self.destination_data = response["prices"]
        return self.destination_data

    # update the IATA data in the spreadsheet
    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]},
            }

            # updating the IATA rown the spreedsheet using id
            response = requests.put(url=f"{ENDPOINT}/{city['id']}", json=new_data, auth=AUTH)
            print(response.text)
