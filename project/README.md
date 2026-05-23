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
├── requirements.txt               # Python-зависимости (15 пакетов)
├── Dockerfile                     # Контейнер для запуска Streamlit
│
├── data/                          # Данные
│   ├── data.csv                   # ⚠ Основной датасет (~9.3 млн строк, 1.3 ГБ) — не в Git
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
│   ├── model.pkl                 # ⚠ Обученная модель (sklearn.Pipeline, 1.6 ГБ) — не в Git
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
    ├── test_api_contract.py     # Smoke-тесты API (требуют model.pkl)
    └── README.md                # Описание тестов
```

### Описание папок и файлов

#### data/ — данные проекта
- `data.csv` — основной датасет для обучения и инференса (9.3 млн строк, ~1.3 ГБ). **Не хранится в Git** из-за размера.
- `sample_data.csv` — маленький пример структуры (5 строк) для Git. Показывает формат всех колонок.
- `preprocess_data.ipynb` — ноутбук с EDA и подготовкой данных. Объединяет исходные CSV, GeoJSON и внешние признаки в `data.csv`.
- `Extended_climate_data.csv` — расширенные климатические данные (исходный источник).
- `Krasnodar_day_length_1995_2025.csv` — длина светового дня по дням (внешний признак).
- `Krasnodar_infrastructure_1995_2025.csv` — географические признаки (внешний признак).
- `Krasnodar_Municipalities_GeoJson.txt` — границы муниципалитетов для карты.
- `Krasnodar_Region_GeoJson.txt` — граница региона для карты.

#### artifacts/ — обученная модель
- `model.pkl` — финальная модель (sklearn.Pipeline с ExtraTreesRegressor, ~1.6 ГБ). **Не хранится в Git** из-за размера.

#### notebooks/ — эксперименты
- `train_model.ipynb` — обучение, валидация, подбор гиперпараметров, метрики.

#### src/ — исходный код
- `config.py` — пути к данным/модели, переменные окружения, константы.
- `streamlit_app.py` — основной Streamlit-интерфейс (выбор муниципалитета, дата, прогноз, карта).
- `models/predictor.py` — класс WeatherPredictor для загрузки модели и инференса.
- `service/main.py` — FastAPI-приложение с endpoints /health, /regions, /metrics, /predict.

#### configs/ — конфигурация
- `.env.example` — пример переменных окружения (без секретов).
- `config.yaml` — параметры модели и сервиса.

#### tests/ — тесты
- `test_api_contract.py` — smoke-тесты для FastAPI endpoints.

---

## Установка

Требуется Python 3.12 (версии 3.13+ не поддерживаются некоторыми зависимостями).

```bash
cd project
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Получение данных и модели

> **Важно:** Файлы `data/data.csv` (1.3 ГБ) и `artifacts/model.pkl` (1.6 ГБ) слишком велики для Git и не хранятся в репозитории. Без них приложение не запустится.

Есть два способа их получить.

---

### Вариант A: скачать готовые артефакты (рекомендуется)

Скачайте оба файла с Google Drive и положите в соответствующие папки.

#### 1. Скачайте data.csv (1.3 ГБ)

```bash
# Из папки project/:
curl -L -o data/data.csv "https://drive.usercontent.google.com/download?id=1TAgdDTo0NvoMHespNDOHsrqmEfCNxaKL&export=download&confirm=t"
```

**Ожидаемый результат:** файл `project/data/data.csv` размером ~1.3 ГБ.

#### 2. Скачайте model.pkl (1.6 ГБ)

```bash
# Из папки project/:
curl -L -o artifacts/model.pkl "https://drive.usercontent.google.com/download?id=1D1J0BpomJzG6KZcrVNrYY__Ti0KCiGve&export=download&confirm=t"
```

**Ожидаемый результат:** файл `project/artifacts/model.pkl` размером ~1.6 ГБ.

#### 3. Проверьте, что файлы на месте

