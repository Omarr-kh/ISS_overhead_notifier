import requests
import datetime
import smtplib
import time

MY_LAT = 29.983320
MY_LNG = 31.016930

EMAIL = "email@gmail.com"
PASS = "pass"


def is_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()['iss_position']

    iss_lat = float(data["latitude"])
    iss_long =float(data["longitude"])

    if (MY_LAT - 5 <= iss_lat <= MY_LAT + 5) and (MY_LNG - 5 <= iss_long <= MY_LNG + 5):
        return True
    else:
        return False


param = {
    "lat": MY_LAT,
    "lng": MY_LNG,
    "formatted": 0,
}


def is_dark():# 
    response = requests.get(url="https://api.sunrise-sunset.org/json", params=param)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split('T')[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True
    return False

while True:
    time.sleep(60)
    if is_overhead() and is_dark():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(EMAIL, PASS)
            connection.sendmail(
                from_addr=EMAIL,
                to_addrs=EMAIL,
                msg=f"Subject:Look Up!\n\nThe ISS is above you!\nGo look at it."
            )
            print("success")
