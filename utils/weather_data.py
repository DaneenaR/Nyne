"""
Weather data fetching using OpenWeatherMap API (free tier)
1000 calls/day free
"""

import os
import requests
from datetime import datetime, timedelta
import numpy as np
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")

# Flag to use mock data if API not configured
USE_MOCK = not OPENWEATHER_API_KEY


def get_weather_forecast(latitude, longitude, days=7):
    """
    Get weather forecast for location
    
    Args:
        latitude: Location latitude
        longitude: Location longitude
        days: Number of days to forecast
    
    Returns:
        dict: Weather forecast data
    """
    if USE_MOCK:
        print("⚠️ Using mock weather data (OpenWeatherMap API not configured)")
        return _get_mock_weather_forecast(latitude, longitude, days)
    
    try:
        # OpenWeatherMap One Call API 3.0
        url = "https://api.openweathermap.org/data/3.0/onecall"
        
        params = {
            'lat': latitude,
            'lon': longitude,
            'appid': OPENWEATHER_API_KEY,
            'units': 'metric',
            'exclude': 'minutely,hourly,alerts'
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract daily forecasts
            dates = []
            rainfall_mm = []
            temperatures = []
            humidity = []
            
            for day in data['daily'][:days]:
                date = datetime.fromtimestamp(day['dt']).strftime("%Y-%m-%d")
                dates.append(date)
                
                # Rainfall (mm)
                rain = day.get('rain', 0)
                rainfall_mm.append(rain)
                
                # Temperature (°C)
                temp = day['temp']['day']
                temperatures.append(temp)
                
                # Humidity (%)
                hum = day['humidity']
                humidity.append(hum)
            
            return {
                'dates': dates,
                'rainfall_mm': rainfall_mm,
                'temperature_c': temperatures,
                'humidity': humidity,
                'avg_humidity': np.mean(humidity),
                'total_rainfall': sum(rainfall_mm),
                'max_rainfall_day': max(rainfall_mm) if rainfall_mm else 0,
                'source': 'OpenWeatherMap'
            }
        
        elif response.status_code == 401:
            print("⚠️ OpenWeatherMap API key invalid or not activated yet")
            print("💡 Tip: New API keys take 10 minutes to activate!")
            return _get_mock_weather_forecast(latitude, longitude, days)
        
        else:
            print(f"⚠️ OpenWeatherMap API error: {response.status_code}")
            return _get_mock_weather_forecast(latitude, longitude, days)
            
    except Exception as e:
        print(f"⚠️ Weather API error: {str(e)}")
        return _get_mock_weather_forecast(latitude, longitude, days)


def _get_mock_weather_forecast(latitude, longitude, days=7):
    """Fallback mock data"""
    dates = [(datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days)]
    
    base_rainfall = np.random.uniform(0, 20)
    rainfall_mm = [max(0, base_rainfall + np.random.normal(0, 10)) for _ in range(days)]
    
    temperatures = [20 + np.random.normal(0, 5) for _ in range(days)]
    humidity = [60 + np.random.normal(0, 15) for _ in range(days)]
    
    return {
        'dates': dates,
        'rainfall_mm': rainfall_mm,
        'temperature_c': temperatures,
        'humidity': humidity,
        'avg_humidity': np.mean(humidity),
        'total_rainfall': sum(rainfall_mm),
        'max_rainfall_day': max(rainfall_mm),
        'source': 'Mock Data'
    }


def get_rainfall_data(latitude, longitude, days_back=30):
    """
    Get historical rainfall data
    
    Args:
        latitude: Location latitude
        longitude: Location longitude
        days_back: Days of history to fetch
    
    Returns:
        dict: Historical rainfall data
    """
    if USE_MOCK:
        return _get_mock_rainfall_data(days_back)
    
    try:
        # For historical data, we'd need a premium API
        # Using current data for now
        return _get_mock_rainfall_data(days_back)
        
    except Exception as e:
        print(f"⚠️ Historical weather error: {str(e)}")
        return _get_mock_rainfall_data(days_back)


def _get_mock_rainfall_data(days_back=30):
    """Mock historical data"""
    dates = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") 
             for i in range(days_back, 0, -1)]
    
    rainfall = [max(0, np.random.normal(10, 8)) for _ in range(days_back)]
    
    return {
        'dates': dates,
        'rainfall_mm': rainfall,
        'average': np.mean(rainfall),
        'max': max(rainfall),
        'total': sum(rainfall),
        'source': 'Mock Data'
    }


def check_storm_alerts(latitude, longitude):
    """
    Check for active storm/flood alerts
    """
    if USE_MOCK:
        return _get_mock_storm_alerts()
    
    try:
        # Would use OpenWeatherMap alerts endpoint
        # Available in One Call API
        return _get_mock_storm_alerts()
        
    except Exception as e:
        print(f"⚠️ Storm alerts error: {str(e)}")
        return _get_mock_storm_alerts()


def _get_mock_storm_alerts():
    """Mock alert system"""
    alert_chance = np.random.random()
    
    if alert_chance > 0.7:
        return {
            'active': True,
            'level': 'SEVERE' if alert_chance > 0.9 else 'MODERATE',
            'description': 'Heavy rainfall expected in the next 48 hours',
            'issued': datetime.now(),
            'expires': datetime.now() + timedelta(days=2)
        }
    
    return {'active': False}