```bash
ls -lh data/data.csv artifacts/model.pkl
```

Должны отобразиться два файла:
```
-rw-r--r--  ...  1.3G data/data.csv
-rw-r--r--  ...  1.6G artifacts/model.pkl
```

#### Альтернатива: скачать через браузер

Если `curl` не работает (например, проблемы с большими файлами), откройте папку на Google Drive в браузере и скачайте файлы вручную:

- Папка: https://drive.google.com/drive/folders/12piY96E4N50C4mVjs_-PxX6rDyo3n91K
- Скопируйте `data.csv` → `project/data/data.csv`
- Скопируйте `model.pkl` → `project/artifacts/model.pkl`

---

### Вариант B: сгенерировать через ноутбуки

> **⚠ Внимание:** Этот способ требует много времени и оперативной памяти.
> - Предобработка данных занимает ~10–20 минут и требует ~8 ГБ ОЗУ.
> - Обучение модели (с RandomizedSearchCV) занимает ~30–60 минут и требует ~16 ГБ ОЗУ.
> - Итоговые файлы будут весить ~1.3 ГБ (data.csv) и ~1.6 ГБ (model.pkl).

#### Шаг 1. Подготовьте данные

Запустите ноутбук `data/preprocess_data.ipynb`:

```bash
# Убедитесь, что виртуальное окружение активировано
source .venv/bin/activate

# Запустите Jupyter
jupyter notebook data/preprocess_data.ipynb
```

Что делает этот ноутбук:
- Загружает `Extended_climate_data.csv` (исходные климатические данные).
- Загружает `Krasnodar_Municipalities_GeoJson.txt` (границы муниципалитетов).
- Загружает `Krasnodar_day_length_1995_2025.csv` (длина светового дня).
- Загружает `Krasnodar_infrastructure_1995_2025.csv` (географические признаки).
- Объединяет все данные, вычисляет календарные признаки (month, day, dayofyear).
- Сохраняет результат в `data/data.csv`.

**Результат:** создаётся файл `project/data/data.csv` (~1.3 ГБ, ~9.3 млн строк).

#### Шаг 2. Обучите модель

Запустите ноутбук `notebooks/train_model.ipynb`:

```bash
# Убедитесь, что виртуальное окружение активировано
source .venv/bin/activate

# Запустите Jupyter
jupyter notebook notebooks/train_model.ipynb
```

Что делает этот ноутбук:
- Загружает `data/data.csv` (должен быть создан на шаге 1).
- Разделяет данные хронологически: train (2018–2023), val (2024), test (2025).
- Строит Pipeline: ColumnTransformer (StandardScaler для чисел, OneHotEncoder для категорий) → ExtraTreesRegressor.
- Выполняет подбор гиперпараметров через RandomizedSearchCV.
- Оценивает модель на тестовом наборе (MAE, RMSE, R²).
- Сохраняет обученную модель в `artifacts/model.pkl`.

**Результат:** создаётся файл `project/artifacts/model.pkl` (~1.6 ГБ).

---

## Запуск (основной способ)

> **Перед запуском убедитесь, что файлы `data/data.csv` и `artifacts/model.pkl` существуют.**
> Если их нет — вернитесь к разделу «Получение данных и модели».

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

---

## Запуск FastAPI (дополнительно)

Помимо Streamlit-интерфейса, проект включает FastAPI-сервис с теми же возможностями.

```bash
cd project
source .venv/bin/activate
PYTHONPATH=. uvicorn src.service.main:app --host 0.0.0.0 --port 8000
```

После запуска:
- Документация Swagger: http://localhost:8000/docs
- Health-check: http://localhost:8000/health
- Список регионов: http://localhost:8000/regions
- Метрики: http://localhost:8000/metrics
- Предсказание: POST http://localhost:8000/predict

---

## Запуск в Docker

