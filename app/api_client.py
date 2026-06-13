import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
API_KEY = os.getenv("API_KEY")


def predict_price(airline, source_city, destination_city, stops, flight_class, duration, days_left):
    try:
        response = requests.post(
            f"{API_URL}/predict",
            headers={"X-API-Key": API_KEY},
            json={
                "airline": airline,
                "source_city": source_city,
                "destination_city": destination_city,
                "stops": stops,
                "class": flight_class,
                "duration": duration,
                "days_left": days_left,
            },
            timeout=5,
        )
        response.raise_for_status()
        return response.json()
    except Exception:
        return None
