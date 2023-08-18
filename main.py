import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


def nutritionix_data(exercise_text):
    uri = "https://trackapi.nutritionix.com//v2/natural/exercise"

    headers = {
        "x-app-id": os.environ["nutritionix_app_id"],
        "x-app-key": os.environ["nutritionix_api_key"],
    }

    params = {
        "query": exercise_text,
        "gender": "male",
        "weight_kg": 97,
        "height_cm": 190,
        "age": 27
    }

    r = requests.post(url=uri, data=params, headers=headers)
    r.raise_for_status()
    return r.json()['exercises']


def write_to_sheety(data):
    uri = f"https://api.sheety.co/{os.environ['sheety_id']}/myWorkouts/workouts"
    header = {
        "Authorization": f"Bearer {os.environ['sheety_api_key']}"
    }
    for d in data:
        params = {"workout": d}
        r = requests.post(url=uri, json=params, headers=header)
        r.raise_for_status()
        print(r.text)


exercise_text = input("Tell me which exercises you did: ")

workout_info = nutritionix_data(exercise_text)

date = datetime.now().date().strftime("%d/%m/%Y")
time = datetime.now().time().strftime("%H:%M:%S")
data = [{
    "date": date,
    "time": time,
    "exercise": d["name"].title(),
    "duration": d["duration_min"],
    "calories": d["nf_calories"]}
    for d in workout_info
]
write_to_sheety(data)