> **⚠ Важно:** При сборке Docker-образа файлы `data.csv` и `model.pkl` копируются в контейнер командой `COPY . .`.
> Убедитесь, что оба файла существуют в `project/` **до сборки образа**.
> Если их нет — вернитесь к разделу «Получение данных и модели».

### Сборка и запуск

```bash
cd project

# Сборка образа
docker build -t krasnodar-weather-app .

# Запуск контейнера
docker run --rm -p 8501:8501 krasnodar-weather-app
```

После запуска откройте http://localhost:8501.

### Docker с volume (без встраивания файлов в образ)

Если вы не хотите увеличивать размер Docker-образа, можно смонтировать файлы через volume:

```bash
cd project

# Сборка образа (без data.csv и model.pkl)
docker build -t krasnodar-weather-app .

# Запуск с монтированием локальных файлов
docker run --rm \
  -v "$(pwd)/data/data.csv:/app/data/data.csv" \
  -v "$(pwd)/artifacts/model.pkl:/app/artifacts/model.pkl" \
  -p 8501:8501 \
  krasnodar-weather-app
```

### Docker для FastAPI (вместо Streamlit)

```bash
docker run --rm \
  -v "$(pwd)/data/data.csv:/app/data/data.csv" \
  -v "$(pwd)/artifacts/model.pkl:/app/artifacts/model.pkl" \
  -p 8000:8000 \
  krasnodar-weather-app \
  uvicorn src.service.main:app --host 0.0.0.0 --port 8000
```

---

## Тесты

> **⚠ Важно:** Тесты загружают `artifacts/model.pkl` через `WeatherPredictor`. Без этого файла тесты упадут с ошибкой `FileNotFoundError`.
> Убедитесь, что модель получена (см. раздел «Получение данных и модели»).

```bash
cd project
source .venv/bin/activate
PYTHONPATH=. pytest tests/ -v
```

Ожидаемый результат — все 4 теста проходят:
```
tests/test_api_contract.py ....                                      [100%]
```

---

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

---

## Ограничения модели

Модель хорошо предсказывает температуру, длину светового дня и солнечную радиацию (R² > 0.7). Хуже справляется с осадками и направлением ветра — это ожидаемо из-за высокой локальной изменчивости этих параметров.

---

## Устранение неполадок

### «FileNotFoundError: data/data.csv» или «artifacts/model.pkl»

**Причина:** файлы не скачаны и не сгенерированы.
**Решение:** вернитесь к разделу «Получение данных и модели» и выполните Вариант A или B.

### «ModuleNotFoundError: No module named '...'»

**Причина:** не установлены зависимости.
**Решение:**
```bash
cd project
source .venv/bin/activate
pip install -r requirements.txt
```

### «InconsistentVersionWarning при загрузке model.pkl»

**Причина:** версия scikit-learn при обучении (1.7.2) отличается от текущей.
**Решение:** это предупреждение, не ошибка. Модель загрузится корректно в большинстве случаев.
Для полной совместимости установите scikit-learn==1.7.2:
```bash
pip install scikit-learn==1.7.2
```

### Docker: «Could not find model.pkl» при запуске контейнера

**Причина:** файл модели не скопирован в образ и не смонтирован через volume.
**Решение:** используйте volume (`-v` флаг) как описано в разделе «Docker с volume», или поместите `model.pkl` в `project/artifacts/` перед сборкой.

### Docker: «Permission denied» при монтировании volume

**Причина:** недостаточно прав на файлы.
**Решение:**
```bash
chmod 644 data/data.csv artifacts/model.pkl
```

---

## Демонстрация на защите

1. Установить зависимости: `pip install -r requirements.txt` (с Python 3.12)
2. Убедиться, что `data/data.csv` и `artifacts/model.pkl` на месте
3. Запустить: `PYTHONPATH=. streamlit run src/streamlit_app.py`
4. Показать выбор муниципалитета и даты
5. Показать прогноз погодных параметров
6. Показать карту с визуализацией
7. При необходимости — открыть `notebooks/train_model.ipynb` и показать метрики модели
