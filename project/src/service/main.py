from __future__ import annotations

import logging
import time

from fastapi import FastAPI, HTTPException, Request

from src.config import DATA_PATH, LOG_LEVEL, MODEL_PATH
from src.models.predictor import WeatherPredictor
from src.service.schemas import HealthResponse, PredictRequest, PredictResponse

# Настройка логирования для приложения
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)

# Инициализация FastAPI-приложения
app = FastAPI(
    title="Krasnodar Weather Prediction API",
    description="API for predicting weather parameters in Krasnodar Krai municipalities.",
    version="1.0.0",
)

# Инициализация предсказателя погоды и метрик
predictor = WeatherPredictor()
metrics = {"requests_total": 0, "predict_requests_total": 0, "predict_errors_total": 0}

# Middleware для логирования HTTP-запросов
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    metrics["requests_total"] += 1
    response = await call_next(request)
    elapsed_ms = (time.perf_counter() - start) * 1000
    logger.info(
        "%s %s -> %s %.2fms",
        request.method,
        request.url.path,
        response.status_code,
        elapsed_ms,
    )
    return response

# Endpoint проверки здоровья сервиса
@app.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(status="ok", model_path=str(MODEL_PATH), data_path=str(DATA_PATH))

# Endpoint для получения списка доступных регионов
@app.get("/regions")
def regions():
    return predictor.available_regions()

# Endpoint для получения метрик
@app.get("/metrics")
def get_metrics():
    return metrics

# Endpoint для предсказания погоды
@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    try:
        metrics["predict_requests_total"] += 1
        result = predictor.predict_region(
            admin_center=request.admin_center,
            forecast_date=request.date,
            lat=request.lat,
            lon=request.lon,
        )
        return PredictResponse(
            admin_center=result["admin_center"],
            date=result["date"],
            points_used=result["points_used"],
            predictions=result["prediction"],
        )
    except Exception as e:
        metrics["predict_errors_total"] += 1
        logger.error("Prediction error: %s", str(e))
        raise HTTPException(status_code=500, detail="Prediction failed")