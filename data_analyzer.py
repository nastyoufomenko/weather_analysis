"""
Модуль для анализа данных о погоде
"""
import pandas as pd
from typing import List, Dict
import json


class WeatherAnalyzer:
    """Класс для анализа данных о погоде"""
    
    def __init__(self, weather_data: List[Dict]):
        """
        Инициализация анализатора
        
        Args:
            weather_data: Список словарей с данными о погоде
        """
        self.df = pd.DataFrame(weather_data)
        
    def get_basic_statistics(self) -> Dict:
        """
        Получить базовую статистику по температуре
        
        Returns:
            Словарь со статистическими показателями
        """
        stats = {
            'средняя_температура': round(self.df['temperature'].mean(), 2),
            'максимальная_температура': round(self.df['temperature'].max(), 2),
            'минимальная_температура': round(self.df['temperature'].min(), 2),
            'средняя_влажность': round(self.df['humidity'].mean(), 2),
            'средняя_скорость_ветра': round(self.df['wind_speed'].mean(), 2),
            'количество_городов': len(self.df)
        }
        
        return stats
    
    def get_hottest_city(self) -> Dict:
        """Найти самый тёплый город"""
        idx = self.df['temperature'].idxmax()
        city_data = self.df.loc[idx]
        return {
            'город': city_data['city'],
            'температура': city_data['temperature'],
            'описание': city_data['description']
        }
    
    def get_coldest_city(self) -> Dict:
        """Найти самый холодный город"""
        idx = self.df['temperature'].idxmin()
        city_data = self.df.loc[idx]
        return {
            'город': city_data['city'],
            'температура': city_data['temperature'],
            'описание': city_data['description']
        }
    
    def get_most_humid_city(self) -> Dict:
        """Найти самый влажный город"""
        idx = self.df['humidity'].idxmax()
        city_data = self.df.loc[idx]
        return {
            'город': city_data['city'],
            'влажность': city_data['humidity'],
            'температура': city_data['temperature']
        }
    
    def get_weather_conditions_summary(self) -> Dict:
        """
        Получить сводку по погодным условиям
        
        Returns:
            Словарь с количеством городов для каждого типа погоды
        """
        return self.df['description'].value_counts().to_dict()
    
    def save_to_csv(self, filename: str = 'weather_data.csv'):
        """
        Сохранить данные в CSV файл
        
        Args:
            filename: Имя файла для сохранения
        """
        self.df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"Данные сохранены в файл: {filename}")
    
    def print_summary(self):
        """Вывести краткую сводку по данным"""
        print("\n" + "="*60)
        print("АНАЛИЗ ДАННЫХ О ПОГОДЕ")
        print("="*60)
        
        stats = self.get_basic_statistics()
        print("\nОБЩАЯ СТАТИСТИКА:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        print("\nСАМЫЙ ТЁПЛЫЙ ГОРОД:")
        hottest = self.get_hottest_city()
        print(f"  {hottest['город']}: {hottest['температура']}°C ({hottest['описание']})")
        
        print("\nСАМЫЙ ХОЛОДНЫЙ ГОРОД:")
        coldest = self.get_coldest_city()
        print(f"  {coldest['город']}: {coldest['температура']}°C ({coldest['описание']})")
        
        print("\nСАМЫЙ ВЛАЖНЫЙ ГОРОД:")
        humid = self.get_most_humid_city()
        print(f"  {humid['город']}: {humid['влажность']}% (температура: {humid['температура']}°C)")
        
        print("\nРАСПРЕДЕЛЕНИЕ ПОГОДНЫХ УСЛОВИЙ:")
        conditions = self.get_weather_conditions_summary()
        for condition, count in conditions.items():
            print(f"  {condition}: {count} город(ов)")
        
        print("="*60 + "\n")
