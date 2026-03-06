"""
02_feature_engineering.py
==========================
Agronomic Feature Engineering for Brachiaria decumbens Emergence Modeling

Transforms raw NASA POWER meteorological telemetry into features that
encode the biologically relevant mechanisms of tropical weed germination:

  1. Hydrothermal Time (HTT) — combined heat + moisture accumulation
  2. Growing Degree Days (GDD) — heat accumulation above base temperature
  3. Vapour Pressure Deficit (VPD) — atmospheric drying stress on soil
  4. Precipitation rolling statistics — infiltration / soil recharge proxy
  5. Solar radiation accumulation — photomorphogenesis trigger for seeds
  6. Simulated canopy density — sugarcane shading effect on weed light access
  7. Soil moisture proxy (bucket model, simplified FAO-56)

Brachiaria decumbens agronomic thresholds (literature values):
  Base germination temperature (Tb)  : 15 °C
  Optimal germination temperature    : 30 °C
  HTT for 50% germination (θHT50)   : 38 MPa·°C·day  (Bradford 2002 model)
"""

import pandas as pd
import numpy as np
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
RAW_PATH = DATA_DIR / "nasa_power_raw.csv"
OUT_PATH = DATA_DIR / "features.csv"

# ---------------------------------------------------------------------------
# Brachiaria decumbens agronomic constants
# ---------------------------------------------------------------------------
T_BASE     = 15.0   # Base temperature for germination (°C)
T_OPT      = 30.0   # Optimal germination temperature (°C)
T_CEIL     = 45.0   # Ceiling temperature for germination (°C)
HTT_50     = 38.0   # Hydrothermal time for 50% emergence (MPa·°C·day)

# Simple bucket soil model parameters
SOIL_WATER_CAPACITY = 100.0   # mm available water capacity
ET_COEFFICIENT      = 0.6     # crop coefficient × reference ET approximation

# Sugarcane canopy closure schedule (fraction of ground shaded per DOY)
# Approximates typical Ribeirao Preto planting calendar (harvest March, ratoon April)
CANOPY_PEAK_DOY   = 240       # Late August — peak vegetative growth
CANOPY_EMERGENCE_DOY = 90     # ~April — canopy closes over inter-rows


# ---------------------------------------------------------------------------
# Feature functions
# ---------------------------------------------------------------------------

def growing_degree_days(t2m: pd.Series, t_base: float = T_BASE) -> pd.Series:
    """Daily thermal contribution above germination base temperature."""
    return (t2m - t_base).clip(lower=0.0)


def canopy_density(doy: pd.Series) -> pd.Series:
    """
    Sinusoidal approximation of sugarcane canopy leaf area index (0–1 scale).
    Uses a half-sine wave peaking at CANOPY_PEAK_DOY.
    """
    phase = (doy - CANOPY_EMERGENCE_DOY) / (CANOPY_PEAK_DOY - CANOPY_EMERGENCE_DOY)
    density = np.sin(np.pi * phase.clip(0, 1))
    return density.clip(0, 1)


def vapour_pressure_deficit(t2m: pd.Series, rh2m: pd.Series) -> pd.Series:
    """
    Compute daily mean VPD (kPa) using the Tetens formula.
    VPD = es × (1 - RH/100)
    es = 0.6108 × exp(17.27 × T / (T + 237.3))  [Tetens, 1930]
    """
    es = 0.6108 * np.exp(17.27 * t2m / (t2m + 237.3))
    vpd = es * (1.0 - rh2m / 100.0)
    return vpd.clip(lower=0.0)


def soil_moisture_bucket(precip: pd.Series,
                          t2m: pd.Series,
                          capacity: float = SOIL_WATER_CAPACITY,
                          et_coeff: float = ET_COEFFICIENT) -> pd.Series:
    """
    Simplified FAO-56 single-layer bucket model for daily soil moisture (mm).

    SM[t] = SM[t-1] + P[t] − ETc[t],  clamped to [0, capacity]

    ETc is approximated from the Hargreaves–Samani formula skeleton
    (T-driven; full radiation data used for GDD only given data fidelity).
    """
    etc_approx = et_coeff * (t2m - T_BASE).clip(lower=0) * 0.5   # crude proxy
    sm = np.empty(len(precip))
    sm[0] = capacity * 0.5   # initialise at field capacity midpoint
    for i in range(1, len(precip)):
        sm[i] = sm[i - 1] + precip.iloc[i] - etc_approx.iloc[i]
        sm[i] = min(max(sm[i], 0.0), capacity)
    return pd.Series(sm, index=precip.index, name="soil_moisture_mm")


