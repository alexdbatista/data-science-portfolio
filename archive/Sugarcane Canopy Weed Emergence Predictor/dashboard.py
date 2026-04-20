"""
dashboard.py
============
Sugarcane Canopy Weed Emergence Predictor — Streamlit Dashboard

A premium, dark-mode agronomic intelligence dashboard featuring:
  • Live zone-level emergence risk prediction via the REST API
  • Historical telemetry visualisation (NASA POWER data)
  • SHAP explainability charts loaded from reports/
  • Model performance metrics panel
  • Interactive 14-day risk timeline

Run:
    streamlit run dashboard.py
"""

import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st
from plotly.subplots import make_subplots

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
ROOT        = Path(__file__).parent
DATA_PATH   = ROOT / "data" / "features.csv"
RAW_PATH    = ROOT / "data" / "nasa_power_raw.csv"
METRICS_PATH = ROOT / "reports" / "model_metrics.json"
SHAP_GLOBAL  = ROOT / "reports" / "shap_global_importance.png"
SHAP_DOT     = ROOT / "reports" / "shap_dot_plot.png"
SHAP_WATER   = ROOT / "reports" / "shap_waterfall_peak_day.png"
CONFUSION    = ROOT / "reports" / "confusion_matrix.png"

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Sugarcane Weed Emergence Predictor",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Custom CSS — dark agronomic theme
# ---------------------------------------------------------------------------
st.markdown("""
<style>
  /* ---- Global ---- */
  html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', sans-serif;
  }
  .stApp {
    background: linear-gradient(135deg, #0a0f0a 0%, #0d1a0e 50%, #0a0f0a 100%);
    color: #e8f5e9;
  }

  /* ---- Sidebar ---- */
  [data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1f10 0%, #071208 100%);
    border-right: 1px solid #1b4d20;
  }
  [data-testid="stSidebar"] .block-container { padding-top: 1rem; }
  [data-testid="stSidebar"] label, [data-testid="stSidebar"] .stMarkdown p {
    color: #a5d6a7 !important;
  }

  /* ---- Metrics ---- */
  [data-testid="metric-container"] {
    background: linear-gradient(135deg, #102712 0%, #0d1f10 100%);
    border: 1px solid #2e7d32;
    border-radius: 12px;
    padding: 1rem 1.2rem !important;
    box-shadow: 0 4px 20px rgba(46, 125, 50, 0.15);
  }
  [data-testid="metric-container"] label {
    color: #81c784 !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.06em;
    text-transform: uppercase;
  }
  [data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #e8f5e9 !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
  }
  [data-testid="metric-container"] [data-testid="stMetricDelta"] {
    color: #66bb6a !important;
  }

  /* ---- Cards ---- */
  .card {
    background: linear-gradient(135deg, #102712 0%, #0d1f10 100%);
    border: 1px solid #2e7d32;
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4);
  }
  .card-title {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #66bb6a;
    margin-bottom: 0.5rem;
  }

  /* ---- Risk badge ---- */
  .risk-badge-low      { background:#1b5e20; color:#a5d6a7; border:1px solid #2e7d32; }
  .risk-badge-moderate { background:#4a3500; color:#ffcc80; border:1px solid #ff8f00; }
  .risk-badge-high     { background:#4a0000; color:#ef9a9a; border:1px solid #c62828; }
  .risk-badge {
    display:inline-block; border-radius:8px; padding:0.35rem 1rem;
    font-size:1.3rem; font-weight:700; letter-spacing:0.05em;
  }

  /* ---- Section headers ---- */
  h1 { color: #a5d6a7 !important; font-weight: 800 !important; }
  h2, h3 { color: #81c784 !important; }

  /* ---- Inputs ---- */
  [data-testid="stSlider"] .stMarkdown { color: #c8e6c9 !important; }
  .stSlider > label { color: #a5d6a7 !important; }
  [data-baseweb="input"] input { background: #0d1f10 !important; color: #e8f5e9 !important; }

  /* ---- Tabs ---- */
  .stTabs [data-baseweb="tab-list"] {
    background: #102712;
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
  }
  .stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #81c784;
    border-radius: 8px;
    font-weight: 600;
    letter-spacing: 0.04em;
  }
  .stTabs [aria-selected="true"] {
    background: #1b5e20 !important;
    color: #e8f5e9 !important;
  }

  /* ---- Divider ---- */
  hr { border-color: #1b4d20 !important; }

  /* ---- Scrollbar ---- */
  ::-webkit-scrollbar { width: 6px; }
  ::-webkit-scrollbar-track { background: #0a0f0a; }
  ::-webkit-scrollbar-thumb { background: #2e7d32; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

@st.cache_data(ttl=300)
def load_features():
    if DATA_PATH.exists():
        return pd.read_csv(DATA_PATH, index_col="Date", parse_dates=True)
    return None


@st.cache_data(ttl=300)
def load_raw():
    if RAW_PATH.exists():
        return pd.read_csv(RAW_PATH, index_col="Date", parse_dates=True)
    return None


@st.cache_data(ttl=300)
def load_metrics():
    if METRICS_PATH.exists():
        with open(METRICS_PATH) as f:
            return json.load(f)
    return {}


def risk_color(level: str):
    return {"LOW": "#4caf50", "MODERATE": "#ff9800", "HIGH": "#f44336"}.get(level, "#9e9e9e")


def risk_badge_class(level: str):
    return {"LOW": "risk-badge-low", "MODERATE": "risk-badge-moderate",
            "HIGH": "risk-badge-high"}.get(level, "")


def api_predict(payload: dict):
    try:
        r = requests.post(f"{API_URL}/predict", json=payload, timeout=5)
        r.raise_for_status()
        return r.json(), None
    except Exception as e:
        return None, str(e)


def api_health():
    try:
        r = requests.get(f"{API_URL}/health", timeout=3)
        return r.json()
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Sidebar — zone configurator
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🌾 Zone Configurator")
    st.markdown("---")

    zone_id = st.text_input("Zone ID", value="zone_A3", label_visibility="visible")

    st.markdown("#### 🌡️ Thermal")
    gdd          = st.slider("Growing Degree Days (°C·day)", 0.0, 30.0, 12.4, 0.1)
    gdd_cumsum   = st.slider("Cumulative GDD", 0.0, 800.0, 430.0, 5.0)
    t2m_mean_3d  = st.slider("3-day mean temp (°C)", 15.0, 40.0, 28.2, 0.1)
    t2m_mean_7d  = st.slider("7-day mean temp (°C)", 15.0, 40.0, 27.8, 0.1)
    t2m_mean_14d = st.slider("14-day mean temp (°C)", 15.0, 40.0, 27.5, 0.1)

    st.markdown("#### 💧 Hydraulic")
    soil_moisture_mm = st.slider("Soil moisture (mm)", 0.0, 100.0, 45.0, 1.0)
    htt_cumsum       = st.slider("Hydrothermal Time (HTT)", 0.0, 80.0, 22.5, 0.5)
    precip_sum_3d    = st.slider("3-day precip (mm)", 0.0, 60.0, 8.5, 0.5)
    precip_sum_7d    = st.slider("7-day precip (mm)", 0.0, 120.0, 22.0, 1.0)
    precip_sum_14d   = st.slider("14-day precip (mm)", 0.0, 200.0, 55.0, 1.0)

    st.markdown("#### 🌬️ Atmospheric")
    vpd_kpa      = st.slider("VPD (kPa)", 0.0, 4.0, 1.8, 0.05)
    vpd_mean_3d  = st.slider("3-day mean VPD", 0.0, 4.0, 1.6, 0.05)
    vpd_mean_7d  = st.slider("7-day mean VPD", 0.0, 4.0, 1.7, 0.05)
    vpd_mean_14d = st.slider("14-day mean VPD", 0.0, 4.0, 1.75, 0.05)
    rh2m_mean_3d  = st.slider("3-day mean RH (%)", 20.0, 100.0, 74.0, 1.0)
    rh2m_mean_7d  = st.slider("7-day mean RH (%)", 20.0, 100.0, 72.5, 1.0)
    rh2m_mean_14d = st.slider("14-day mean RH (%)", 20.0, 100.0, 71.0, 1.0)

    st.markdown("#### ☀️ Solar")
    canopy_density    = st.slider("Canopy closure (0–1)", 0.0, 1.0, 0.72, 0.01)
    solar_rad_7d_sum  = st.slider("7-day solar radiation (MJ/m²)", 0.0, 200.0, 120.0, 1.0)
    sub_canopy_rad    = st.slider("Sub-canopy irradiance (MJ/m²/day)", 0.0, 30.0, 4.2, 0.1)

    st.markdown("---")
    run_predict = st.button("⚡ Run Prediction", use_container_width=True, type="primary")


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
col_title, col_status = st.columns([4, 1])
with col_title:
    st.markdown("""
    <h1 style="margin-bottom:0; font-size:2rem;">
      🌿 Sugarcane Canopy Weed Emergence Predictor
    </h1>
    <p style="color:#66bb6a; margin-top:0.2rem; font-size:0.95rem; letter-spacing:0.03em;">
      <em>Brachiaria decumbens</em> · Ribeirão Preto, São Paulo · XGBoost + SHAP
    </p>
    """, unsafe_allow_html=True)

with col_status:
    health = api_health()
    if health and health.get("status") == "healthy":
        st.markdown("""
        <div style="text-align:right; margin-top:0.8rem;">
          <span style="background:#1b5e20;border:1px solid #2e7d32;border-radius:20px;
                       padding:0.3rem 0.8rem;font-size:0.8rem;color:#a5d6a7;font-weight:600;">
            ● API LIVE
          </span>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align:right; margin-top:0.8rem;">
          <span style="background:#4a0000;border:1px solid #c62828;border-radius:20px;
                       padding:0.3rem 0.8rem;font-size:0.8rem;color:#ef9a9a;font-weight:600;">
            ● API OFFLINE
          </span>
        </div>""", unsafe_allow_html=True)

st.markdown("---")


# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🎯 Live Prediction", "📈 Telemetry Timeline", "🧠 Model Explainability", "📊 Model Performance"
])


# ============================================================
# TAB 1: LIVE PREDICTION
# ============================================================
with tab1:
    payload = {
        "zone_id": zone_id,
        "gdd": gdd, "gdd_cumsum": gdd_cumsum,
        "vpd_kpa": vpd_kpa, "canopy_density": canopy_density,
        "soil_moisture_mm": soil_moisture_mm, "htt_cumsum": htt_cumsum,
        "precip_sum_3d": precip_sum_3d, "t2m_mean_3d": t2m_mean_3d,
        "rh2m_mean_3d": rh2m_mean_3d, "vpd_mean_3d": vpd_mean_3d,
        "precip_sum_7d": precip_sum_7d, "t2m_mean_7d": t2m_mean_7d,
        "rh2m_mean_7d": rh2m_mean_7d, "vpd_mean_7d": vpd_mean_7d,
        "precip_sum_14d": precip_sum_14d, "t2m_mean_14d": t2m_mean_14d,
        "rh2m_mean_14d": rh2m_mean_14d, "vpd_mean_14d": vpd_mean_14d,
        "solar_rad_7d_sum": solar_rad_7d_sum, "sub_canopy_rad": sub_canopy_rad,
    }

    # Auto-predict on load or when button clicked
    if run_predict or "last_result" not in st.session_state:
        result, err = api_predict(payload)
        if result:
            st.session_state["last_result"] = result
            st.session_state["last_payload"] = payload
        else:
            st.session_state["last_result"] = None
            st.session_state["last_err"] = err

    result = st.session_state.get("last_result")
    err    = st.session_state.get("last_err")

    if result:
        prob   = result["emergence_probability"]
        level  = result["risk_level"]
        drivers = result["top_drivers"]
        reco   = result["recommendation"]

        # ---- Top KPI row ----
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Emergence Probability", f"{prob*100:.1f}%",
                      delta=f"{(prob - 0.5)*100:+.1f}pp vs neutral")
        with col2:
            st.metric("Risk Level", level)
        with col3:
            st.metric("Zone", result.get("zone_id", "—"))
        with col4:
            st.metric("HTT Accumulated", f"{htt_cumsum:.1f} MPa·°C·d",
                      delta="threshold 38" if htt_cumsum < 38 else "⚠ above threshold")

        st.markdown("---")

        col_gauge, col_drivers = st.columns([1, 1])

        # ---- Gauge chart ----
        with col_gauge:
            st.markdown("##### Emergence Probability Gauge")
            gauge_color = risk_color(level)
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=prob * 100,
                delta={"reference": 50, "valueformat": ".1f", "suffix": "pp",
                       "increasing": {"color": "#f44336"},
                       "decreasing": {"color": "#4caf50"}},
                title={"text": f"<b>{level} RISK</b>", "font": {"color": gauge_color, "size": 18}},
                gauge={
                    "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#4a7c5a",
                             "tickfont": {"color": "#a5d6a7"}},
                    "bar": {"color": gauge_color, "thickness": 0.25},
                    "bgcolor": "#0d1f10",
                    "bordercolor": "#1b4d20",
                    "steps": [
                        {"range": [0, 35],  "color": "#0a2c0a"},
                        {"range": [35, 65], "color": "#3a2800"},
                        {"range": [65, 100],"color": "#3a0000"},
                    ],
                    "threshold": {"line": {"color": "#ffffff", "width": 3},
                                  "thickness": 0.8, "value": prob * 100},
                },
                number={"suffix": "%", "font": {"color": "#e8f5e9", "size": 40}},
            ))
            fig_gauge.update_layout(
                paper_bgcolor="#0d1f10", font_color="#e8f5e9",
                height=300, margin=dict(t=40, b=10, l=20, r=20),
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

            # Recommendation card
            badge_cls = risk_badge_class(level)
            icon = {"LOW": "✅", "MODERATE": "⚠️", "HIGH": "🚨"}.get(level, "")
            st.markdown(f"""
            <div class="card">
              <div class="card-title">Field Recommendation</div>
              <span class="risk-badge {badge_cls}">{icon} {level}</span>
              <p style="margin-top:0.8rem; color:#c8e6c9; line-height:1.6;">{reco}</p>
            </div>""", unsafe_allow_html=True)

        # ---- SHAP drivers ----
        with col_drivers:
            st.markdown("##### SHAP Feature Drivers")
            feat_names  = [d["feature"] for d in drivers]
            shap_vals   = [d["shap_value"] for d in drivers]
            directions  = [d["direction"] for d in drivers]
            colors      = ["#f44336" if v > 0 else "#4caf50" for v in shap_vals]

            fig_shap = go.Figure(go.Bar(
                x=shap_vals,
                y=feat_names,
                orientation="h",
                marker_color=colors,
                marker_line_width=0,
                text=[f"{v:+.3f}" for v in shap_vals],
                textposition="outside",
                textfont={"color": "#e8f5e9", "size": 12},
            ))
            fig_shap.add_vline(x=0, line_color="#4a7c5a", line_width=1.5, line_dash="dot")
            fig_shap.update_layout(
                paper_bgcolor="#0d1f10", plot_bgcolor="#0d1a0e",
                font_color="#e8f5e9", height=300,
                margin=dict(t=20, b=20, l=10, r=60),
                xaxis=dict(title="SHAP value (log-odds)", gridcolor="#1b3a1f",
                           zerolinecolor="#2e7d32"),
                yaxis=dict(autorange="reversed", gridcolor="#1b3a1f"),
            )
            st.plotly_chart(fig_shap, use_container_width=True)

            # Driver cards
            for d in drivers[:3]:
                icon2 = "🔺" if d["direction"] == "increases_risk" else "🔻"
                col_a = "#ef9a9a" if d["direction"] == "increases_risk" else "#a5d6a7"
                st.markdown(f"""
                <div style="background:#0d1f10;border:1px solid #1b4d20;border-radius:8px;
                            padding:0.5rem 0.8rem;margin-bottom:0.4rem;display:flex;
                            justify-content:space-between;align-items:center;">
                  <span style="color:#c8e6c9;font-size:0.85rem;">{icon2} <b>{d['feature']}</b></span>
                  <span style="color:{col_a};font-weight:700;font-size:0.9rem;">
                    {d['shap_value']:+.4f}
                  </span>
                </div>""", unsafe_allow_html=True)

    elif err:
        st.error(f"❌ API Error: {err}")
        st.info("Make sure the API is running: `uvicorn app.main:app --port 8000`")

    # ---- Sensitivity sweep across soil moisture ----
    st.markdown("---")
    st.markdown("##### 📉 Sensitivity Analysis — Soil Moisture vs. Emergence Probability")
    sm_range = np.linspace(0, 100, 40)
    probs_sm = []
    for sm_val in sm_range:
        p = payload.copy()
        p["soil_moisture_mm"] = float(sm_val)
        res, _ = api_predict(p)
        probs_sm.append(res["emergence_probability"] if res else None)

    df_sens = pd.DataFrame({"soil_moisture_mm": sm_range, "probability": probs_sm}).dropna()
    fig_sens = px.line(df_sens, x="soil_moisture_mm", y="probability",
                       labels={"soil_moisture_mm": "Soil Moisture (mm)",
                                "probability": "Emergence Probability"},
                       template="plotly_dark",
                       color_discrete_sequence=["#4caf50"])
    fig_sens.add_hline(y=0.65, line_color="#f44336", line_dash="dash",
                       annotation_text="HIGH threshold", annotation_font_color="#ef9a9a")
    fig_sens.add_hline(y=0.35, line_color="#ff9800", line_dash="dash",
                       annotation_text="MODERATE threshold", annotation_font_color="#ffcc80")
    fig_sens.add_vline(x=soil_moisture_mm, line_color="#81c784", line_dash="dot",
                       annotation_text=f"Current: {soil_moisture_mm}mm",
                       annotation_font_color="#a5d6a7")
    fig_sens.update_layout(
        paper_bgcolor="#0d1f10", plot_bgcolor="#0a140b",
        font_color="#c8e6c9", height=280,
        margin=dict(t=20, b=20, l=20, r=20),
        xaxis=dict(gridcolor="#1b3a1f"), yaxis=dict(gridcolor="#1b3a1f"),
    )
    st.plotly_chart(fig_sens, use_container_width=True)


# ============================================================
# TAB 2: TELEMETRY TIMELINE
# ============================================================
with tab2:
    df_raw  = load_raw()
    df_feat = load_features()

    if df_raw is None or df_feat is None:
        st.warning("⚠️ Run the data pipeline first: `python 01_data_ingestion.py && python 02_feature_engineering.py`")
    else:
        st.markdown("##### 🌡️ NASA POWER Meteorological Telemetry — Ribeirão Preto, São Paulo")

        # Date filter
        date_min = df_raw.index.min().date()
        date_max = df_raw.index.max().date()
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            d_start = st.date_input("From", value=date_min, min_value=date_min, max_value=date_max)
        with col_d2:
            d_end   = st.date_input("To",   value=date_max, min_value=date_min, max_value=date_max)

        mask = (df_raw.index.date >= d_start) & (df_raw.index.date <= d_end)
        df_r = df_raw.loc[mask]
        df_f = df_feat.loc[mask]

        # ---- 4-panel telemetry ----
        fig_tele = make_subplots(
            rows=4, cols=1, shared_xaxes=True,
            subplot_titles=["Temperature (°C)", "Precipitation (mm)", "Relative Humidity (%)",
                            "Solar Irradiance (MJ/m²/day)"],
            vertical_spacing=0.07,
        )
        fig_tele.add_trace(go.Scatter(x=df_r.index, y=df_r["T2M"], name="T2M",
                                       line=dict(color="#ef9a9a", width=1.5)), row=1, col=1)
        fig_tele.add_trace(go.Bar(x=df_r.index, y=df_r["PRECTOTCORR"], name="Precip",
                                   marker_color="#64b5f6", opacity=0.8), row=2, col=1)
        fig_tele.add_trace(go.Scatter(x=df_r.index, y=df_r["RH2M"], name="RH2M",
                                       line=dict(color="#80cbc4", width=1.5),
                                       fill="tozeroy", fillcolor="rgba(128,203,196,0.1)"), row=3, col=1)
        fig_tele.add_trace(go.Scatter(x=df_r.index, y=df_r["ALLSKY_SFC_SW_DWN"], name="Solar Rad",
                                       line=dict(color="#fff176", width=1.5),
                                       fill="tozeroy", fillcolor="rgba(255,241,118,0.08)"), row=4, col=1)
        fig_tele.update_layout(
            paper_bgcolor="#0d1f10", plot_bgcolor="#0a140b",
            font_color="#c8e6c9", height=650, showlegend=False,
            margin=dict(t=40, b=20, l=60, r=20),
        )
        for i in range(1, 5):
            fig_tele.update_xaxes(gridcolor="#1b3a1f", row=i, col=1)
            fig_tele.update_yaxes(gridcolor="#1b3a1f", row=i, col=1)
        for ann in fig_tele.layout.annotations:
            ann.font.color = "#81c784"
        st.plotly_chart(fig_tele, use_container_width=True)

        # ---- Engineered features timeline ----
        st.markdown("---")
        st.markdown("##### 🧪 Engineered Agronomic Features")
        col_f1, col_f2 = st.columns(2)

        with col_f1:
            fig_htt = go.Figure()
            fig_htt.add_trace(go.Scatter(x=df_f.index, y=df_f["htt_cumsum"],
                                          name="Cumulative HTT", line=dict(color="#4caf50", width=2)))
            fig_htt.add_hline(y=38, line_color="#f44336", line_dash="dash",
                               annotation_text="50% Germination Threshold (38 MPa·°C·d)",
                               annotation_font_color="#ef9a9a")
            fig_htt.update_layout(
                title="Hydrothermal Time Accumulation",
                paper_bgcolor="#0d1f10", plot_bgcolor="#0a140b",
                font_color="#c8e6c9", height=300, margin=dict(t=40, b=20, l=50, r=10),
                xaxis=dict(gridcolor="#1b3a1f"), yaxis=dict(gridcolor="#1b3a1f",
                                                             title="HTT (MPa·°C·day)"),
            )
            st.plotly_chart(fig_htt, use_container_width=True)

        with col_f2:
            fig_canopy = go.Figure()
            fig_canopy.add_trace(go.Scatter(x=df_f.index, y=df_f["canopy_density"],
                                             name="Canopy Density", fill="tozeroy",
                                             fillcolor="rgba(76,175,80,0.15)",
                                             line=dict(color="#66bb6a", width=2)))
            fig_canopy.add_trace(go.Scatter(x=df_f.index, y=df_f["sub_canopy_rad"],
                                             name="Sub-canopy Irradiance",
                                             line=dict(color="#fff176", width=1.5),
                                             yaxis="y2"))
            fig_canopy.update_layout(
                title="Canopy Closure & Sub-canopy Light",
                paper_bgcolor="#0d1f10", plot_bgcolor="#0a140b",
                font_color="#c8e6c9", height=300, margin=dict(t=40, b=20, l=50, r=60),
                xaxis=dict(gridcolor="#1b3a1f"),
                yaxis=dict(gridcolor="#1b3a1f", title="Canopy Density (0–1)",
                            range=[0, 1.2]),
                yaxis2=dict(title="Irradiance (MJ/m²/day)", overlaying="y",
                             side="right", gridcolor="#1b3a1f"),
                legend=dict(bgcolor="#0d1f10", bordercolor="#2e7d32"),
            )
            st.plotly_chart(fig_canopy, use_container_width=True)

        # ---- Emergence risk heatmap ----
        st.markdown("---")
        st.markdown("##### 🗓️ Emergence Risk Calendar")
        df_cal = df_f[["emergence_risk_14d"]].copy()
        df_cal["month"] = df_cal.index.month
        df_cal["day"]   = df_cal.index.day
        df_cal["year"]  = df_cal.index.year

        for year_val in df_cal["year"].unique():
            df_y = df_cal[df_cal["year"] == year_val]
            pivot = df_y.pivot_table(index="month", columns="day",
                                      values="emergence_risk_14d", aggfunc="mean")
            fig_cal = px.imshow(
                pivot, color_continuous_scale=["#0a2c0a", "#f44336"],
                zmin=0, zmax=1, aspect="auto",
                labels={"x": "Day of Month", "y": "Month", "color": "Risk"},
                title=f"Emergence Risk Heatmap — {year_val}",
            )
            fig_cal.update_layout(
                paper_bgcolor="#0d1f10", font_color="#c8e6c9",
                height=280, margin=dict(t=40, b=20, l=40, r=20),
                coloraxis_colorbar=dict(tickfont=dict(color="#c8e6c9")),
            )
            st.plotly_chart(fig_cal, use_container_width=True)


# ============================================================
# TAB 3: MODEL EXPLAINABILITY
# ============================================================
with tab3:
    st.markdown("##### 🧠 SHAP Explainability — Understanding What Drives the Prediction")
    st.markdown("""
    <p style="color:#a5d6a7; line-height:1.7;">
    SHAP (SHapley Additive exPlanations) decomposes each prediction into per-feature contributions.
    Red bars push emergence risk higher; blue bars push it lower.
    </p>
    """, unsafe_allow_html=True)

    col_s1, col_s2 = st.columns(2)

    with col_s1:
        if SHAP_GLOBAL.exists():
            st.markdown('<div class="card-title">Global Feature Importance (Bar)</div>',
                        unsafe_allow_html=True)
            st.image(str(SHAP_GLOBAL), use_container_width=True)

    with col_s2:
        if SHAP_DOT.exists():
            st.markdown('<div class="card-title">SHAP Value Distribution (Dot Plot)</div>',
                        unsafe_allow_html=True)
            st.image(str(SHAP_DOT), use_container_width=True)

    if SHAP_WATER.exists():
        st.markdown("---")
        st.markdown('<div class="card-title">Waterfall Plot — Peak Risk Day Prediction</div>',
                    unsafe_allow_html=True)
        st.image(str(SHAP_WATER), use_container_width=True)

    if CONFUSION.exists():
        st.markdown("---")
        col_cm, col_interp = st.columns([1, 1])
        with col_cm:
            st.markdown('<div class="card-title">Confusion Matrix — Test Set</div>',
                        unsafe_allow_html=True)
            st.image(str(CONFUSION), use_container_width=True)
        with col_interp:
            st.markdown("""
            <div class="card">
              <div class="card-title">Interpretation</div>
              <p style="color:#c8e6c9; line-height:1.7; font-size:0.9rem;">
              The model achieves <b>100% recall</b> on the emergence class — meaning
              zero genuine weed emergence windows are missed. This is the critical
              property for a herbicide advisory system: a missed alert is far more
              costly than a false alarm.<br><br>
              The 31% false alarm rate on non-risk days is acceptable — an unnecessary
              herbicide inspection costs far less than a missed pre-emergence window.
              </p>
            </div>""", unsafe_allow_html=True)

    if not any([SHAP_GLOBAL.exists(), SHAP_DOT.exists(), SHAP_WATER.exists()]):
        st.warning("⚠️ SHAP reports not found. Run `python 03_model_training.py` to generate them.")


# ============================================================
# TAB 4: MODEL PERFORMANCE
# ============================================================
with tab4:
    st.markdown("##### 📊 Model Performance Summary")
    metrics = load_metrics()

    if metrics:
        # KPI row
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Test ROC-AUC",      f"{metrics.get('test_roc_auc', 0):.4f}",
                  delta="vs 0.5 baseline")
        c2.metric("Test Avg Precision", f"{metrics.get('test_avg_precision', 0):.4f}")
        c3.metric("CV ROC-AUC (mean)",
                  f"{metrics.get('cv_roc_auc_mean', 0):.4f}",
                  delta=f"±{metrics.get('cv_roc_auc_std', 0):.4f}")
        c4.metric("CV Avg Precision",   f"{metrics.get('cv_ap_mean', 0):.4f}")

        st.markdown("---")

        # Bar chart of key metrics
        metric_names = ["ROC-AUC (Test)", "Avg Precision (Test)",
                        "ROC-AUC (CV)", "Avg Precision (CV)"]
        metric_vals  = [
            metrics.get("test_roc_auc", 0),
            metrics.get("test_avg_precision", 0),
            metrics.get("cv_roc_auc_mean", 0),
            metrics.get("cv_ap_mean", 0),
        ]
        fig_metrics = go.Figure(go.Bar(
            x=metric_names, y=metric_vals,
            marker_color=["#4caf50", "#66bb6a", "#81c784", "#a5d6a7"],
            text=[f"{v:.4f}" for v in metric_vals],
            textposition="outside",
            textfont=dict(color="#e8f5e9"),
        ))
        fig_metrics.add_hline(y=0.9, line_color="#fff176", line_dash="dash",
                              annotation_text="0.90 target",
                              annotation_font_color="#fff176")
        fig_metrics.update_layout(
            paper_bgcolor="#0d1f10", plot_bgcolor="#0a140b",
            font_color="#c8e6c9", height=350,
            yaxis=dict(range=[0, 1.1], gridcolor="#1b3a1f", title="Score"),
            xaxis=dict(gridcolor="#1b3a1f"),
            margin=dict(t=20, b=20, l=40, r=20),
        )
        st.plotly_chart(fig_metrics, use_container_width=True)

        # Technical summary card
        st.markdown("""
        <div class="card">
          <div class="card-title">Model Architecture</div>
          <table style="width:100%; border-collapse:collapse; color:#c8e6c9; font-size:0.88rem;">
            <tr style="border-bottom:1px solid #1b4d20;">
              <th style="text-align:left; padding:0.4rem 0.6rem; color:#66bb6a;">Parameter</th>
              <th style="text-align:left; padding:0.4rem 0.6rem; color:#66bb6a;">Value</th>
            </tr>
            <tr><td style="padding:0.35rem 0.6rem;">Algorithm</td><td>XGBoost Classifier</td></tr>
            <tr style="background:#0a1a0b;">
              <td style="padding:0.35rem 0.6rem;">Estimators</td><td>300</td></tr>
            <tr><td style="padding:0.35rem 0.6rem;">Max depth</td><td>5</td></tr>
            <tr style="background:#0a1a0b;">
              <td style="padding:0.35rem 0.6rem;">Learning rate</td><td>0.05</td></tr>
            <tr><td style="padding:0.35rem 0.6rem;">Subsample</td><td>0.8</td></tr>
            <tr style="background:#0a1a0b;">
              <td style="padding:0.35rem 0.6rem;">Class imbalance</td>
              <td>scale_pos_weight (neg/pos ratio)</td></tr>
            <tr><td style="padding:0.35rem 0.6rem;">Validation</td>
              <td>TimeSeriesSplit (5-fold rolling window)</td></tr>
            <tr style="background:#0a1a0b;">
              <td style="padding:0.35rem 0.6rem;">Split strategy</td>
              <td>Year boundary: 2021 train / 2022 test</td></tr>
            <tr><td style="padding:0.35rem 0.6rem;">Features</td>
              <td>20 agronomic features (HTT, GDD, VPD, canopy, soil moisture, rolling stats)</td></tr>
          </table>
        </div>""", unsafe_allow_html=True)
    else:
        st.warning("⚠️ No metrics found. Run `python 03_model_training.py` to generate them.")

# ---- Footer ----
st.markdown("---")
st.markdown("""
<p style="text-align:center; color:#2e7d32; font-size:0.78rem; letter-spacing:0.05em;">
  Sugarcane Canopy Weed Emergence Predictor · Ribeirão Preto, SP · 
  NASA POWER · XGBoost · SHAP · FastAPI · Docker
</p>
""", unsafe_allow_html=True)
