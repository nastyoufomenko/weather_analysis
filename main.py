"""
Главный модуль приложения для анализа погоды
Демонстрационный проект по работе с данными
Использует Open-Meteo API - бесплатный API без регистрации
"""
import weather_fetcher
import data_analyzer
import visualizer


def main():
    """Главная функция"""
    
    print("="*60)
    print("АНАЛИЗ ПОГОДЫ В РОССИЙСКИХ ГОРОДАХ")
    print("="*60)
    print("\n✅ Используется Open-Meteo API - бесплатный, без регистрации!")
    print("📡 Источник: https://open-meteo.com\n")
    
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
    
    # ШАГ 1: Получаем данные о погоде
    print("ШАГ 1: Получение данных через API...")
    print("-" * 60)
    weather_data = weather_fetcher.get_weather_for_cities(cities)
    
    if not weather_data:
        print("\n❌ Не удалось получить данные о погоде.")
        return
    
    print(f"\n✓ Получено данных для {len(weather_data)} городов\n")
    
    # ШАГ 2: Анализируем данные
    print("ШАГ 2: Анализ полученных данных...")
    print("-" * 60)
    data_analyzer.print_summary(weather_data)
    data_analyzer.save_to_csv(weather_data)
    
    # ШАГ 3: Создаем графики
    print("ШАГ 3: Создание визуализаций...")
    print("-" * 60)
    visualizer.create_all_plots(weather_data)
    
    # Итоги
    print("="*60)
    print("АНАЛИЗ ЗАВЕРШЁН!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
