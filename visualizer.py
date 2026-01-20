"""
Модуль для визуализации данных о погоде
"""
import matplotlib.pyplot as plt
import pandas as pd
from typing import List, Dict
import seaborn as sns


class WeatherVisualizer:
    """Класс для создания визуализаций данных о погоде"""
    
    def __init__(self, weather_data: List[Dict]):
        """
        Инициализация визуализатора
        
        Args:
            weather_data: Список словарей с данными о погоде
        """
        self.df = pd.DataFrame(weather_data)
        # Настройка стиля графиков
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 10
        
    def plot_temperature_comparison(self, save_path: str = 'temperature_comparison.png'):
        """
        Создать график сравнения температур по городам
        
        Args:
            save_path: Путь для сохранения графика
        """
        fig, ax = plt.subplots(figsize=(14, 6))
        
        cities = self.df['city']
        x_pos = range(len(cities))
        
        # Столбцы для температуры
        bars = ax.bar(x_pos, self.df['temperature'], color='skyblue', 
                     edgecolor='navy', alpha=0.7, label='Текущая температура')
        
        # Линия для ощущаемой температуры
        ax.plot(x_pos, self.df['feels_like'], color='red', marker='o', 
               linewidth=2, markersize=6, label='Ощущается как')
        
        ax.set_xlabel('Города', fontsize=12, fontweight='bold')
        ax.set_ylabel('Температура (°C)', fontsize=12, fontweight='bold')
        ax.set_title('Сравнение температур по городам', fontsize=14, fontweight='bold')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(cities, rotation=45, ha='right')
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        # Добавляем значения на столбцы
        for i, (bar, temp) in enumerate(zip(bars, self.df['temperature'])):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{temp:.1f}°C', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"График сохранён: {save_path}")
        plt.close()
    
    def plot_humidity_wind(self, save_path: str = 'humidity_wind.png'):
        """
        Создать график влажности и скорости ветра
        
        Args:
            save_path: Путь для сохранения графика
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # График влажности
        colors = plt.cm.Blues(self.df['humidity'] / 100)
        bars1 = ax1.bar(range(len(self.df)), self.df['humidity'], 
                       color=colors, edgecolor='navy', alpha=0.7)
        ax1.set_xlabel('Города', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Влажность (%)', fontsize=12, fontweight='bold')
        ax1.set_title('Влажность по городам', fontsize=14, fontweight='bold')
        ax1.set_xticks(range(len(self.df)))
        ax1.set_xticklabels(self.df['city'], rotation=45, ha='right')
        ax1.set_ylim(0, 110)
        ax1.grid(axis='y', alpha=0.3)
        
        # Добавляем значения
        for bar, humidity in zip(bars1, self.df['humidity']):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{humidity}%', ha='center', va='bottom', fontsize=9)
        
        # График скорости ветра
        colors2 = plt.cm.Greens(self.df['wind_speed'] / self.df['wind_speed'].max())
        bars2 = ax2.bar(range(len(self.df)), self.df['wind_speed'], 
                       color=colors2, edgecolor='darkgreen', alpha=0.7)
        ax2.set_xlabel('Города', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Скорость ветра (м/с)', fontsize=12, fontweight='bold')
        ax2.set_title('Скорость ветра по городам', fontsize=14, fontweight='bold')
        ax2.set_xticks(range(len(self.df)))
        ax2.set_xticklabels(self.df['city'], rotation=45, ha='right')
        ax2.grid(axis='y', alpha=0.3)
        
        # Добавляем значения
        for bar, wind in zip(bars2, self.df['wind_speed']):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{wind:.1f}', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"График сохранён: {save_path}")
        plt.close()
    
    def plot_weather_conditions_pie(self, save_path: str = 'weather_conditions.png'):
        """
        Создать круговую диаграмму погодных условий
        
        Args:
            save_path: Путь для сохранения графика
        """
        fig, ax = plt.subplots(figsize=(10, 8))
        
        conditions = self.df['description'].value_counts()
        
        colors = plt.cm.Set3(range(len(conditions)))
        wedges, texts, autotexts = ax.pie(conditions.values, 
                                           labels=conditions.index,
                                           autopct='%1.1f%%',
                                           colors=colors,
                                           startangle=90,
                                           textprops={'fontsize': 11})
        
        # Улучшаем читаемость
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        ax.set_title('Распределение погодных условий', 
                    fontsize=14, fontweight='bold', pad=20)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"График сохранён: {save_path}")
        plt.close()
    
    def plot_all(self):
        """Создать все графики"""
        print("\nСоздание визуализаций...")
        self.plot_temperature_comparison()
        self.plot_humidity_wind()
        self.plot_weather_conditions_pie()
        print("Все графики успешно созданы!\n")
