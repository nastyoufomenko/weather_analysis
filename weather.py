import asyncio
import logging
import io
import requests
import pandas as pd

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, BufferedInputFile

# --- КОНФИГУРАЦИЯ ---
BOT_TOKEN = "*"
WEATHER_API_KEY = "*"

# Координаты городов (чтобы не тратить лишние запросы на геокодинг)
CITIES = {
    "Москва": {"lat": 55.75, "lon": 37.61},
    "Санкт-Петербург": {"lat": 59.93, "lon": 30.33},
    "Новосибирск": {"lat": 55.00, "lon": 82.93},
    "Екатеринбург": {"lat": 56.84, "lon": 60.64},
    "Казань": {"lat": 55.79, "lon": 49.12}
}

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- ФУНКЦИИ ЛОГИКИ ---

def get_weather_data(lat, lon):
    """Получает прогноз погоды на 5 дней (шаг 3 часа)"""
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def generate_weather_plot(data, city_name):
    """Создает график температуры и возвращает объект байтов (картинку в памяти)"""
    
    # Парсим данные для Pandas
    timestamps = [item['dt'] for item in data['list']]
    temps = [item['main']['temp'] for item in data['list']]
    dates = [datetime.fromtimestamp(ts) for ts in timestamps]

    df = pd.DataFrame({'Date': dates, 'Temp': temps})

    # Настройка стиля графика
    plt.style.use('bmh') # Красивый встроенный стиль
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Построение линии
    ax.plot(df['Date'], df['Temp'], color='#1f77b4', linewidth=2, marker='o', markersize=4, label='Температура')
    
    # Заливка градиентом (или просто цветом) под графиком
    ax.fill_between(df['Date'], df['Temp'], color='#1f77b4', alpha=0.2)

    # Оформление осей
    ax.set_title(f"Прогноз температуры: {city_name}", fontsize=16, fontweight='bold', pad=20)
    ax.set_ylabel("Температура (°C)", fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Форматирование дат на оси X
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m %H:00'))
    plt.xticks(rotation=45)
    
    # Добавляем подписи значений (аннотации) для пиков
    max_temp = df['Temp'].max()
    max_date = df.loc[df['Temp'].idxmax(), 'Date']
    ax.annotate(f'Max: {max_temp}°', xy=(max_date, max_temp), xytext=(0, 10), 
                textcoords='offset points', ha='center', fontweight='bold', color='red')

    plt.tight_layout()

    # Сохраняем график в буфер памяти (не на диск)
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    buf.seek(0)
    plt.close(fig) # Обязательно закрываем фигуру, чтобы не забить память
    
    # Статистика для текста
    stats = {
        'min': df['Temp'].min(),
        'max': df['Temp'].max(),
        'avg': round(df['Temp'].mean(), 1)
    }
    
    return buf, stats

# --- ОБРАБОТЧИКИ (HANDLERS) ---

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Создаем клавиатуру с городами
    buttons = [[KeyboardButton(text=city)] for city in CITIES.keys()]
    # Разбиваем кнопки по 2 в ряд для красоты (кроме последней)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons[0] + buttons[1], buttons[2] + buttons[3], buttons[4]],
        resize_keyboard=True,
        input_field_placeholder="Выберите город..."
    )
    
    await message.answer(
        "👋 Привет! Я погодный бот-аналитик.\n"
        "Выберите город ниже, и я составлю график прогноза на 5 дней.",
        reply_markup=keyboard
    )

@dp.message(F.text.in_(CITIES.keys()))
async def city_weather(message: types.Message):
    city = message.text
    coords = CITIES[city]
    
    await message.answer(f"⏳ Собираю данные и рисую график для города {city}...")
    
    # Получаем данные
    weather_data = get_weather_data(coords['lat'], coords['lon'])
    
    if not weather_data:
        await message.answer("❌ Не удалось получить данные от погодного сервиса.")
        return

    # Генерируем график и статистику
    # Запускаем синхронную функцию в отдельном потоке, чтобы не блокировать бота
    photo_buffer, stats = await asyncio.to_thread(generate_weather_plot, weather_data, city)
    
    # Формируем красивую подпись
    caption = (
        f"📊 **Анализ погоды: {city}**\n\n"
        f"❄️ Мин. температура: {stats['min']}°C\n"
        f"🔥 Макс. температура: {stats['max']}°C\n"
        f"🌡 Средняя температура: {stats['avg']}°C\n\n"
        f"График прогноза на 5 дней прикреплен выше 👆"
    )

    # Отправляем фото
    file = BufferedInputFile(photo_buffer.read(), filename=f"weather_{city}.png")
    await message.answer_photo(photo=file, caption=caption, parse_mode="Markdown")

# --- ЗАПУСК ---

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")
