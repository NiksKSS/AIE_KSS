# Прогноз погоды по муниципалитетам Краснодарского края

Итоговый проект по курсу «Инженерия Искусственного Интеллекта». Проект решает задачу многовыходной регрессии: по дате, координатам и признакам муниципалитета предсказывает основные погодные параметры для Краснодарского края.

## Паспорт проекта

- **Автор:** Вероника Денисенко
- **Группа:** ИКБО-51-24
- **Контакт:** tg: @niks_kss
- **Домен:** табличные данные, прогнозирование погодных параметров
- **Основной сервис:** Streamlit-интерфейс с визуализацией на карте
- **Модель:** `ExtraTreesRegressor` в `sklearn.Pipeline`

## Структура проекта

```
project/
├── README.md                      # Этот файл — инструкция по запуску
├── report.md                      # Подробный отчёт о проекте
├── self-checklist.md              # Чеклист самопроверки (10/10)
├── requirements.txt               # Python-зависимости (14 пакетов)
├── Dockerfile                     # Контейнер для запуска Streamlit
│
├── data/                          # Данные
│   ├── data.csv                   # Основной датасет (~9.3 млн строк)
│   ├── sample_data.csv            # Пример структуры данных для Git
│   ├── preprocess_data.ipynb      # Ноутбук подготовки данных (EDA)
│   ├── Extended_climate_data.csv  # Исходные климатические данные
│   ├── Krasnodar_day_length_1995_2025.csv  # Длина светового дня
│   ├── Krasnodar_infrastructure_1995_2025.csv # Инфраструктура
│   ├── Krasnodar_Municipalities_GeoJson.txt # Границы муниципалитетов
│   ├── Krasnodar_Region_GeoJson.txt         # Граница региона
│   └── README.md                  # Описание данных
│
├── artifacts/                    # Артефакты модели
│   ├── model.pkl                 # Обученная модель (sklearn.Pipeline)
│   └── README.md                 # Описание артефактов
│
├── notebooks/                     # Ноутбуки экспериментов
│   ├── train_model.ipynb          # Обучение модели, подбор гиперпараметров, метрики
│   └── README.md                  # Описание экспериментов
│
├── src/                          # Исходный код
│   ├── __init__.py               # Пакет проекта
│   ├── config.py                 # Конфигурация: пути, переменные окружения
│   ├── streamlit_app.py          # Основной Streamlit-интерфейс
│   ├── models/                   # Модели и инференс
│   │   ├── __init__.py
│   │   └── predictor.py          # Загрузка модели, подготовка признаков
│   ├── service/                  # FastAPI-сервис (дополнительно)
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI-приложение
│   │   └── schemas.py           # Pydantic-схемы
│   └── README.md                 # Описание кода
│
├── configs/                      # Конфигурационные файлы
│   ├── .env.example             # Пример переменных окружения
│   ├── config.yaml              # Параметры сервиса и модели
│   └── README.md                # Описание конфигов
│
└── tests/                        # Тесты
    ├── test_api_contract.py     # Smoke-тесты API
    └── README.md                # Описание тестов
```

### Описание папок и файлов

#### data/ — данные проекта
- `data.csv` — основной датасет для обучения и инференса (9.3 млн строк, ~1.4 ГБ)
- `sample_data.csv` — маленький пример структуры для Git
- `preprocess_data.ipynb` — ноутбук с EDA и подготовкой данных
- `Extended_climate_data.csv` — расширенные климатические данные
- `Krasnodar_day_length_1995_2025.csv` — длина светового дня по дням
- `Krasnodar_infrastructure_1995_2025.csv` — географические признаки
- `Krasnodar_Municipalities_GeoJson.txt` — границы муниципалитетов для карты

#### artifacts/ — обученная модель
- `model.pkl` — финальная модель (sklearn.Pipeline с ExtraTreesRegressor, ~1.7 ГБ)

#### notebooks/ — эксперименты
- `train_model.ipynb` — обучение, валидация, подбор гиперпараметров, метрики

#### src/ — исходный код
- `config.py` — пути к данным/модели, переменные окружения, константы
- `streamlit_app.py` — основной Streamlit-интерфейс (выбор муниципалитета, дата, прогноз, карта)
- `models/predictor.py` — класс WeatherPredictor для загрузки модели и инференса
- `service/main.py` — FastAPI-приложение с endpoints /health, /regions, /metrics, /predict

#### configs/ — конфигурация
- `.env.example` — пример переменных окружения (без секретов)
- `config.yaml` — параметры модели и сервиса

#### tests/ — тесты
- `test_api_contract.py` — smoke-тесты для FastAPI endpoints

## Установка

Требуется Python 3.12 (версии 3.13+ не поддерживаются некоторыми зависимостями).

```bash
cd project
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Запуск (основной способ)

```bash
cd project
source .venv/bin/activate
PYTHONPATH=. streamlit run src/streamlit_app.py
```

После запуска откроется браузер (обычно http://localhost:8501).

### Возможности Streamlit-интерфейса

1. **Выбор муниципалитета** — выпадающий список всех районов Краснодарского края
2. **Выбор даты** — календарь для выбора даты прогноза
3. **Прогноз** — отображение предсказанных погодных параметров:
   - температура (средняя, максимальная, минимальная)
   - осадки
   - солнечная радиация
   - скорость и направление ветра
   - длина светового дня
4. **Карта** — визуализация прогноза на интерактивной карте муниципалитетов
5. **История** — просмотр исторических данных для выбранного района

## Запуск FastAPI (дополнительно)

```bash
cd project
source .venv/bin/activate
PYTHONPATH=. uvicorn src.service.main:app --host 0.0.0.0 --port 8000
```

## Запуск в Docker

```bash
cd project
docker build -t krasnodar-weather-app .
docker run --rm -p 8501:8501 krasnodar-weather-app
```

## Тесты

```bash
cd project
source .venv/bin/activate
PYTHONPATH=. pytest tests/ -v
```

## Данные

Проект использует табличные погодные данные по точкам Краснодарского края за 1995–2025 годы. Ключевые признаки модели:

- координаты: `lat`, `lon`
- календарные признаки: `month`, `day`, `dayofyear`
- географические признаки: `sea_border`, `mountain_border`
- административный центр: `admin_center`

Целевые переменные (8 штук):

- `precipitation`, `temp`, `tmax`, `tmin`
- `solar_radiation`, `wind_speed`, `wind_direction`, `day_length_hours`

Большие файлы (`data/data.csv`, `artifacts/model.pkl`) добавлены в `.gitignore`. Для запуска проекта они должны быть доступны локально.

## Ограничения модели

Модель хорошо предсказывает температуру, длину светового дня и солнечную радиацию (R² > 0.7). Хуже справляется с осадками и направлением ветра — это ожидаемо из-за высокой локальной изменчивости этих параметров.

## Демонстрация на защите

1. Установить зависимости: `pip install -r requirements.txt` (с Python 3.12)
2. Запустить: `PYTHONPATH=. streamlit run src/streamlit_app.py`
3. Показать выбор муниципалитета и даты
4. Показать прогноз погодных параметров
5. Показать карту с визуализацией
6. При необходимости — открыть `notebooks/train_model.ipynb` и показать метрики модели