"""
01_data_ingestion.py
====================
NASA POWER Agroclimatology API Extraction Pipeline
Target region: Ribeirão Preto, São Paulo, Brazil — primary sugarcane hub.

Extracts daily meteorological telemetry required to compute cumulative
hydrothermal time for Brachiaria decumbens (signal grass) emergence modeling.

Parameters retrieved:
  T2M             – Air temperature at 2 m (°C)
  PRECTOTCORR     – Bias-corrected total precipitation (mm)
  RH2M            – Relative humidity at 2 m (%)
  ALLSKY_SFC_SW_DWN – All-sky surface shortwave downward irradiance (MJ/m²/day)
"""

import requests
import pandas as pd
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
LATITUDE  = -21.17   # Ribeirão Preto, SP
LONGITUDE = -47.81
START_DATE = "20210101"
END_DATE   = "20221231"

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
RAW_OUT  = DATA_DIR / "nasa_power_raw.csv"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def fetch_nasa_power_data(lat: float, lon: float, start: str, end: str) -> pd.DataFrame:
    """
    Connect to the NASA POWER Agroclimatology daily API and return a
    tidy DataFrame indexed by date.

    Parameters
    ----------
    lat, lon : float
        Decimal-degree coordinates of the target field zone.
    start, end : str
        Query window in YYYYMMDD format.

    Returns
    -------
    pd.DataFrame
        Columns: T2M, PRECTOTCORR, RH2M, ALLSKY_SFC_SW_DWN
        Index  : datetime (daily frequency)
    """
    url = "https://power.larc.nasa.gov/api/temporal/daily/point"
    params = {
        "parameters": "T2M,PRECTOTCORR,RH2M,ALLSKY_SFC_SW_DWN",
        "community": "AG",
        "longitude": lon,
        "latitude": lat,
        "start": start,
        "end": end,
        "format": "JSON",
    }

    print(f"[INFO] Querying NASA POWER API for ({lat}, {lon}) ...")
    response = requests.get(url, params=params, timeout=60)
    response.raise_for_status()
    payload = response.json()

    features = payload["properties"]["parameter"]

    # Reshape: keys are dates (YYYYMMDD str), values are measurements
    df = pd.DataFrame(features)
    df.index = pd.to_datetime(df.index, format="%Y%m%d")
    df.index.name = "Date"

    # NASA POWER uses -999 as a fill value — replace with NaN
    df.replace(-999.0, float("nan"), inplace=True)

    return df


def validate_dataframe(df: pd.DataFrame) -> None:
    """Basic sanity checks on the retrieved telemetry."""
    expected_cols = {"T2M", "PRECTOTCORR", "RH2M", "ALLSKY_SFC_SW_DWN"}
    missing = expected_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing expected columns: {missing}")

    miss_pct = df.isna().mean() * 100
    for col, pct in miss_pct.items():
        if pct > 5:
            print(f"[WARN] {col} has {pct:.1f}% missing values.")
        else:
            print(f"[OK]   {col}: {pct:.1f}% missing.")

    print(f"\n[INFO] Date range : {df.index.min().date()} → {df.index.max().date()}")
    print(f"[INFO] Total rows  : {len(df)}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    df_raw = fetch_nasa_power_data(LATITUDE, LONGITUDE, START_DATE, END_DATE)

    print("\n--- Data Validation ---")
    validate_dataframe(df_raw)

    print("\n--- Sample Telemetry (first 5 rows) ---")
    print(df_raw.head().to_string())

    print(f"\n[INFO] Persisting raw telemetry → {RAW_OUT}")
    df_raw.to_csv(RAW_OUT)
    print("[DONE]")
