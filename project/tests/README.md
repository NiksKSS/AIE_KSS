# Тесты

Минимальный набор тестов проверяет:

- контракт endpoint `/health`;
- валидность минимального payload для `/predict`.

Запуск:

```bash
cd project
PYTHONPATH=. pytest tests
```
