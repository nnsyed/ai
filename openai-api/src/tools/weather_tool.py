import requests

def get_weather(city_name, api_key):
    # Base URL for the OpenWeatherMap Current Weather Data API
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    # Query parameters required by the API
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric"  # Use "imperial" for Fahrenheit, "metric" for Celsius
    }
    
    try:
        # Sending the GET request
        response = requests.get(base_url, params=params)
        
        # Raise an exception if the request returned an unsuccessful status code
        response.raise_for_status()
        
        # Parse the JSON response data
        data = response.json()
        
        # Extract and print specific weather attributes
        weather_desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        
        print(f"--- Weather in {city_name.title()} ---")
        print(f"Condition: {weather_desc.capitalize()}")
        print(f"Temperature: {temp}°C")
        print(f"Humidity: {humidity}%")
        print(f"Wind Speed: {wind_speed} m/s")
        
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            print("City not found. Please check the spelling.")
        elif response.status_code == 401:
            print("Invalid API Key. Please verify your OpenWeatherMap credentials.")
        else:
            print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

from dotenv import load_dotenv
import os

# Example Usage:
if __name__ == "__main__":
    # Replace with your actual free API key from your OpenWeatherMap dashboard
    load_dotenv()
    API_KEY = os.getenv("OPEN_WEATHER_API_KEY") 
    CITY = "London"
    print(API_KEY)
    get_weather(CITY, API_KEY)

