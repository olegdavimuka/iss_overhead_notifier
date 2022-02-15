import time
import os
import requests
from datetime import datetime
import smtplib

MY_LAT = 48.598538
MY_LONG = 22.274249
MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")
TO_EMAIL = "olegdavimuka00@gmail.com"


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    longitude = float(data["iss_position"]["longitude"])
    latitude = float(data["iss_position"]["latitude"])
    if abs(MY_LAT - latitude) <= 5 and abs(MY_LONG - longitude) <= 5:
        return True
    else:
        return False


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise_hour = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset_hour = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    hour_now = datetime.now().hour
    if hour_now in range(sunrise_hour, sunset_hour):
        return True
    else:
        return False


def send_message():
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=TO_EMAIL,
            msg="Subject:Look up!\n\n"
                "The sputnik is here!"
        )


while True:
    if is_iss_overhead() and is_night():
        send_message()
    time.sleep(60)
