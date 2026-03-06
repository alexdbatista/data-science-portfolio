"""
app/main.py
===========
FastAPI REST Service — Weed Emergence Prediction Endpoint

Exposes the trained XGBoost model as a JSON API suitable for integration
with field telemetry platforms, mobile apps, or agrifood dashboards.

Endpoints:
  GET  /health          — Liveness probe for container orchestrators
  POST /predict         — Single-zone emergence probability prediction
  POST /predict/batch   — Multi-zone batch prediction
  GET  /features        — Returns expected input schema

Run locally:
  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
"""

import joblib
import numpy as np
import pandas as pd
import shap
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional

# ---------------------------------------------------------------------------
# Paths & model loading
# ---------------------------------------------------------------------------
ROOT        = Path(__file__).parent.parent
MODEL_PATH  = ROOT / "models" / "xgb_weed_emergence.joblib"
SCALER_PATH = ROOT / "models" / "scaler.joblib"

try:
    model   = joblib.load(MODEL_PATH)
    scaler  = joblib.load(SCALER_PATH)
    explainer = shap.TreeExplainer(model)
    MODEL_LOADED = True
except FileNotFoundError:
    MODEL_LOADED = False

# Feature names the model expects (must match 02_feature_engineering.py output)
FEATURE_NAMES = [
    "gdd", "gdd_cumsum", "vpd_kpa", "canopy_density", "soil_moisture_mm",
    "htt_cumsum",
    "precip_sum_3d",  "t2m_mean_3d",  "rh2m_mean_3d",  "vpd_mean_3d",
    "precip_sum_7d",  "t2m_mean_7d",  "rh2m_mean_7d",  "vpd_mean_7d",
    "precip_sum_14d", "t2m_mean_14d", "rh2m_mean_14d", "vpd_mean_14d",
    "solar_rad_7d_sum", "sub_canopy_rad",
]

