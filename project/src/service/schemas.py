import datetime as dt
from typing import Dict, Optional

from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    admin_center: str = Field(..., examples=["Краснодар"])
    date: dt.date = Field(..., examples=["2026-06-15"])
    lat: Optional[float] = Field(default=None, ge=-90, le=90)
    lon: Optional[float] = Field(default=None, ge=-180, le=180)
    sea_border: Optional[str] = Field(default=None, examples=["No sea"])
    mountain_border: Optional[int] = Field(default=None, ge=0, le=1)


class PredictResponse(BaseModel):
    admin_center: str
    date: str
    points_used: int
    predictions: Dict[str, Optional[float]]


class HealthResponse(BaseModel):
    status: str
    model_path: str
    data_path: str