def hydrothermal_time(gdd: pd.Series, sm: pd.Series,
                      capacity: float = SOIL_WATER_CAPACITY) -> pd.Series:
    """
    Cumulative hydrothermal time index.

    Daily HTT contribution = GDD × (SM / capacity)
    This captures the joint requirement of warm temperatures AND adequate
    moisture for B. decumbens germination triggering.
    """
    sm_frac = (sm / capacity).clip(0, 1)
    return (gdd * sm_frac).cumsum()


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def build_features(df_raw: pd.DataFrame) -> pd.DataFrame:
    df = df_raw.copy()

    # 1. Growing Degree Days
    df["gdd"] = growing_degree_days(df["T2M"])

    # 2. Cumulative GDD (heat accumulation)
    df["gdd_cumsum"] = df["gdd"].cumsum()

    # 3. VPD
    df["vpd_kpa"] = vapour_pressure_deficit(df["T2M"], df["RH2M"])

    # 4. Sugarcane canopy density proxy
    doy = pd.Series(df.index.day_of_year, index=df.index)
    df["canopy_density"] = canopy_density(doy)

    # 5. Soil moisture (bucket model)
    df["soil_moisture_mm"] = soil_moisture_bucket(df["PRECTOTCORR"], df["T2M"])

    # 6. Hydrothermal Time
    df["htt_cumsum"] = hydrothermal_time(df["gdd"], df["soil_moisture_mm"])

    # 7. Rolling meteorological windows (3-day, 7-day, 14-day)
    for window in [3, 7, 14]:
        df[f"precip_sum_{window}d"]  = df["PRECTOTCORR"].rolling(window, min_periods=1).sum()
        df[f"t2m_mean_{window}d"]    = df["T2M"].rolling(window, min_periods=1).mean()
        df[f"rh2m_mean_{window}d"]   = df["RH2M"].rolling(window, min_periods=1).mean()
        df[f"vpd_mean_{window}d"]    = df["vpd_kpa"].rolling(window, min_periods=1).mean()

    # 8. Solar radiation accumulation
    df["solar_rad_7d_sum"] = df["ALLSKY_SFC_SW_DWN"].rolling(7, min_periods=1).sum()

    # 9. Sub-canopy light availability (canopy interception)
    #    Light reaching soil = irradiance × (1 - canopy_density)
    df["sub_canopy_rad"] = df["ALLSKY_SFC_SW_DWN"] * (1 - df["canopy_density"])

    # 10. Emergence risk label (target variable)
    #     Rule: HTT exceeds 50% germination threshold AND soil moisture > 25 mm
    #     AND sub-canopy light > threshold (seeds need >3 MJ/m²/day to germinate)
    df["emergence_risk_14d"] = (
        (df["htt_cumsum"] > HTT_50) &
        (df["soil_moisture_mm"] > 25.0) &
        (df["sub_canopy_rad"] > 3.0)
    ).astype(int)

    # Drop raw API columns (retained in nasa_power_raw.csv)
    feature_cols = [c for c in df.columns if c not in
                    ["T2M", "PRECTOTCORR", "RH2M", "ALLSKY_SFC_SW_DWN"]]
    return df[feature_cols]


if __name__ == "__main__":
    print(f"[INFO] Loading raw telemetry from {RAW_PATH} ...")
    df_raw = pd.read_csv(RAW_PATH, index_col="Date", parse_dates=True)

    print("[INFO] Building agronomic features ...")
    df_feat = build_features(df_raw)

    print(f"[INFO] Feature matrix shape: {df_feat.shape}")
    print("\n--- Feature Preview ---")
    print(df_feat.head().to_string())

    print(f"\n--- Target class distribution ---")
    vc = df_feat["emergence_risk_14d"].value_counts()
    print(f"  No risk  (0): {vc.get(0, 0)}")
    print(f"  At risk  (1): {vc.get(1, 0)}")

    df_feat.to_csv(OUT_PATH)
    print(f"\n[DONE] Features persisted → {OUT_PATH}")
