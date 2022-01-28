from Data_Manager import DataManager
from Customer_Acquisition import CustomerAcquisition
from Flight_Search import FlightSearch
from datetime import datetime, timedelta
from Notification_Manager import NotificationManager

# customer acquisition details
customer_acquisition = CustomerAcquisition()

# add customer details
member = False
if member:
    customer_acquisition.add_customer()

# assigning class to variables
data_manager = DataManager()
sheet_data = data_manager.get_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()

ORIGIN_IATA = "LON"

# checking if iatacode is empty, if empty fill iata code
if sheet_data[0]["iataCode"] == "":
    from Flight_Search import FlightSearch

    # looping through the sheet_data to update it with each city IATA code
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    print(f"sheet_data:\n {sheet_data}")

    # updating the data
    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()

# getting the date needed
date = datetime.now()
months = date + timedelta(days=180)
# from date and to date
today = date.strftime("%d/%m/%Y")
next_6_months = months.strftime("%d/%m/%Y")

# activate the code to send message
send = True

# looping to search for each city flight data
if send:
    for destination in sheet_data:
        # print(destination)
        #  passing parameter needed for the check_flight method

        flights = flight_search.check_flight(origin=ORIGIN_IATA,
                                             to_code=destination["iataCode"],
                                             from_date=today,
                                             to_date=next_6_months)

        try:
            # if flight price lower than our minimum price
            if flights.price < destination["lowestPrice"]:
                if flights.stop == 0:
                    msg = f"Low price alert! Only £{flights.price} to fly from {flights.city_from}-" \
                          f"{flights.fly_from} to {flights.city_to}-{flights.fly_to}, from {flights.flight_date}" \
                          f" to {flights.return_date}. "
                else:
                    msg = f"Low price alert! Only £{flights.price} to fly from {flights.city_from}-" \
                          f"{flights.fly_from} to {flights.city_to}-{flights.fly_to}, from {flights.flight_date} to " \
                          f" {flights.return_date}.\nFlight has {flights.stop} stop over, via {flights.via_city} city"
                link = f"https://www.google.co.uk/flights?hl=en#flt={flights.fly_from}.{flights.fly_to}." \
                       f"{flights.flight_date}*{flights.fly_to}.{flights.fly_from}.{flights.return_date}"
                send_message = f"{msg}:\n\n{link}"
                # sending email
                print(send_message)
                email = customer_acquisition.get_users()
                notification_manager.send_email(emails=email, mail=send_message)

                # sending message
                notification_manager.send_message(msg)

        # if an attribute error occurs
        except AttributeError:
            pass
