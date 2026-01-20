"""
Модуль для создания графиков
Простые функции для визуализации данных
"""
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Настройка стиля графиков
sns.set_style("whitegrid")


def plot_temperature(weather_data):
    """Нарисовать график температур"""
    # Создаем таблицу из данных
    df = pd.DataFrame(weather_data)
    
    # Создаем график
    plt.figure(figsize=(14, 6))
    
    cities = df['city']
    x = range(len(cities))
    
    # Рисуем столбцы с температурой
    bars = plt.bar(x, df['temperature'], color='skyblue', edgecolor='navy', alpha=0.7, label='Температура')
    
    # Добавляем линию "ощущается как"
    plt.plot(x, df['feels_like'], color='red', marker='o', linewidth=2, markersize=6, label='Ощущается как')
    
    plt.xlabel('Города', fontsize=12, fontweight='bold')
    plt.ylabel('Температура (°C)', fontsize=12, fontweight='bold')
    plt.title('Сравнение температур по городам', fontsize=14, fontweight='bold')
    plt.xticks(x, cities, rotation=45, ha='right')
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    
    # Подписываем значения на столбцах
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{df["temperature"].iloc[i]:.1f}°C',
                ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('temperature_comparison.png', dpi=300, bbox_inches='tight')
    print("График сохранён: temperature_comparison.png")
    plt.close()


def plot_humidity_and_wind(weather_data):
    """Нарисовать графики влажности и ветра"""
    # Создаем таблицу из данных
    df = pd.DataFrame(weather_data)
    
    # Создаем два графика рядом
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    cities = df['city']
    x = range(len(cities))
    
    # ГРАФИК 1: Влажность
    colors1 = plt.cm.Blues(df['humidity'] / 100)
    bars1 = ax1.bar(x, df['humidity'], color=colors1, edgecolor='navy', alpha=0.7)
    ax1.set_xlabel('Города', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Влажность (%)', fontsize=12, fontweight='bold')
    ax1.set_title('Влажность по городам', fontsize=14, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(cities, rotation=45, ha='right')
    ax1.set_ylim(0, 110)
    ax1.grid(axis='y', alpha=0.3)
    
    # Подписываем значения
    for i, bar in enumerate(bars1):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{df["humidity"].iloc[i]}%',
                ha='center', va='bottom', fontsize=9)
    
    # ГРАФИК 2: Скорость ветра
    colors2 = plt.cm.Greens(df['wind_speed'] / df['wind_speed'].max())
    bars2 = ax2.bar(x, df['wind_speed'], color=colors2, edgecolor='darkgreen', alpha=0.7)
    ax2.set_xlabel('Города', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Скорость ветра (м/с)', fontsize=12, fontweight='bold')
    ax2.set_title('Скорость ветра по городам', fontsize=14, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(cities, rotation=45, ha='right')
    ax2.grid(axis='y', alpha=0.3)
    
    # Подписываем значения
    for i, bar in enumerate(bars2):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{df["wind_speed"].iloc[i]:.1f}',
                ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('humidity_wind.png', dpi=300, bbox_inches='tight')
    print("График сохранён: humidity_wind.png")
    plt.close()


def plot_weather_pie(weather_data):
    """Нарисовать круговую диаграмму погоды"""
    # Создаем таблицу из данных
    df = pd.DataFrame(weather_data)
    
    # Создаем график
    plt.figure(figsize=(10, 8))
    
    # Считаем количество каждого типа погоды
    conditions = df['description'].value_counts()
    
    # Рисуем круговую диаграмму
    colors = plt.cm.Set3(range(len(conditions)))
    wedges, texts, autotexts = plt.pie(conditions.values,
                                        labels=conditions.index,
                                        autopct='%1.1f%%',
                                        colors=colors,
                                        startangle=90,
                                        textprops={'fontsize': 11})
    
    # Делаем проценты белыми и жирными
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    plt.title('Распределение погодных условий', fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig('weather_conditions.png', dpi=300, bbox_inches='tight')
    print("График сохранён: weather_conditions.png")
    plt.close()


def create_all_plots(weather_data):
    """Создать все графики"""
    print("\nСоздание визуализаций...")
    plot_temperature(weather_data)
    plot_humidity_and_wind(weather_data)
    plot_weather_pie(weather_data)
    print("Все графики успешно созданы!\n")
