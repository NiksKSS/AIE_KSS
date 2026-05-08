from pathlib import Path
import os

# Корневая директория проекта
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Загрузка переменных окружения из .env файла (если доступен)
try:
    from dotenv import load_dotenv
    load_dotenv(PROJECT_ROOT / "configs" / ".env")
except ImportError:
    pass

# Пути к данным, модели и GeoJSON-файлам
DATA_PATH = Path(os.getenv("WEATHER_DATA_PATH", PROJECT_ROOT / "data" / "data.csv"))
MODEL_PATH = Path(os.getenv("WEATHER_MODEL_PATH", PROJECT_ROOT / "artifacts" / "model.pkl"))
GEOJSON_PATH = Path(
    os.getenv(
        "WEATHER_GEOJSON_PATH",
        PROJECT_ROOT / "data" / "Krasnodar_Municipalities_GeoJson.txt",
    )
)

# Уровень логирования для приложения
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Целевые переменные для предсказания
TARGET_VARS = [
    "precipitation",
    "temp",
    "tmax",
    "tmin",
    "solar_radiation",
    "wind_speed",
    "wind_direction",
    "day_length_hours",
]

# Единицы измерения для каждой целевой переменной
TARGET_UNITS = {
    "precipitation": "мм",
    "temp": "°C",
    "tmax": "°C",
    "tmin": "°C",
    "solar_radiation": "Вт/м²",
    "wind_speed": "м/с",
    "wind_direction": "градусы",
    "day_length_hours": "ч",
}

# Признаки, используемые для обучения и предсказания
FEATURE_COLUMNS = [
    "lat",
    "lon",
    "month",
    "day",
    "dayofyear",
    "sea_border",
    "mountain_border",
    "admin_center",
]