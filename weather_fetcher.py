"""
Модуль для получения данных о погоде через API OpenWeatherMap
"""
import requests
import json
from datetime import datetime
from typing import Dict, List, Optional


class WeatherFetcher:
    """Класс для получения данных о погоде"""
    
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
    
    def __init__(self, api_key: str):
        """
        Инициализация класса
        
        Args:
            api_key: API ключ для OpenWeatherMap
        """
        self.api_key = api_key
        
    def get_weather(self, city: str, country_code: str = "RU") -> Optional[Dict]:
        """
        Получить данные о погоде для указанного города
        
        Args:
            city: Название города
            country_code: Код страны (по умолчанию RU)
            
        Returns:
            Словарь с данными о погоде или None при ошибке
        """
        try:
            params = {
                'q': f'{city},{country_code}',
                'appid': self.api_key,
                'units': 'metric',  # Температура в градусах Цельсия
                'lang': 'ru'
            }
            
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # Форматируем данные
            weather_data = {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'temp_min': data['main']['temp_min'],
                'temp_max': data['main']['temp_max'],
                'pressure': data['main']['pressure'],
                'humidity': data['main']['humidity'],
                'description': data['weather'][0]['description'],
                'wind_speed': data['wind']['speed'],
                'clouds': data['clouds']['all'],
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return weather_data
            
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе данных для {city}: {e}")
            return None
        except KeyError as e:
            print(f"Ошибка обработки данных для {city}: {e}")
            return None
    
    def get_multiple_cities(self, cities: List[str], country_code: str = "RU") -> List[Dict]:
        """
        Получить данные о погоде для нескольких городов
        
        Args:
            cities: Список названий городов
            country_code: Код страны
            
        Returns:
            Список словарей с данными о погоде
        """
        results = []
        
        for city in cities:
            print(f"Получение данных для города: {city}...")
            weather = self.get_weather(city, country_code)
            if weather:
                results.append(weather)
                
        return results
