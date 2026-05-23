# Данные проекта

Папка содержит данные для проекта прогнозирования погоды по муниципалитетам Краснодарского края.

## Файлы

- `sample_data.csv` — маленький пример структуры итоговой таблицы, безопасный для хранения в Git.
- `data.csv` — полный локальный датасет для обучения и инференса.
- `Extended_climate_data.csv` — расширенные исходные климатические данные.
- `Krasnodar_day_length_1995_2025.csv` — длина светового дня.
- `Krasnodar_infrastructure_1995_2025.csv` — дополнительные географические/инфраструктурные признаки.
- `Krasnodar_Municipalities_GeoJson.txt` — границы муниципалитетов для карты.
- `Krasnodar_Region_GeoJson.txt` — граница региона.
- `preprocess_data.ipynb` — подготовка и первичный анализ данных.

## Политика хранения

Некоторые CSV-файлы (`data.csv`, `Extended_climate_data.csv`) большие, поэтому они добавлены в `.gitignore`. В репозитории хранятся `sample_data.csv`, `Krasnodar_day_length_1995_2025.csv`, `Krasnodar_infrastructure_1995_2025.csv`, ноутбук подготовки и описание данных. Для запуска API и Streamlit преподавателю нужны локальные файлы:

- `data/data.csv`;
- `data/Krasnodar_Municipalities_GeoJson.txt`;
- `artifacts/model.pkl`.

Данные не содержат персональных данных, паролей, токенов или другой секретной информации.
