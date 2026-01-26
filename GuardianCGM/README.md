
# 🩸 GuardianCGM: Predictive Glucose Monitoring AI

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Pandas](https://img.shields.io/badge/Data_Science-Pandas-orange)
![Scikit-Learn](https://img.shields.io/badge/Machine_Learning-Scikit--Learn-yellow)
![Status](https://img.shields.io/badge/Status-Portfolio_Ready-brightgreen)

**GuardianCGM** is an end-to-end, regulatory-aware data science pipeline for forecasting blood glucose levels using Continuous Glucose Monitoring (CGM) data. It combines advanced signal processing, robust machine learning, and explainability to deliver clinically meaningful, auditable predictions—demonstrating best practices for MedTech and pharma applications.

> **Designed for MedTech, pharma, and digital health roles in Germany and Europe.**

**Key Features:**
- Clinical-grade signal denoising and feature engineering
- Chronological data splitting to prevent leakage
- Robust Random Forest model with SHAP explainability
- Clinical safety validation (Clarke Error Grid)
- Real-time inference pipeline with alert logic
- Full traceability, audit logs, and regulatory context


## 🔬 Methodology & Pipeline

The project is structured as a modular, three-stage pipeline:

### 1. Signal Processing & Feature Engineering
- **Data Simulation:** Realistic, synthetic CGM data with physiological oscillations and sensor noise
- **Signal Smoothing:** Savitzky-Golay filter for denoising, preserving clinical features
- **Biomarker Extraction:**
    - Velocity (rate of change)
    - Acceleration (change in velocity)
    - Volatility (rolling SD)
    - Metabolic memory (lagged values)
- **Data Quality:** Outlier detection, missing value checks, and audit trail

### 2. Model Training, Evaluation & Explainability
- **Chronological Split:** Prevents data leakage, mimics real-world deployment
- **Model:** Random Forest Regressor (robust, interpretable)
- **Performance:**
    - RMSE ≈ 4.8 mg/dL, R² ≈ 0.92 (simulated data)
    - TimeSeriesSplit cross-validation for robustness
    - Baseline (last value) predictor for context
- **Explainability:** SHAP summary and force plots for clinical trust
- **Clinical Safety:** Clarke Error Grid analysis and plot
- **Reproducibility:** Audit log and environment info exported

### 3. Deployment & Real-Time Inference
- **Model Loading:** Error handling, versioning, and environment logging
- **Batch Inference:** Input validation, alert logic (hypo/hyper/borderline/normal)
- **Alert Visualization:** Bar plot and log export
- **Explainability:** SHAP for each batch
- **Integration Ready:** API, cloud, and mobile deployment notes


## 🛠️ Tech Stack

- **Language:** Python 3.9+
- **Data Manipulation:** Pandas, NumPy
- **Signal Processing:** SciPy
- **Visualization:** Plotly, Matplotlib, Seaborn
- **Machine Learning:** Scikit-Learn
- **Explainability:** SHAP
- **Notebooks:** Jupyter


## 📂 Project Structure

- `01_Signal_Processing_and_EDA.ipynb` — Data simulation, cleaning, filtering, feature engineering
- `02_Model_Training_and_Clinical_Evaluation.ipynb` — Model training, validation, explainability, clinical safety
- `03_Model_Deployment_and_Inference.ipynb` — Real-time inference, alerting, deployment notes
- `data/` — Processed biomarker data
- `models/` — Trained model artifacts and logs


## 🚀 How to Run

1. **Install dependencies** (see `requirements.txt`)
2. **Run notebooks in order:**
    - `01_Signal_Processing_and_EDA.ipynb` — Generate and process data
    - `02_Model_Training_and_Clinical_Evaluation.ipynb` — Train and validate model
    - `03_Model_Deployment_and_Inference.ipynb` — Run real-time inference and alerts
3. **Review outputs:**
    - Visualizations, model metrics, SHAP plots, and audit logs

> For MedTech/pharma interviews, highlight the pipeline’s clinical safety, explainability, and regulatory readiness.

---

## 📈 Results & Impact

- **Model Performance:** RMSE ≈ 4.8 mg/dL, R² ≈ 0.92 (simulated data)
- **Clinical Safety:** Most predictions in Clarke Error Grid zones A/B (safe/acceptable)
- **Explainability:** SHAP plots and feature importances support clinical trust
- **Deployment:** Real-time inference, alerting, and audit trail ready for integration

## ⚖️ Regulatory & Clinical Context

- **Traceability:** All steps are logged and auditable
- **Compliance:** Pipeline aligns with MDR (EU 2017/745), FDA, and GDPR principles
- **Reproducibility:** Environment info and random seeds are logged
- **Next Steps:** Validate on real CGM data, expand regulatory documentation, and explore patient-specific adaptation

---

## 👤 Author

**Alex Domingues Batista, PhD**  
Academic leader, researcher, and educator with a proven track record in Chemistry, Sustainability, and Data Science. Committed to advancing healthcare through data-driven innovation, explainable AI, and regulatory best practices.

> _Ready to drive impactful solutions in MedTech and pharma._
