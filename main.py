import os
from datetime import *

nut_url = "https://app.100daysofpython.dev/v1/nutrition/natural/exercise"
she_url = os.environ.get("SHEET_ENDPOINT")

BEARER_TOKEN = os.environ.get("BEARER_TOKEN")
APP_ID = os.environ.get("X_APP_ID")
APP_KEY = os.environ.get("X_APP_KEY")

headers_nut = {
    "x-app-id" : f"{APP_ID}",
    "x-app-key":f"{APP_KEY}"
}

body_nut = {
    "query": input("Tell me which exercise u did: "),
    "weight_kg": 70,
    "height_cm": 175,
    "age": 30,
    "gender": "male"
}

headers_she = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "Content-Type": "application/json"
}

now = datetime.now()
current_date = now.strftime("%d/%m/%Y")
current_time = now.strftime("%H:%M:%S")



response_nut = post(nut_url, json=body_nut, headers=headers_nut)

for i in response_nut.json()["exercises"]:
    exe = (i["name"]).title()
    tim = i["duration_min"]
    cal = i["nf_calories"]

    body_she = {
        "workout":{
            "date":current_date,
            "time":current_time,
            "exercise":exe,
            "duration":tim,
            "calories":cal
        }
    }

    response_she = post(she_url, json=body_she, headers=headers_she)

# Print the structured workout data

    print(f"Nutrition API call: \n {response_she.json()}")
