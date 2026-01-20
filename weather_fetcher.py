"""
Модуль для получения данных о погоде
Простые функции для работы с API Open-Meteo
"""
import requests
from datetime import datetime

# Адреса API
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def get_coordinates(city):
    """Найти координаты города"""
    try:
        # Ищем город через API
        response = requests.get(GEOCODING_URL, params={
            'name': city,
            'count': 1,
            'language': 'ru'
        })
        data = response.json()
        
        # Если город найден, возвращаем координаты
        if 'results' in data and len(data['results']) > 0:
            result = data['results'][0]
            lat = result['latitude']
            lon = result['longitude']
            name = result['name']
            return lat, lon, name
        else:
            return None
    except:
        print(f"Не удалось найти город: {city}")
        return None


def get_weather_description(code):
    """Перевести код погоды в понятное описание"""
    # Коды погоды от Open-Meteo
    weather_codes = {
        0: "ясно",
        1: "преимущественно ясно",
        2: "переменная облачность",
        3: "пасмурно",
        45: "туман",
        48: "туман с изморозью",
        51: "лёгкая морось",
        53: "морось",
        55: "сильная морось",
        61: "небольшой дождь",
        63: "дождь",
        65: "сильный дождь",
        71: "небольшой снег",
        73: "снег",
        75: "сильный снег",
        77: "снежная крупа",
        80: "небольшой ливень",
        81: "ливень",
        82: "сильный ливень",
        85: "слабый снегопад",
        86: "снегопад",
        95: "гроза",
        96: "гроза с градом",
        99: "сильная гроза с градом"
    }
    
    # Если код не найден, возвращаем "неизвестно"
    if code in weather_codes:
        return weather_codes[code]
    else:
        return "неизвестно"


def get_weather(city):
    """Получить погоду для города"""
    # Сначала находим координаты
    coords = get_coordinates(city)
    if not coords:
        return None
    
    lat, lon, city_name = coords
    
    # Запрашиваем погоду по координатам
    try:
        response = requests.get(WEATHER_URL, params={
            'latitude': lat,
            'longitude': lon,
            'current': 'temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,surface_pressure,wind_speed_10m,cloud_cover',
            'timezone': 'auto'
        })
        data = response.json()
        current = data['current']
        
        # Собираем все данные в один словарь
        weather_info = {
            'city': city_name,
            'country': 'RU',
            'temperature': round(current['temperature_2m'], 1),
            'feels_like': round(current['apparent_temperature'], 1),
            'temp_min': round(current['temperature_2m'] - 2, 1),
            'temp_max': round(current['temperature_2m'] + 2, 1),
            'pressure': round(current['surface_pressure'], 0),
            'humidity': current['relative_humidity_2m'],
            'description': get_weather_description(current['weather_code']),
            'wind_speed': round(current['wind_speed_10m'], 1),
            'clouds': current['cloud_cover'],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return weather_info
    except:
        print(f"Ошибка получения погоды для {city}")
        return None


def get_weather_for_cities(cities):
    """Получить погоду для списка городов"""
    all_weather = []
    
    # Проходим по каждому городу
    for city in cities:
        print(f"Получение данных для города: {city}...")
        weather = get_weather(city)
        
        # Если данные получены, добавляем в список
        if weather:
            all_weather.append(weather)
    
    return all_weather
