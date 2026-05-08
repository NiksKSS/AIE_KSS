# Самопроверка проекта

| # | Критерий | Да/Нет | Где смотреть / комментарий |
|---|---|---|---|
| 1 | Сервис запускается по инструкциям из `project/README.md` и работает | ✅ | `README.md`, разделы «Запуск (основной способ)», «Запуск FastAPI», «Docker» |
| 2 | Endpoint `/predict` использует реальную модель, а не заглушку | ✅ | `src/service/main.py`, `src/models/predictor.py`, `artifacts/model.pkl` |
| 3 | Есть EDA и хотя бы один эксперимент с метриками | ✅ | `data/preprocess_data.ipynb`, `notebooks/train_model.ipynb`, `report.md` |
| 4 | Есть baseline/улучшенная модель и сравнение по метрикам | ✅ | `notebooks/train_model.ipynb`, `report.md`, разделы 4-5 |
| 5 | Код не свален в один ноутбук: есть структура в `src/` | ✅ | `src/config.py`, `src/models/`, `src/service/`, `src/streamlit_app.py` |
| 6 | Есть Dockerfile или понятный сценарий развёртывания без Docker | ✅ | `Dockerfile`, `README.md`, раздел «Docker» |
| 7 | Есть `.env.example` и нет реальных секретов/паролей | ✅ | `configs/.env.example`, `.gitignore` |
| 8 | Реализованы логи/наблюдаемость, минимум консольные логи + `/health` | ✅ | `src/service/main.py`: middleware логирования, `/health`, `/metrics` |
| 9 | В `report.md` обоснован выбор финальной модели по экспериментам | ✅ | `report.md`, разделы «Результаты» и «Модели и эксперименты» |
| 10 | `README.md` и `report.md` позволяют понять сценарий демонстрации | ✅ | `README.md`, раздел «Демонстрация»; `report.md`, раздел 9 |

**Итого:** 10 / 10.

Самооценка честная при условии, что для проверки доступны локальные артефакты `data/data.csv` и `artifacts/model.pkl`. Большие файлы добавлены в `.gitignore`; ё