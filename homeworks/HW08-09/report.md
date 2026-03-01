# HW08-09 – PyTorch MLP: регуляризация и оптимизация обучения

## 1. Кратко: что сделано

- Выбран датасет **EMNIST (balanced)** - 47 классов символов (буквы + цифры)
- В части A сравнивались: base MLP, Dropout, BatchNorm, EarlyStopping
- В части B исследовались: влияние learning rate (O1, O2), SGD+momentum с weight decay (O3)

## 2. Среда и воспроизводимость

- Python: 3.12.12
- torch: 2.5.1+cu124, torchvision: 0.20.1+cu124
- Устройство (CPU/GPU): CPU
- Seed: 42 (torch.manual_seed, np.random.seed)
- Как запустить: открыть `HW08-09.ipynb` и выполнить Run All

## 3. Данные

- Датасет: **EMNIST Balanced** (47 классов)
- Разделение: train/val/test (80/20 от train + стандартный test из torchvision)
- Трансформации (transform): ToTensor(), Normalize((0.5,), (0.5,))
- Комментарий: EMNIST содержит рукописные буквы и цифры, 28x28 grayscale. 47 классов делают задачу сложнее, чем CIFAR10.

## 4. Базовая модель и обучение

- Модель MLP (кратко): 3 скрытых слоя (256->128->47), BatchNorm, ReLU
- Loss: CrossEntropyLoss
- Базовый Optimizer (для части A): Adam (lr=0.001)
- Batch size: 64
- Epochs (макс): 15-30
- EarlyStopping: patience=5, metric=val_accuracy

## 5. Часть A (S08): регуляризация (E1-E4)

- E1 (base): 2 скрытых слоя, без Dropout/BatchNorm
- E2 (Dropout): как E1 + Dropout(p=0.3)
- E3 (BatchNorm): как E1 + BatchNorm1d между Linear и ReLU
- E4 (EarlyStopping): E3 (лучший) + EarlyStopping (patience=5)

## 6. Часть B (S09): LR, оптимизаторы, weight decay (O1-O3)

- O1: LR слишком большой (Adam, lr=0.1)
- O2: LR слишком маленький (Adam, lr=1e-5)
- O3: SGD+momentum (momentum=0.9) + weight_decay=1e-4 (lr=0.01)

## 7. Результаты

Ссылки на файлы в репозитории:

- Таблица результатов: `./artifacts/runs.csv`
- Лучшая модель: `./artifacts/best_model.pt`
- Конфиг лучшей модели: `./artifacts/best_config.json`
- Кривые лучшего прогона: `./artifacts/figures/curves_best.png`
- Кривые "плохих LR": `./artifacts/figures/curves_lr_extremes.png`

Короткая сводка:

- Лучший эксперимент части A: **E3_BatchNorm** (val_accuracy=0.8502), E4_EarlyStop использовал ту же архитектуру с EarlyStopping (patience=5)
- Лучшая val_accuracy (E3_BatchNorm): **0.8502**
- Итоговая test_accuracy (для лучшей модели): **0.8459**
- Что видно на O1 (слишком большой LR): accuracy застревает на ~2% - модель не обучается, loss не уменьшается
- Что видно на O2 (слишком маленький LR): медленный рост accuracy (от 8% до 56% за 6 эпох), требуется больше эпох
- Как повёл себя O3 (SGD+momentum + weight decay): сопоставимо с BatchNorm (0.8516 vs 0.8502), стабильная сходимость

## 8. Анализ

- Переобучение видно на E1: разрыв между train (~87%) и val (~83%). Dropout (E2) немного улучшил val, но BatchNorm (E3) дал лучший результат - разрыв меньше, val accuracy выше.
- EarlyStopping в E4 остановил обучение на 15 эпохе (patience=5 без улучшения). Модель не переобучилась, но и значительного улучшения не дала - val accuracy осталась на уровне E3.
- O1 показывает классический признак слишком большого LR: loss застревает на плато (~3.87), accuracy около 2% ( random для 47 классов ~2.1%). Градиенты "перепрыгивают" минимум функции потерь.
- O2 демонстрирует обратную проблему: loss медленно уменьшается, accuracy растёт очень медленно. За 6 эпох val acc достигла только 56%.
- SGD+momentum (O3) с weight_decay показал результат сопоставимый с BatchNorm: 0.8516 vs 0.8502. Возможно, требуется подбор lr или больше эпох. Weight decay помогает регуляризации, но в данном случае BatchNorm уже справляется.
- Выбранный конфиг (BatchNorm + Adam + lr=0.001) разумен для EMNIST: архитектура не слишком сложная, данные относительно простые, BatchNorm стабилизирует обучение.

## 9. Итоговый вывод

Лучший конфиг: MLP с BatchNorm (256->128) + Adam (lr=0.001) + EarlyStopping. Test accuracy ~84.6%.

Что бы попробовали улучшить дальше:
1. Попробовать CNN вместо MLP - для изображений CNN обычно работает лучше
2. Увеличить dropout и добавить data augmentation
3. Попробовать learning rate scheduler (ReduceLROnPlateau)

## 10. Приложение (опционально)

Дополнительные графики доступны в: `./artifacts/figures/`
