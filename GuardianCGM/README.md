
# 🩸 GuardianCGM: Predictive Glucose Monitoring AI

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Pandas](https://img.shields.io/badge/Data_Science-Pandas-orange)
![Scikit-Learn](https://img.shields.io/badge/Machine_Learning-Scikit--Learn-yellow)
![Status](https://img.shields.io/badge/Status-Portfolio_Ready-brightgreen)

**GuardianCGM** is an end-to-end, regulatory-aware data science pipeline for forecasting blood glucose levels using Continuous Glucose Monitoring (CGM) data. It combines advanced signal processing, robust machine learning, and explainability to deliver clinically meaningful, auditable predictions—demonstrating best practices for MedTech and pharma applications.

> **Designed for MedTech, pharma, and digital health roles in Germany and Europe.**

> **📌 Note:** Some interactive Plotly visualizations in notebook 01 may not render on GitHub's notebook viewer. For full visualization support, please:
> - Clone the repository and run notebooks locally in VS Code or Jupyter
> - Or view via [nbviewer](https://nbviewer.org/) for better rendering
> - All analytical figures (Clarke Grid, SHAP plots, model comparisons) in notebooks 02-03 display correctly as static images

**Key Features:**
- **Clinical-grade signal processing:** Savitzky-Golay filtering with chemistry/electrochemistry context
- **Advanced feature engineering:** Velocity, acceleration, volatility, and metabolic memory biomarkers
- **Comprehensive model evaluation:** Baseline comparison showing 38.9% RMSE improvement
- **Feature importance analysis:** Quantitative ranking of predictive biomarkers
- **Uncertainty quantification:** 95% prediction intervals with calibration validation
- **Clinical safety validation:** Clarke Error Grid analysis (99.4% Zone A on synthetic data)
- **Explainable AI:** SHAP force plots and summary visualizations for clinical transparency
- **Production-ready deployment:** FastAPI REST API example with Pydantic validation
- **Full traceability:** Chronological splits, audit logs, and regulatory context


## 🔬 Methodology & Pipeline

The project is structured as a modular, three-stage pipeline:

### 1. Signal Processing & Feature Engineering
- **Data Simulation:** Realistic, synthetic CGM data with physiological oscillations and sensor noise
- **Chemistry Context:** Electrochemical sensor principles and analytical chemistry insights
- **Signal Smoothing:** Savitzky-Golay filter (polynomial order 2, window 11) for denoising while preserving clinical features
- **Biomarker Extraction:**
    - Velocity (rate of change in mg/dL/min)
    - Acceleration (change in velocity)
    - Volatility (1-hour rolling standard deviation)
    - Metabolic memory (15m, 30m, 60m lagged values)
- **Data Quality:** Outlier detection, missing value checks, and audit trail
- **Output:** 846 samples with 10 engineered features exported to CSV

### 2. Model Training, Evaluation & Clinical Validation
- **Chronological Split:** 80/20 train-test with strict temporal ordering to prevent data leakage
- **Model Comparison Framework:**
    - Baseline (persistence model): RMSE 7.87 mg/dL
    - Linear Regression: RMSE 4.98 mg/dL
    - Random Forest (100 trees): **RMSE 4.81 mg/dL** (38.9% improvement over baseline)
- **Feature Importance Analysis:** Quantitative ranking showing `glucose_smooth` as dominant feature (87.7% importance)
- **Uncertainty Quantification:**
    - 95% prediction intervals using Random Forest ensemble variance
    - Mean uncertainty: 4.26 mg/dL
    - Calibration validation: 94.7% coverage (target 95%)
- **Clinical Safety Validation:**
    - **Clarke Error Grid:** 99.4% Zone A, 0.6% Zone B (100% clinically safe)
    - Exceeds FDA target of >95% in Zones A+B
    - Full zone-by-zone breakdown and visualization
- **Explainability:** SHAP summary plots, force plots, and feature impact analysis for regulatory transparency
- **Model Persistence:** Saved to `models/glucose_rf_v1.pkl` with joblib

### 3. Deployment & Real-Time Inference
- **Model Loading:** Joblib-based loading with version tracking and error handling
- **Batch Inference Pipeline:**
    - Dynamic feature extraction matching training pipeline
    - Clinical zone classification (hypoglycemia <70, target 70-180, hyperglycemia >180)
    - Uncertainty ribbons showing 95% confidence intervals
- **Production API Example:**
    - **FastAPI REST endpoint** with async support
    - Pydantic schemas for input validation
    - Health checks and model metadata endpoints
    - Error handling and logging middleware
- **Explainability:** SHAP summary plots for batch predictions showing feature contributions
- **Visualization:** Dual-panel plots (glucose predictions + velocity analysis) with clinical zones
- **Integration Ready:** Docker deployment notes, cloud scaling considerations


## 🛠️ Tech Stack

- **Language:** Python 3.13.5
- **Data Manipulation:** Pandas, NumPy
- **Signal Processing:** SciPy (Savitzky-Golay filter)
- **Visualization:** Plotly (interactive), Matplotlib, Seaborn
- **Machine Learning:** Scikit-Learn (Random Forest, Linear Regression)
- **Explainability:** SHAP (TreeExplainer)
- **Model Persistence:** Joblib
- **API Framework:** FastAPI with Pydantic validation
- **Development:** Jupyter Notebooks in VS Code
- **Environment:** Virtual environment (`guardian_env`)


## 📂 Project Structure

```
GuardianCGM/
├── 01_Signal_Processing_and_EDA.ipynb           # Data simulation, chemistry context, feature engineering
├── 02_Model_Training_and_Clinical_Evaluation.ipynb  # Model comparison, Clarke Grid, SHAP analysis
├── 03_Model_Deployment_and_Inference.ipynb      # Real-time inference, FastAPI deployment
├── data/
│   └── processed_biomarkers.csv                 # 846 samples × 10 features
├── models/
│   └── glucose_rf_v1.pkl                        # Trained Random Forest (100 trees)
└── README.md                                     # This file
```


## 🚀 How to Run

```bash
# 1. Create and activate virtual environment
python -m venv guardian_env
source guardian_env/bin/activate  # macOS/Linux
# guardian_env\Scripts\activate  # Windows

# 2. Install dependencies
pip install pandas numpy scipy scikit-learn matplotlib seaborn plotly shap joblib fastapi pydantic uvicorn

# 3. Run notebooks in order (in VS Code or Jupyter)
# Select guardian_env as kernel
```

**Notebook Execution Order:**
1. **01_Signal_Processing_and_EDA.ipynb** → Generates `data/processed_biomarkers.csv`
2. **02_Model_Training_and_Clinical_Evaluation.ipynb** → Trains model, saves to `models/glucose_rf_v1.pkl`
3. **03_Model_Deployment_and_Inference.ipynb** → Loads model, runs inference, displays FastAPI code

**Key Outputs to Review:**
- Feature importance bar chart (notebook 02)
- Clarke Error Grid with zone breakdown (notebook 02)
- Model comparison table (notebook 02)
- Uncertainty calibration plot (notebook 02)
- Real-time inference with clinical zones (notebook 03)
- SHAP explainability visualizations (notebooks 02 & 03)

> **For MedTech/pharma interviews:** Emphasize Clarke Error Grid results (99.4% Zone A), uncertainty quantification, SHAP explainability, and FastAPI production deployment.

---

## 📈 Results & Impact

| Metric | Value | Clinical Significance |
|--------|-------|----------------------|
| **RMSE** | 4.81 mg/dL | 38.9% improvement over baseline (7.87 mg/dL) |
| **R²** | 0.92 | High predictive accuracy on test set |
| **Clarke Zone A** | 99.4% | Clinically accurate predictions (target >95%) |
| **Clarke Zone B** | 0.6% | Benign errors with no clinical impact |
| **Zones C-E** | 0.0% | No dangerous predictions |
| **Uncertainty** | 4.26 mg/dL (mean) | Well-calibrated prediction intervals (94.7% coverage) |
| **Top Feature** | `glucose_smooth` | 87.7% feature importance (expected for 30-min horizon) |

**Clinical Validation:**
- ✅ **100% clinically safe** predictions (Clarke Zones A+B)
- ✅ Exceeds FDA guidance (>95% in zones A+B)
- ✅ Uncertainty quantification enables risk-aware decision making
- ✅ SHAP explainability provides audit trail for regulatory compliance

**Deployment Readiness:**
- ✅ FastAPI REST API with async support and input validation
- ✅ Model persistence and versioning with joblib
- ✅ Real-time inference pipeline with clinical zone classification
- ✅ Explainability visualizations for each prediction batch

## ⚖️ Regulatory & Clinical Context

**Compliance Alignment:**
- **MDR (EU 2017/745):** Clinical evaluation framework, risk management, traceability
- **FDA 21 CFR Part 820:** Design controls, validation, and documentation
- **ISO 13485:** Quality management for medical devices
- **GDPR:** Data privacy and security considerations for patient data

**Clinical Safety:**
- **Clarke Error Grid:** Gold standard for glucose prediction validation
- **Uncertainty Quantification:** Risk-aware predictions with confidence intervals
- **Explainability:** SHAP provides transparent, auditable feature contributions

**Traceability & Reproducibility:**
- Chronological data splits prevent look-ahead bias
- Random seeds ensure reproducible model training
- Environment versioning captured in notebooks
- Model artifacts saved with version identifiers

**Limitations & Next Steps:**
- Current results based on synthetic data (realistic but simplified)
- Real-world validation needed with FDA-approved CGM devices (Dexcom, Abbott FreeStyle Libre)
- Patient-specific calibration and personalization
- Prospective clinical trials for regulatory submission
- Edge case handling (sensor failures, rapid glucose changes)

**Chemistry/Analytical Science Perspective:**
- CGM sensors use glucose oxidase electrochemistry
- Signal processing accounts for sensor drift and lag time
- Feature engineering informed by glucose metabolism kinetics
- Analytical validation (precision, accuracy, LOD) required for clinical deployment

---

## 👤 Author

**Alex Domingues Batista, PhD**  
Academic leader, researcher, and educator with a proven track record in Chemistry, Sustainability, and Data Science. Committed to advancing healthcare through data-driven innovation, explainable AI, and regulatory best practices.

> _Ready to drive impactful solutions in MedTech and pharma._
