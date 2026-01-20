"""
Модуль для анализа погоды
Простые функции для работы с данными
"""
import pandas as pd


def get_statistics(weather_data):
    """Рассчитать статистику по погоде"""
    # Создаем таблицу из данных
    df = pd.DataFrame(weather_data)
    
    # Считаем средние значения
    stats = {
        'средняя_температура': round(df['temperature'].mean(), 2),
        'максимальная_температура': round(df['temperature'].max(), 2),
        'минимальная_температура': round(df['temperature'].min(), 2),
        'средняя_влажность': round(df['humidity'].mean(), 2),
        'средняя_скорость_ветра': round(df['wind_speed'].mean(), 2),
        'количество_городов': len(df)
    }
    
    return stats


def find_hottest_city(weather_data):
    """Найти самый теплый город"""
    df = pd.DataFrame(weather_data)
    # Находим индекс максимальной температуры
    idx = df['temperature'].idxmax()
    city = df.loc[idx]
    
    return {
        'город': city['city'],
        'температура': city['temperature'],
        'описание': city['description']
    }


def find_coldest_city(weather_data):
    """Найти самый холодный город"""
    df = pd.DataFrame(weather_data)
    # Находим индекс минимальной температуры
    idx = df['temperature'].idxmin()
    city = df.loc[idx]
    
    return {
        'город': city['city'],
        'температура': city['temperature'],
        'описание': city['description']
    }


def find_most_humid_city(weather_data):
    """Найти самый влажный город"""
    df = pd.DataFrame(weather_data)
    # Находим индекс максимальной влажности
    idx = df['humidity'].idxmax()
    city = df.loc[idx]
    
    return {
        'город': city['city'],
        'влажность': city['humidity'],
        'температура': city['temperature']
    }


def count_weather_conditions(weather_data):
    """Посчитать количество каждого типа погоды"""
    df = pd.DataFrame(weather_data)
    # Считаем сколько раз встречается каждое описание
    counts = df['description'].value_counts().to_dict()
    return counts


def save_to_csv(weather_data, filename='weather_data.csv'):
    """Сохранить данные в CSV файл"""
    df = pd.DataFrame(weather_data)
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"Данные сохранены в файл: {filename}")


def print_summary(weather_data):
    """Вывести красивую сводку по погоде"""
    print("\n" + "="*60)
    print("АНАЛИЗ ДАННЫХ О ПОГОДЕ")
    print("="*60)
    
    # Общая статистика
    stats = get_statistics(weather_data)
    print("\nОБЩАЯ СТАТИСТИКА:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Самый теплый город
    print("\nСАМЫЙ ТЁПЛЫЙ ГОРОД:")
    hottest = find_hottest_city(weather_data)
    print(f"  {hottest['город']}: {hottest['температура']}°C ({hottest['описание']})")
    
    # Самый холодный город
    print("\nСАМЫЙ ХОЛОДНЫЙ ГОРОД:")
    coldest = find_coldest_city(weather_data)
    print(f"  {coldest['город']}: {coldest['температура']}°C ({coldest['описание']})")
    
    # Самый влажный город
    print("\nСАМЫЙ ВЛАЖНЫЙ ГОРОД:")
    humid = find_most_humid_city(weather_data)
    print(f"  {humid['город']}: {humid['влажность']}% (температура: {humid['температура']}°C)")
    
    # Распределение погоды
    print("\nРАСПРЕДЕЛЕНИЕ ПОГОДНЫХ УСЛОВИЙ:")
    conditions = count_weather_conditions(weather_data)
    for condition, count in conditions.items():
        print(f"  {condition}: {count} город(ов)")
    
    print("="*60 + "\n")
