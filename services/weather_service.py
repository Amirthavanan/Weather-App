import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5"

def get_current_weather(city=None, country=None):
    if not API_KEY or API_KEY == "your_openweather_api_key":
        return {"error": "API Key is missing or invalid."}
    
    query = ""
    if city and country:
        query = f"{city},{country}"
    elif city:
        query = city
    elif country:
        query = country
    else:
        return {"error": "Please provide a city or country."}

    url = f"{BASE_URL}/weather?q={query}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def get_forecast(city):
    if not API_KEY or API_KEY == "your_openweather_api_key":
        return {"error": "API Key is missing or invalid."}
        
    url = f"{BASE_URL}/forecast?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
