from datetime import *
import os
from requests import *

# 1. Pull hidden variables from the environment
SHEET_ENDPOINT = os.environ.get("SHEET_ENDPOINT")
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")
APP_ID = os.environ.get("X_APP_ID")
APP_KEY = os.environ.get("X_APP_KEY")

nut_url = "https://app.100daysofpython.dev/v1/nutrition/natural/exercise"

# 2. Check if text is coming from GitHub browser inputs, otherwise ask local terminal
if os.environ.get("DEFAULT_QUERY"):
    query_text = os.environ.get("DEFAULT_QUERY")
else:
    query_text = input("Tell me which exercise u did: ")

headers_nut = {
    "x-app-id": f"{APP_ID}",
    "x-app-key": f"{APP_KEY}"
}

body_nut = {
    "query": query_text,
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

# 3. Request data from Nutritionix
response_nut = post(nut_url, json=body_nut, headers=headers_nut)

# 4. Loop dynamically over every exercise returned
for i in response_nut.json()["exercises"]:
    exe = (i["name"]).title()
    tim = i["duration_min"]
    cal = i["nf_calories"]

    body_she = {
        "workout": {
            "date": current_date,
            "time": current_time,
            "exercise": exe,
            "duration": tim,
            "calories": cal
        }
    }

    # 5. Send individual rows straight to Sheety inside the loop
    response_she = post(SHEET_ENDPOINT, json=body_she, headers=headers_she)
    print(f"Added row successfully: {exe}")
    print(f"API Response Details: \n {response_she.json()}\n")