# ---------------------------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Sugarcane Weed Emergence Predictor API",
    description=(
        "Predicts *Brachiaria decumbens* emergence probability within a "
        "14-day window from microclimate and soil telemetry. "
        "Powered by XGBoost + SHAP explainability."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class FieldZoneFeatures(BaseModel):
    """Agronomic microclimate feature vector for a single field zone."""
    zone_id: Optional[str] = Field(None, example="zone_A3")
    gdd: float = Field(..., description="Growing degree days today (°C·day)", example=12.4)
    gdd_cumsum: float = Field(..., description="Cumulative GDD since season start", example=430.0)
    vpd_kpa: float = Field(..., description="Vapour pressure deficit (kPa)", example=1.8)
    canopy_density: float = Field(..., ge=0, le=1, description="Sugarcane canopy closure fraction", example=0.72)
    soil_moisture_mm: float = Field(..., description="Soil moisture from bucket model (mm)", example=45.0)
    htt_cumsum: float = Field(..., description="Cumulative hydrothermal time index", example=22.5)
    precip_sum_3d: float = Field(..., description="3-day precipitation total (mm)", example=8.5)
    t2m_mean_3d: float = Field(..., description="3-day mean temperature (°C)", example=28.2)
    rh2m_mean_3d: float = Field(..., description="3-day mean relative humidity (%)", example=74.0)
    vpd_mean_3d: float = Field(..., description="3-day mean VPD (kPa)", example=1.6)
    precip_sum_7d: float = Field(..., description="7-day precipitation total (mm)", example=22.0)
    t2m_mean_7d: float = Field(..., description="7-day mean temperature (°C)", example=27.8)
    rh2m_mean_7d: float = Field(..., description="7-day mean relative humidity (%)", example=72.5)
    vpd_mean_7d: float = Field(..., description="7-day mean VPD (kPa)", example=1.7)
    precip_sum_14d: float = Field(..., description="14-day precipitation total (mm)", example=55.0)
    t2m_mean_14d: float = Field(..., description="14-day mean temperature (°C)", example=27.5)
    rh2m_mean_14d: float = Field(..., description="14-day mean relative humidity (%)", example=71.0)
    vpd_mean_14d: float = Field(..., description="14-day mean VPD (kPa)", example=1.75)
    solar_rad_7d_sum: float = Field(..., description="7-day cumulative solar radiation (MJ/m²)", example=120.0)
    sub_canopy_rad: float = Field(..., description="Sub-canopy irradiance reaching soil (MJ/m²/day)", example=4.2)


class PredictionResponse(BaseModel):
    zone_id: Optional[str]
    emergence_probability: float
    risk_level: str
    top_drivers: List[dict]
    recommendation: str


class BatchRequest(BaseModel):
    zones: List[FieldZoneFeatures]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

RISK_THRESHOLDS = {
    "LOW":      (0.0, 0.35),
    "MODERATE": (0.35, 0.65),
    "HIGH":     (0.65, 1.01),
}

RECOMMENDATIONS = {
    "LOW":      "Emergence unlikely within 14 days. Standard monitoring interval.",
    "MODERATE": "Conditions approaching threshold. Prepare herbicide equipment; "
                "reassess in 3–5 days.",
    "HIGH":     "High emergence probability. Apply pre-emergent herbicide within "
                "48 hours. Target inter-row zones with reduced canopy cover.",
}


def classify_risk(probability: float) -> str:
    for level, (lo, hi) in RISK_THRESHOLDS.items():
        if lo <= probability < hi:
            return level
    return "HIGH"


def compute_shap_drivers(feature_vector: np.ndarray, top_n: int = 5) -> List[dict]:
    """Return top N SHAP contributors for a single prediction."""
    sv = explainer.shap_values(feature_vector.reshape(1, -1))[0]
    driver_df = pd.DataFrame({
        "feature": FEATURE_NAMES,
        "shap_value": sv,
        "abs_shap": np.abs(sv),
    }).sort_values("abs_shap", ascending=False).head(top_n)

    return [
        {
            "feature": row["feature"],
            "shap_value": round(row["shap_value"], 4),
            "direction": "increases_risk" if row["shap_value"] > 0 else "reduces_risk",
        }
        for _, row in driver_df.iterrows()
    ]


def predict_single(zone: FieldZoneFeatures) -> PredictionResponse:
    if not MODEL_LOADED:
        raise HTTPException(status_code=503,
                            detail="Model artefacts not found. Run 03_model_training.py first.")

    raw = np.array([getattr(zone, f) for f in FEATURE_NAMES], dtype=float)
    scaled = scaler.transform(raw.reshape(1, -1))

    prob = float(model.predict_proba(scaled)[0, 1])
    risk = classify_risk(prob)
    drivers = compute_shap_drivers(scaled[0])

    return PredictionResponse(
        zone_id=zone.zone_id,
        emergence_probability=round(prob, 4),
        risk_level=risk,
        top_drivers=drivers,
        recommendation=RECOMMENDATIONS[risk],
    )


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/health", tags=["Infrastructure"])
def health_check():
    return {
        "status": "healthy",
        "model_loaded": MODEL_LOADED,
        "version": "1.0.0",
    }


@app.get("/features", tags=["Schema"])
def get_feature_schema():
    """Returns the list of features expected by the model."""
    return {"features": FEATURE_NAMES, "target": "emergence_risk_14d"}


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
def predict(zone: FieldZoneFeatures):
    """
    Predict *Brachiaria decumbens* emergence probability for a single field zone.
    Returns probability (0–1), risk tier, top SHAP drivers, and a field recommendation.
    """
    return predict_single(zone)


@app.post("/predict/batch", tags=["Prediction"])
def predict_batch(request: BatchRequest):
    """
    Batch prediction for multiple field zones in a single call.
    Suitable for fleet telemetry ingestion pipelines.
    """
    results = []
    for zone in request.zones:
        try:
            results.append(predict_single(zone).dict())
        except Exception as e:
            results.append({"zone_id": zone.zone_id, "error": str(e)})
    return {"predictions": results, "count": len(results)}
