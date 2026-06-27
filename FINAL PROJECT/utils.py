import requests #type:ignore
from config import WEATHER_API_KEY, JOKE_URL

class WeatherService:
    """Handles weather-related API calls"""
    
    def __init__(self):
        self.api_key = WEATHER_API_KEY
        self.url = "https://api.openweathermap.org/data/2.5/weather"
    
    def get_weather(self, city):
        """Get weather data for a city"""
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'
        }
        try:
            response = requests.get(self.url, params=params, timeout=10)
            data = response.json()
            
            if response.status_code == 200:
                main = data['main']
                weather = data['weather'][0]
                wind = data['wind']
                
                return {
                    'city': city,
                    'temperature': main['temp'],
                    'feels_like': main['feels_like'],
                    'humidity': main['humidity'],
                    'pressure': main['pressure'],
                    'description': weather['description'],
                    'wind_speed': wind.get('speed', 'N/A')
                }
            else:
                return {'error': data.get('message', 'City not found')}
        except Exception as e:
            return {'error': f"Could not fetch weather: {str(e)}"}

class JokeService:
    """Handles joke-related API calls"""
    
    def __init__(self):
        self.url = JOKE_URL
    
    def get_joke(self):
        """Fetch a random joke"""
        try:
            response = requests.get(self.url, timeout=10)
            data = response.json()
            
            if data.get('error'):
                return {'error': 'Failed to fetch joke'}
            
            if data['type'] == 'single':
                joke_text = data['joke']
            else:
                joke_text = f"{data['setup']}\n{data['delivery']}"
            
            return {
                'joke': joke_text,
                'category': data.get('category', 'Unknown')
            }
        except Exception as e:
            return {'error': f"Could not fetch joke: {str(e)}"}

def format_weather_message(weather_data):
    """Format weather data into a readable message"""
    if 'error' in weather_data:
        return f"❌ {weather_data['error']}"
    
    return (
        f"🌤️ Weather in {weather_data['city']}\n"
        f"├ Temperature: {weather_data['temperature']:.1f}°C\n"
        f"├ Feels like: {weather_data['feels_like']:.1f}°C\n"
        f"├ Humidity: {weather_data['humidity']}%\n"
        f"├ Pressure: {weather_data['pressure']} hPa\n"
        f"├ Description: {weather_data['description'].capitalize()}\n"
        f"└ Wind speed: {weather_data['wind_speed']} m/s"
    )

def format_todo_message(todos):
    """Format todo list into a readable message"""
    if not todos:
        return "✅ No pending tasks! Great job!"
    
    message = "📋 Your todo list:\n"
    for idx, (todo_id, task, created_at) in enumerate(todos, 1):
        date = created_at[:10] if created_at else "Unknown"
        message += f"{idx}. {task} (added {date})\n"
    
    return message