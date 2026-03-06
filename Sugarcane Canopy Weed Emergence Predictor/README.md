# Sugarcane Canopy Weed Emergence Predictor
## Microclimate-Driven Herbicide Decision Intelligence for Brazilian Sugarcane

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0+-orange.svg)](https://xgboost.readthedocs.io/)
[![SHAP](https://img.shields.io/badge/SHAP-Explainability-brightgreen.svg)](https://shap.readthedocs.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-REST_API-teal.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerised-blue.svg)](https://www.docker.com/)

---

## Summary

This project models the emergence probability of *Brachiaria decumbens* (signal grass) within Brazilian sugarcane plantations — one of the most economically damaging weed infestations in South American agriculture, responsible for yield losses of 30–80% in heavily infested fields.

The system ingests daily microclimate telemetry from the NASA POWER Agroclimatology API, engineers agronomically meaningful features grounded in seed germination physics, and produces a 14-day emergence risk forecast via an XGBoost classifier. SHAP explainability surfaces the specific meteorological or soil drivers behind each prediction, and a FastAPI service containerised in Docker exposes the model for integration into field advisory platforms.

**Operational Objective:** A precision herbicide scheduling tool that minimizes unnecessary chemical applications while ensuring interventions land strictly within the thermodynamically optimal pre-emergence window.

---

## The Problem

*Brachiaria decumbens* competes aggressively with sugarcane for water, light, and nutrients during the critical establishment phase (0–120 days after planting). Its germination is highly responsive to a narrow confluence of conditions:

| Driver | Mechanism |
|--------|-----------|
| Soil temperature (>15 °C) | Activates metabolic processes in dormant seeds |
| Accumulated soil moisture | Enables imbibition and radicle emergence |
| Sub-canopy irradiance | Photomorphogenesis — seeds sense red/far-red ratio |
| Canopy closure lag | *B. decumbens* times emergence to gaps in sugarcane canopy |

Pre-emergent herbicide application is only effective within a 5–10 day window before seedling emergence. Too early and rainfall degrades the active ingredient; too late and the weed is already established. This project computes exactly when that window is approaching.

---

## Technical Architecture

```mermaid
flowchart TD
    %% Define Styles
    classDef api fill:#0f172a,stroke:#3b82f6,stroke-width:2px,color:#fff
    classDef script fill:#1e293b,stroke:#10b981,stroke-width:2px,color:#fff
    classDef data fill:#334155,stroke:#475569,stroke-width:1px,color:#cbd5e1
    classDef model fill:#450a0a,stroke:#ef4444,stroke-width:2px,color:#fff

    A[NASA POWER API]:::api -->|Daily Telemetry| B(01_data_ingestion.py):::script
    B -->|nasa_power_raw.csv| C(02_feature_engineering.py):::script
    
    subgraph Feature Engineering
        direction TB
        F1[Growing Degree Days]:::data
        F2[Hydrothermal Time]:::data
        F3[Canopy Density Sim]:::data
    end
    
    C --> F1 & F2 & F3
    F1 & F2 & F3 -->|features.csv| D(03_model_training.py):::script
    
    subgraph Predictive Engine
        M1[XGBoost Classifier]:::model
        M2[SHAP TreeExplainer]:::model
    end
    
    D --> M1
    M1 --> M2
    
    M2 -->|xgb.joblib| E(FastAPIREST Service):::api
    
    subgraph Deployment
        E --> E1[POST /predict]:::data
        E --> E2[Streamlit Dashboard]:::data
    end
```

---

## Feature Engineering

The critical design choice was encoding the *biophysical mechanism* of germination — not just treating meteorology as raw predictors.

### Hydrothermal Time (HTT) — the primary signal

HTT accumulates only when temperature *and* moisture are simultaneously above biological thresholds. A hot dry week contributes nothing; a cool wet week contributes nothing. Only their co-occurrence triggers germination progress, governed by the following integration:

$$ GDD_{t} = \max(T_{t} - T_{b}, 0) $$

$$ HTT_{t} = \left[ GDD_{t} \cdot \left(\frac{\psi_{t}}{\psi_{c}}\right) \right] \cdot \mathbf{1}_{\{\psi_t > \psi_{base}\}} $$

$$ HTT_{cumulative} = \sum_{t=0}^{n} HTT_{t} $$

Where $T_b$ is the base temperature for biological activity, $\psi_t$ is soil moisture tension, and $\psi_c$ is field capacity. *B. decumbens* requires an integrated HTT of $\approx 38$ MPa·°C·day for 50% germination probability ( Bradford 2002 hydrotime model).

### Canopy Density Simulation

Rather than using raw solar irradiance, I modelled the **sub-canopy light reaching the soil surface** using a sinusoidal canopy closure curve calibrated to Ribeirão Preto's typical planting calendar:

$$ \Phi_{canopy}(t) = \sin(\pi \cdot \omega_t)^{k} $$
$$ I_{sub}(t) = I_{raw}(t) \cdot (1 - \Phi_{canopy}(t)) $$

This matters because *B. decumbens* seeds are strongly photoblastic — they germinate faster in inter-row zones where canopy gaps persist.

### Feature Set (20 features)

| Category | Features | Agronomic rationale |
|----------|----------|---------------------|
| Thermal | `gdd`, `gdd_cumsum` | Heat accumulation drives metabolic activation |
| Hydraulic | `soil_moisture_mm`, `htt_cumsum` | Imbibition requires sustained moisture |
| Atmospheric | `vpd_kpa`, rolling VPD | Evaporative demand affects soil drying rate |
| Precipitation | 3/7/14-day sums | Infiltration and leaching dynamics |
| Temperature rolling | 3/7/14-day means | Short-term heat windows |
| Humidity rolling | 3/7/14-day means | Canopy microclimate |
| Radiation | `solar_rad_7d_sum`, `sub_canopy_rad` | Photomorphogenesis trigger |
| Structural | `canopy_density` | Shading suppression index |

---

## Modelling Decisions

### Why time-series cross-validation?

Standard k-fold CV leaks future information into the training set. In time-series data, rows adjacent in time are heavily autocorrelated. I used `TimeSeriesSplit` with 5 rolling folds, so each validation fold is strictly after its training fold — simulating real deployment where you predict into an unseen future period.

### Why XGBoost over Random Forest?

Gradient boosting's sequential error-correction captures subtle threshold effects in the germination physics (e.g., HTT crossing 38 MPa·°C·day). Random Forest averages independently, smoothing out exactly the sharp transitions that matter most agronomically.

### Class Imbalance

Emergence events are relatively rare (~25% of days meet all threshold conditions simultaneously). I used `scale_pos_weight = negative_count / positive_count` rather than SMOTE oversampling, which can create synthetic meteorological states that are physically impossible.

---

## SHAP Explainability

SHAP decomposes each prediction into per-feature contributions. This is critical for agronomic trust — a field advisor needs to understand *why* the model is flagging a risk, not just that it is.

Three explanation types are generated:

| Plot | Purpose |
|------|---------|
| `shap_global_importance.png` | Which features matter most across the full dataset |
| `shap_dot_plot.png` | How feature values (high/low) push risk up or down |
| `shap_waterfall_peak_day.png` | Feature-level breakdown for the single highest-risk prediction |

The API endpoint also returns the **top 5 SHAP drivers per prediction** inline in the JSON response — so a field advisory app can display plain-language explanations like *"Risk elevated by high 14-day precipitation accumulation (SHAP +0.34)"*.

---

## API Reference

### `POST /predict`

**Request:**
```json
{
  "zone_id": "zone_A3",
  "gdd": 12.4,
  "gdd_cumsum": 430.0,
  "vpd_kpa": 1.8,
  "canopy_density": 0.72,
  "soil_moisture_mm": 45.0,
  "htt_cumsum": 22.5,
  "precip_sum_3d": 8.5,
  "t2m_mean_3d": 28.2,
  "rh2m_mean_3d": 74.0,
  "vpd_mean_3d": 1.6,
  "precip_sum_7d": 22.0,
  "t2m_mean_7d": 27.8,
  "rh2m_mean_7d": 72.5,
  "vpd_mean_7d": 1.7,
  "precip_sum_14d": 55.0,
  "t2m_mean_14d": 27.5,
  "rh2m_mean_14d": 71.0,
  "vpd_mean_14d": 1.75,
  "solar_rad_7d_sum": 120.0,
  "sub_canopy_rad": 4.2
}
```

**Response:**
```json
{
  "zone_id": "zone_A3",
  "emergence_probability": 0.7831,
  "risk_level": "HIGH",
  "top_drivers": [
    {"feature": "htt_cumsum",     "shap_value": 0.4312, "direction": "increases_risk"},
    {"feature": "sub_canopy_rad", "shap_value": 0.2104, "direction": "increases_risk"},
    {"feature": "soil_moisture_mm","shap_value": 0.1876, "direction": "increases_risk"},
    {"feature": "precip_sum_14d", "shap_value": 0.1504, "direction": "increases_risk"},
    {"feature": "canopy_density", "shap_value": -0.0932,"direction": "reduces_risk"}
  ],
  "recommendation": "High emergence probability. Apply pre-emergent herbicide within 48 hours. Target inter-row zones with reduced canopy cover."
}
```

---

## Reproducing the Pipeline

```bash
# 1. Clone and navigate
git clone https://github.com/alexdbatista/data-science-portfolio.git
cd "data-science-portfolio/Sugarcane Canopy Weed Emergence Predictor"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Fetch NASA POWER data (2021–2022, Ribeirão Preto)
python 01_data_ingestion.py

# 4. Engineer features
python 02_feature_engineering.py

# 5. Train model + generate SHAP reports
python 03_model_training.py
# → models/xgb_weed_emergence.joblib
# → reports/shap_global_importance.png
# → reports/shap_dot_plot.png
# → reports/shap_waterfall_peak_day.png

# 6. Launch API locally
uvicorn app.main:app --reload --port 8000
# Interactive docs: http://localhost:8000/docs
```

### Docker Deployment

```bash
# Build image
docker build -t sugarcane-weed-predictor:latest .

# Run standalone
docker run -p 8000:8000 \
  -v $(pwd)/models:/app/models:ro \
  sugarcane-weed-predictor:latest

# Or with Docker Compose (API + Swagger UI)
docker-compose up --build
# API:         http://localhost:8000
# Swagger UI:  http://localhost:8080
```

---

## Files

```
Sugarcane Canopy Weed Emergence Predictor/
├── 01_data_ingestion.py          # NASA POWER API extraction
├── 02_feature_engineering.py     # Agronomic feature construction
├── 03_model_training.py          # XGBoost training + SHAP reports
├── app/
│   └── main.py                   # FastAPI REST service
├── Dockerfile                    # Multi-stage container build
├── docker-compose.yml            # API + Swagger UI stack
├── requirements.txt
├── README.md
├── data/                         # Generated by pipeline (gitignored)
│   ├── nasa_power_raw.csv
│   └── features.csv
├── models/                       # Trained artefacts (gitignored)
│   ├── xgb_weed_emergence.joblib
│   └── scaler.joblib
└── reports/                      # SHAP visualisations (gitignored)
    ├── confusion_matrix.png
    ├── shap_global_importance.png
    ├── shap_dot_plot.png
    └── shap_waterfall_peak_day.png
```

---

## 🔬 Agronomic Data Science Principles

**1. Latent Target Definition**
Building the binary target (`emergence_risk_14d`) from first principles — combining exact HTT thresholds, soil moisture constraints, and sub-canopy light availability — is the core of this pipeline. The model learns whatever signal the labels contain; unphysical agronomic labels produce mathematically meaningless models regardless of the ML architecture.

**2. Temporal Non-Stationarity in Environmental Data**
Standard k-fold cross-validation is fundamentally flawed for meteorological data due to high temporal autocorrelation. Utilizing `TimeSeriesSplit` with strict year-boundary splits prevents data leakage and provides an honest estimate of the model's out-of-sample inferential power for future growing seasons.

**3. Hard-Coding Physical Constraints**
Encoding the germination base temperature directly (GDD = max(T - Tb, 0)) removes the algorithm's burden of re-learning established biophysical thresholds. The gradient booster is mathematically reserved only for learning the nonlinear interdependencies between the feature matrices.

**4. Explainability as an Operational Requirement**
In agronomy, recommendations without causal explanation are un-deployable. The per-prediction SHAP waterfall provides the field agronomist with a concrete, verifiable biophysical reason to trigger an application pass—or the data needed to override the model when localized micro-conditions deviate from satellite telemetry.

---

## Data Sources

- **NASA POWER Agroclimatology API** — [power.larc.nasa.gov](https://power.larc.nasa.gov/)
  Daily meteorological data for agricultural applications, globally available
- *B. decumbens* germination parameters derived from the Bradford (2002) hydrotime model framework.
- Sugarcane canopy phenology calibrated to the Ribeirão Preto, SP agroclimatic zone.
