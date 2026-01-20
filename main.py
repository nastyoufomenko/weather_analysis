"""
Главный модуль приложения для анализа погоды
Демонстрационный проект по работе с данными
"""
import os
from weather_fetcher import WeatherFetcher
from data_analyzer import WeatherAnalyzer
from visualizer import WeatherVisualizer


def main():
    """Основная функция приложения"""
    
    print("="*60)
    print("АНАЛИЗ ПОГОДЫ В РОССИЙСКИХ ГОРОДАХ")
    print("="*60)
    
    # API ключ (можно получить бесплатно на openweathermap.org)
    # Для демонстрации используется переменная окружения
    api_key = os.getenv('OPENWEATHER_API_KEY', 'YOUR_API_KEY_HERE')
    
    if api_key == 'YOUR_API_KEY_HERE':
        print("\n⚠ ВНИМАНИЕ: Необходимо установить API ключ!")
        print("1. Зарегистрируйтесь на https://openweathermap.org/api")
        print("2. Получите бесплатный API ключ")
        print("3. Установите переменную окружения:")
        print("   set OPENWEATHER_API_KEY=your_api_key")
        print("\nИли измените строку api_key в файле main.py\n")
        return
    
    # Список городов для анализа
    cities = [
        'Moscow',
        'Saint Petersburg',
        'Novosibirsk',
        'Yekaterinburg',
        'Kazan',
        'Nizhny Novgorod',
        'Chelyabinsk',
        'Samara',
        'Omsk',
        'Rostov-on-Don',
        'Ufa',
        'Krasnoyarsk',
        'Vladivostok',
        'Sochi',
        'Murmansk'
    ]
    
    print(f"\nАнализируем погоду в {len(cities)} городах России...\n")
    
    # Шаг 1: Получение данных
    print("ШАГ 1: Получение данных через API...")
    print("-" * 60)
    fetcher = WeatherFetcher(api_key)
    weather_data = fetcher.get_multiple_cities(cities)
    
    if not weather_data:
        print("\n❌ Не удалось получить данные о погоде.")
        print("Проверьте API ключ и подключение к интернету.")
        return
    
    print(f"\n✓ Получено данных для {len(weather_data)} городов\n")
    
    # Шаг 2: Анализ данных
    print("ШАГ 2: Анализ полученных данных...")
    print("-" * 60)
    analyzer = WeatherAnalyzer(weather_data)
    
    # Вывод статистики
    analyzer.print_summary()
    
    # Сохранение в CSV
    analyzer.save_to_csv('weather_data.csv')
    
    # Шаг 3: Визуализация
    print("\nШАГ 3: Создание визуализаций...")
    print("-" * 60)
    visualizer = WeatherVisualizer(weather_data)
    visualizer.plot_all()
    
    # Итоги
    print("="*60)
    print("АНАЛИЗ ЗАВЕРШЁН!")
    print("="*60)
    print("\nСозданные файлы:")
    print("  📊 weather_data.csv - данные в формате CSV")
    print("  📈 temperature_comparison.png - сравнение температур")
    print("  📈 humidity_wind.png - влажность и скорость ветра")
    print("  📈 weather_conditions.png - распределение погодных условий")
    print("\nПроект демонстрирует:")
    print("  ✓ Работу с API (OpenWeatherMap)")
    print("  ✓ Обработку данных с pandas")
    print("  ✓ Статистический анализ")
    print("  ✓ Визуализацию данных (matplotlib, seaborn)")
    print("  ✓ Экспорт данных в CSV")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
