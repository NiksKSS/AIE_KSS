# Артефакты модели

Основной артефакт проекта:

- `model.pkl` — финальный `sklearn.Pipeline` с препроцессингом и `ExtraTreesRegressor`.

Модель используется в `src/streamlit_app.py` для предсказания погоды.

Файл `model.pkl` крупный, поэтому он добавлен в `.gitignore`. Для локальной проверки положите модель в:

```
project/artifacts/model.pkl
```