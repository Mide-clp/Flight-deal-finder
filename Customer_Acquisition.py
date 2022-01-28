import requests
from dotenv import load_dotenv
import os

load_dotenv()
ENDPOINT = os.getenv("URL_SHEETY_U")
AUTH = os.getenv("AUTHORIZATION")
headers = os.getenv("HEADERS")


class CustomerAcquisition:
    # requesting customers details
    def add_customer(self):
        confirm = False
        while confirm:
            print("welcome to flight club\nwe find the best flight deals and email you")
            f_name = input("What is your first name? ")
            l_name = input("What is your last name? ")
            email = input("what is your email? ")
            confirm_email = input("Type your email again? ")

            # confirming customer email before sending message
            if email == confirm_email:
                confirm = True
                details = {
                    "user": {
                        "firstName": f_name,
                        "lastName": l_name,
                        "email": email,
                    }
                }

                # saving customers details to the spreadsheet
                response = requests.post(url=ENDPOINT, json=details, headers=headers)
                print(response.text)

    def get_users(self):
        # getting user emails
        response = requests.get(url=ENDPOINT, headers=headers)
        data = response.json()["users"]
        email = [mail["email"] for mail in data]
        return email
