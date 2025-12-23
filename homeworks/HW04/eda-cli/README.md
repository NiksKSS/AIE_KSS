# S04 – eda_cli: мини-EDA для CSV


Небольшое CLI-приложение для базового анализа CSV-файлов.  
Используется в рамках Семинара 04 курса «Инженерия ИИ» и как основа HTTP-сервиса качества датасетов в HW04 (FastAPI + REST API).


## Требования


- Python 3.11+  
- [uv](https://docs.astral.sh/uv/) установлен в систему

Дополнительно для HTTP-сервиса используются зависимости `fastapi`, `uvicorn[standard]`, `python-multipart`, которые подключаются через `pyproject.toml` и устанавливаются вместе с проектом командой `uv sync`.


## Инициализация проекта


В корне проекта (S04/HW04):

```bash
uv sync
```

Эта команда:

- создаст виртуальное окружение `.venv`;  
- установит зависимости из `pyproject.toml`;  
- установит сам проект `eda-cli` в окружение.


### Структура проекта (HW04)

В репозитории ожидается следующая структура:

```text
homeworks/
  HW04/
    eda-cli/
      pyproject.toml
      README.md
      src/
        eda_cli/
          __init__.py
          core.py
          viz.py
          cli.py
          api.py
      tests/
        test_core.py
      data/
        example.csv
```

Именно этот проект внутри `homeworks/HW04/` используется для проверки HW04.


## Запуск CLI


### Краткий обзор


```bash
uv run eda-cli overview data/example.csv
```


Параметры:

- `--sep` – разделитель (по умолчанию `,`);  
- `--encoding` – кодировка (по умолчанию `utf-8`).


### Полный EDA-отчёт


```bash
uv run eda-cli report data/example.csv --out-dir reports
```


Дополнительные параметры:  
- `--title TEXT` — заголовок отчёта в report.md (по умолчанию: EDA-отчёт)  
- `--top-k-categories N` — сколько самых частых значений показывать для категориальных признаков (по умолчанию: 5)  
- `--max-hist-columns N` — макс. число числовых колонок для гистограмм (по умолчанию: 6)


Пример с новыми опциями:
```bash
uv run eda-cli report data/example.csv \
  --out-dir my_report \
  --title "Анализ пользовательских данных" \
  --top-k-categories 10 \
  --max-hist-columns 4
```


В результате в каталоге `reports/` появятся:

- `report.md` – основной отчёт в Markdown;  
- `summary.csv` – таблица по колонкам;  
- `missing.csv` – пропуски по колонкам;  
- `correlation.csv` – корреляционная матрица (если есть числовые признаки);  
- `top_categories/*.csv` – top-k категорий по строковым признакам;  
- `hist_*.png` – гистограммы числовых колонок;  
- `missing_matrix.png` – визуализация пропусков;  
- `correlation_heatmap.png` – тепловая карта корреляций.


### Новые эвристики качества данных


В отчёте `report.md` теперь автоматически анализируются дополнительные признаки качества:

- **Константные колонки** — если все значения в колонке одинаковые (например, `[5, 5, 5]`), это может означать ошибку в сборе данных.  
- **Высокая кардинальность категорий** — если в категориальной колонке доля уникальных значений превышает 50% (например, почти каждая строка имеет своё значение), такая колонка может быть не категорией, а ID или шумом.

Также считаются базовые флаги качества (`too_few_rows`, `too_many_columns`, `too_many_missing`) и интегральная метрика `quality_score` в диапазоне от 0 до 1, которая используется и в HTTP-сервисе.


## HTTP-сервис качества датасетов (HW04)


На основе ядра `eda-cli` реализован HTTP-сервис качества датасетов на FastAPI (`src/eda_cli/api.py`).


Запуск сервера (из папки проекта, например `homeworks/HW04/eda-cli`):

```bash
uv run uvicorn eda_cli.api:app --reload --port 8000
# Эквивалентная команда без uv:
uvicorn eda_cli.api:app --reload --port 8000
```

Доступна интерактивная документация по адресу `http://127.0.0.1:8000/docs`.


Реализованы следующие эндпоинты:

- `GET /health` — health-check сервиса, возвращает статус и версию.  

- `POST /quality` — принимает агрегированные признаки датасета (модель `QualityRequest`, JSON с полями `n_rows`, `n_cols`, `max_missing_share`, `numeric_cols`, `categorical_cols`) и возвращает эвристическую оценку качества (`QualityResponse`) с полями `ok_for_model`, `quality_score`, `message`, `latency_ms`, `flags`, `dataset_shape`.  

- `POST /quality-from-csv` — принимает CSV-файл в формате `multipart/form-data` (поле `file` с типом `UploadFile`), использует функции `summarize_dataset`, `missing_table`, `compute_quality_flags` и возвращает `quality_score` и флаги качества; при ошибках чтения или пустом CSV возвращает код `400`.  

- `POST /quality-flags-from-csv` — дополнительный эндпоинт HW04, принимает CSV-файл в формате `multipart/form-data` (поле `file`) и возвращает полный набор булевых флагов качества (включая новые: `has_constant_columns`, `has_high_cardinality_categoricals`).


## Тесты


```bash
uv run pytest -q
```


Тесты проверяют:

- корректную работу функций `summarize_dataset`, `missing_table`, `correlation_matrix`, `top_categories`, `compute_quality_flags`;  
- диапазон значения `quality_score`;  
- наличие и корректность новых флагов `has_constant_columns` и `has_high_cardinality_categoricals`.


### Команды для проверки HW04

Для проверки решения HW04 используются следующие команды (из папки проекта внутри `homeworks/HW04/eda-cli`):

```bash
uv sync
uv run eda-cli report data/example.csv --out-dir reports_example
uv run pytest -q
uv run uvicorn eda_cli.api:app --port 8000
```

После запуска сервиса эндпоинты `/health`, `/quality`, `/quality-from-csv` и `/quality-flags-from-csv` должны работать согласно описанию выше.