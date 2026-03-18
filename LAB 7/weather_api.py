import requests # type: ignore
import json
from datetime import datetime

API_KEY = 'ab9aba11ec84a952ef4786cb5ab81709'
URL = 'https://api.openweathermap.org/data/2.5/weather'

class WeatherAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.params = {
            'appid': self.api_key,
            'units': 'metric'
        }
        self.city = ''
    
    def set_city(self, city_name):
        self.city = city_name
        print(f"City set to: {city_name}")
    
    def fetch_weather(self):
        self.params['q'] = self.city
        try:
            response = requests.get(URL, params=self.params, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: {response.json().get('message', 'Unknown error')}")
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def display(self, data):
        if not data:
            return
        
        print("\n")
        print(f"WEATHER IN {self.city.upper()}")
        print("\n")
        
        main = data.get('main', {})
        weather = data.get('weather', [{}])[0]
        wind = data.get('wind', {})
        sys = data.get('sys', {})
        
        print(f"Temperature: {main.get('temp', 'N/A')}°C")
        print(f"Feels like: {main.get('feels_like', 'N/A')}°C")
        print(f"Humidity: {main.get('humidity', 'N/A')}%")
        print(f"Pressure: {main.get('pressure', 'N/A')} hPa")
        print(f"Description: {weather.get('description', 'N/A').capitalize()}")
        print(f"Wind speed: {wind.get('speed', 'N/A')} m/s")
        
        if sys.get('country'):
            print(f"Country: {sys.get('country')}")
        
        print("\n")

if __name__ == '__main__':
    api = WeatherAPI(API_KEY)
    
    city = input("Enter city name: ").strip()
    api.set_city(city)
    
    print("Fetching weather data...")
    result = api.fetch_weather()
    
    if result:
        api.display(result)
        
        filename = f'weather_{city}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2)
        print(f"Saved to {filename}")