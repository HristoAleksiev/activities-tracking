import requests
import os

APP_ID = os.getenv("NUTRITION_IX_ID")
APP_KEY = os.getenv("NUTRITION_IX_KEY")
APP_EXERCISE_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"

user_params = {
    "gender": "male",
    "weight_kg": 73.5,
    "height_cm": 185.03,
    "age": 27
}

user_input = {
    "query": input("What did you do today? ")
}

user_params.update(user_input)
