from twilio.rest import Client
import smtplib
from dotenv import load_dotenv
import os
load_dotenv()

ACCOUNT_SID = os.getenv("ACCOUNT")
AUTH_TOKEN = os.getenv("TOKEN")
ACCOUNT_NUMBER = os.getenv("NUMBER")
USER_NUMBER = os.getenv("RECIPIENT")
EMAIL = os.getenv("YOUR_EMAIL")
PASSWORD = os.getenv("YOUR_PASSWORD")


class NotificationManager:

    # this method is used to send message
    def send_message(self, message):
        # Authenticating
        client = Client(ACCOUNT_SID, AUTH_TOKEN)

        # send message
        message = client.messages.create(
            body=message,
            from_=ACCOUNT_NUMBER,
            to=USER_NUMBER,
        )
        print(message.status)

    def send_email(self, emails, mail):

        msg = f"Subject: FLight Discount\n\n{mail}"

        # sending mail to each email in emails
        for email in emails:
            with smtplib.SMTP("smtp.gmail.com") as message:
                message.starttls()
                message.login(user=EMAIL, password=PASSWORD)
                message.sendmail(from_addr=EMAIL, to_addrs=email, msg=msg.encode('utf-8'))
            print(f"sent to: {email}")

