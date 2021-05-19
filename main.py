import requests
import os
from datetime import datetime

# Sheety setup:
SHEETY_APP_ID = os.getenv("SHEETY_IX_ID")
SHEETY_APP_KEY = os.getenv("SHEETY_IX_KEY")
SHEETY_EXERCISE_ENDPOINT = f"https://api.sheety.co/{SHEETY_APP_ID}/workoutTracking/workouts"
SHEETY_BASE64 = os.getenv("SHEETY_BASE64")
sheety_headers = {
    "Authorization": f"Bearer {SHEETY_BASE64}",
}
sheety_params = {"workout": {
    "date": "",
    "time": "",
    "exercise": "",
    "duration": "",
    "calories": "",
}}
# NutritionIX setup:
NUT_APP_ID = os.getenv("NUTRITION_IX_ID")
NUT_APP_KEY = os.getenv("NUTRITION_IX_KEY")
NUT_EXERCISE_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
nut_app_headers = {
    "x-app-key": NUT_APP_KEY,
    "x-app-id": NUT_APP_ID,
}
nut_user_params = {
    "gender": "male",
    "weight_kg": 73.5,
    "height_cm": 185.03,
    "age": 27
}
# Preparing a dict with date and time for today's date:
now = datetime.now()
today_date_string = now.strftime("%d/%m/%Y")
time_form = now.time()
today_time = ((time_form.hour + ((time_form.minute + (time_form.second / 60.0)) / 60.0)) / 24.0)

# Getting the user input in natural language:
nut_user_input = {
    "query": input("What did you do today? ")
}
nut_user_params.update(nut_user_input)

# Making requests to APIs:
response = requests.post(url=NUT_EXERCISE_ENDPOINT, json=nut_user_params, headers=nut_app_headers)

# Formatting the data with only the fields we need from the JSON:
exercise_data = response.json()
exercise_data = [{
    "Exercise": item["name"],
    "Duration": item["nf_calories"],
    "Calories": item["duration_min"],
    }
                 for item
                 in exercise_data["exercises"]]

# Updating params dict with the acquired data from NUT:
for exercise in exercise_data:
    sheety_params.update({"workout": {
        "date": today_date_string,
        "time": today_time,
        "exercise": exercise["Exercise"],
        "duration": exercise["Duration"],
        "calories": exercise["Calories"],
    }})
    response = requests.post(url=SHEETY_EXERCISE_ENDPOINT, json=sheety_params, headers=sheety_headers)
    print(response.status_code)
    print(response.text)
    print(sheety_params)
