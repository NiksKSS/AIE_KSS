from __future__ import annotations

from datetime import date
import logging

import joblib
import numpy as np
import pandas as pd

from src.config import DATA_PATH, FEATURE_COLUMNS, MODEL_PATH, TARGET_VARS


logger = logging.getLogger(__name__)


class WeatherPredictor:
    """Загружает обученную модель и подготавливает признаки для инференса."""

    def __init__(self, model_path=MODEL_PATH, data_path=DATA_PATH):
        self.model_path = model_path
        self.data_path = data_path
        self._model = None
        self._data = None

    @property
    def model(self):
        if self._model is None:
            logger.info("Loading model from %s", self.model_path)
            model_info = joblib.load(self.model_path)
            self._model = model_info["model"] if isinstance(model_info, dict) else model_info
        return self._model

    @property
    def data(self) -> pd.DataFrame:
        if self._data is None:
            logger.info("Loading data from %s", self.data_path)
            df = pd.read_csv(self.data_path)
            df["date"] = pd.to_datetime(df["date"])
            self._data = df
        return self._data

    def available_regions(self) -> list[str]:
        return sorted(self.data["admin_center"].dropna().unique().tolist())

    def build_features(
        self,
        admin_center: str,
        forecast_date: date,
        lat: float | None = None,
        lon: float | None = None,
        sea_border: str | None = None,
        mountain_border: int | None = None,
    ) -> pd.DataFrame:
        if lat is not None and lon is not None:
            row = {
                "lat": lat,
                "lon": lon,
                "sea_border": sea_border or "No sea",
                "mountain_border": int(mountain_border or 0),
                "admin_center": admin_center,
            }
            points = pd.DataFrame([row])
        else:
            region_rows = self.data[self.data["admin_center"] == admin_center]
            if region_rows.empty:
                raise ValueError(f"Unknown admin_center: {admin_center}")
            points = (
                region_rows[["lat", "lon", "sea_border", "mountain_border", "admin_center"]]
                .drop_duplicates(subset=["lat", "lon"])
                .reset_index(drop=True)
            )

        ts = pd.Timestamp(forecast_date)
        points["month"] = ts.month
        points["day"] = ts.day
        points["dayofyear"] = ts.dayofyear
        points["mountain_border"] = points["mountain_border"].astype(int)
        return points[FEATURE_COLUMNS]

    def predict(self, features: pd.DataFrame) -> pd.DataFrame:
        raw_predictions = self.model.predict(features)
        predictions = pd.DataFrame(raw_predictions, columns=TARGET_VARS)
        predictions["wind_direction"] = predictions["wind_direction"] % 360
        return predictions

    def predict_region(
        self,
        admin_center: str,
        forecast_date: date,
        lat: float | None = None,
        lon: float | None = None,
        sea_border: str | None = None,
        mountain_border: int | None = None,
    ) -> dict:
        features = self.build_features(
            admin_center=admin_center,
            forecast_date=forecast_date,
            lat=lat,
            lon=lon,
            sea_border=sea_border,
            mountain_border=mountain_border,
        )
        predictions = self.predict(features)
        return {
            "admin_center": admin_center,
            "date": str(forecast_date),
            "points_used": int(len(features)),
            "prediction": aggregate_predictions(predictions),
        }


def circular_mean_degrees(values) -> float:
    series = pd.to_numeric(pd.Series(values), errors="coerce").dropna()
    if series.empty:
        return float("nan")

    radians = np.deg2rad(series % 360)
    sin_mean = np.sin(radians).mean()
    cos_mean = np.cos(radians).mean()
    if np.isclose(sin_mean, 0) and np.isclose(cos_mean, 0):
        return float("nan")
    return float((np.rad2deg(np.arctan2(sin_mean, cos_mean)) + 360) % 360)


def aggregate_predictions(predictions: pd.DataFrame) -> dict[str, float | None]:
    result = {}
    for column in TARGET_VARS:
        if column == "wind_direction":
            value = circular_mean_degrees(predictions[column])
        else:
            value = pd.to_numeric(predictions[column], errors="coerce").mean()
        result[column] = None if pd.isna(value) else round(float(value), 4)
    return result
