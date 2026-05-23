# Тесты

Минимальный набор тестов проверяет:

- контракт endpoint `/health`;
- валидность минимального payload для `/predict`.

## Зависимости

Тесты загружают `artifacts/model.pkl` через `WeatherPredictor`. **Без этого файла тесты не запустятся.**

Если модель отсутствует — см. инструкцию в `project/README.md`, раздел «Получение данных и модели».

## Запуск

```bash
cd project
source .venv/bin/activate
PYTHONPATH=. pytest tests -v
```
