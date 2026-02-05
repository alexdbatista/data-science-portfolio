# Data Science Portfolio
**Alex Domingues Batista, PhD**  
**Digital Biomarker Data Scientist | CGM & Health Time-Series | Python • ML • Regulatory-aware Validation**

> 📖 **New to this repo?** Check out [CONTRIBUTING.md](CONTRIBUTING.md) for repository structure and guidelines.

Portfolio of end-to-end projects focused on **healthcare/clinical AI**, **sensor/measurement data**, **concept drift**, **predictive maintenance**, and **diagnostics analytics** — built with a validation-first mindset (clinical safety, reproducibility, explainability).

---

## Start here (2 minutes)
- **GuardianCGM: Clinical Glucose Prediction AI** — regulatory-aware MedTech pipeline with Clarke Error Grid validation + SHAP explainability  
  → `./GuardianCGM/`
- **Gas Sensor Drift & Calibration Transfer** — concept drift + adaptive retraining to maintain performance over time  
  → `./gas-sensor-drift-monitoring/`
- **Predictive Maintenance (NASA Turbofan RUL)** — leakage-safe evaluation + interpretable monitoring outputs  
  → `./nasa-turbofan-predictive-maintenance/`
- **LC–MS Metabolomics Biomarker Prioritization** — explainable ML + feature selection for diagnostics-style data  
  → `./metabolomics-biomarker-discovery/`

---

## Quick summary
**10+ years** working with analytical measurement systems and experimental data; now building modern DS/ML solutions in Python/SQL.

**Core strengths**
- **ML & analytics:** scikit-learn, SHAP, feature engineering, model evaluation, uncertainty-aware thinking
- **Sensor/time-series:** drift monitoring, anomaly detection, degradation patterns, early-warning signals
- **Diagnostics & lab data:** high-dimensional assay pipelines (e.g., LC–MS), QC thinking and reproducibility
- **Collaboration:** translating complex analysis into actionable insights for engineers and stakeholders

**What I can deliver in 30–60 days:** a data-quality + drift monitoring baseline, an interpretable model, and a simple dashboard/report your team can use.

**Target industries:** Digital Health • Diabetes Care • SaMD / Medical Device Analytics • Instrumentation • Diagnostics • Life Sciences • Manufacturing • Industry 4.0 / IIoT

**Software engineering practices:**
- **Version control:** Git workflow with clear commit messages and branch management
- **Code quality:** PEP8 style compliance, modular architecture, reusable functions
- **Reproducibility:** Requirements files, virtual environments, documented dependencies
- **Documentation:** Inline comments, docstrings, and comprehensive README files
- **Testing mindset:** Validation checks, data quality assertions, and reproducible results

---

## Germany experience (2020–2024)
- **Humboldt Research Fellow — Ulm University (2020–2021)**  
  Applied ML-guided optimization in biosensing research; published results in peer-reviewed work.
- **Research Group Leader — Hahn-Schickard Institute (2022–2024)**  
  Led an applied diagnostics R&D team; collaborated with engineering and research stakeholders; built analytics workflows for sensor performance monitoring, data quality, and comparison across conditions.

**Languages:** Portuguese (Native) • English (Fluent) • German (B1)

---

## Featured projects

### 1) 🩸 GuardianCGM: Clinical Glucose Prediction AI (MedTech/Pharma)
**Objective:** Build a regulatory-aware, end-to-end pipeline for 30-minute glucose forecasting using Continuous Glucose Monitoring (CGM) data.

**Highlights**
- **Chemistry + Data Science:** Signal processing with Savitzky-Golay filtering and electrochemistry context from PhD background.
- **Clinical Validation:** Clarke Error Grid analysis showing **99.4% Zone A** (Zones A+B commonly used in CGM evaluation).
- **Model Comparison:** Tested baseline/Linear Regression/Random Forest; achieved **RMSE 4.81 mg/dL** (38.9% improvement over baseline).
- **Uncertainty Quantification:** 95% prediction intervals with **94.7% calibration coverage** for risk-aware clinical decisions.
- **Explainability:** SHAP analysis for regulatory transparency and clinical trust.
- **Production Ready:** FastAPI REST API example with Pydantic validation and async support.

**Tech stack:** Python, SciPy, scikit-learn, SHAP, FastAPI, Plotly  
**Target audience:** MedTech, pharma, digital health roles (Roche, Siemens Healthineers, Abbott)  
**Project:** `./GuardianCGM/`

---

### 2) 🔬 Explainable AI for Biomarker Prioritization (LC–MS Metabolomics)
**Objective:** Build an interpretable ML pipeline to prioritize candidate biomarkers from high-dimensional assay data.

**Highlights**
- Preprocessed and analyzed a cachexia metabolomics dataset; performed QC with PCA and volcano-style inspection.
- Benchmarked sparse linear models (feature selection) vs tree-based models (non-linearity).
- Used **SHAP** to interpret drivers and communicate which features matter and why.
- Emphasis on **reproducibility** and **stakeholder-friendly interpretation** (what to validate next and how to reduce scope).

**Tech stack:** Python, Pandas, scikit-learn, SHAP, Seaborn  
**Project:** `./metabolomics-biomarker-discovery/`

---

### 3) 📊 Gas Sensor Drift & Calibration Transfer (Concept Drift)
**Objective:** Quantify long-term drift and evaluate strategies to keep sensor models stable over time.

**Highlights**
- Analyzed a longitudinal sensor dataset and visualized drift behavior with PCA and performance decay curves.
- Measured how static models degrade as sensors age (concept drift).
- Implemented adaptive calibration / windowed retraining strategies to maintain performance under drift.
- Clear takeaway: how to design a practical monitoring + retraining policy for long-lived sensor deployments.

**Tech stack:** Python, scikit-learn (PCA, tree-based models), drift analysis  
**Project:** `./gas-sensor-drift-monitoring/`

---

### 4) 🔧 NASA Turbofan Predictive Maintenance (RUL)
**Objective:** Predict Remaining Useful Life (RUL) from multivariate engine sensor time-series and create monitoring-ready outputs.

**Highlights**
- Processed run-to-failure sensor time series from multiple engines (NASA C-MAPSS).
- Engineered rolling/trend features to capture degradation patterns.
- Trained and evaluated models with **engine-level splitting** to prevent data leakage.
- Achieved strong RUL predictive performance and translated outputs into early-warning/maintenance planning signals.

**Tech stack:** Python, time-series feature engineering, Gradient Boosting / Random Forest  
**Project:** `./nasa-turbofan-predictive-maintenance/`

---

### 5) 🛒 RFM Customer Segmentation (Retail Analytics)
**Objective:** Create actionable customer segments with statistical validation and business-ready insights.

**Highlights**
- Segmented **4,372 customers** from UCI Online Retail dataset (~540k transactions) into **5 groups**.
- **Revenue concentration:** Top segment contributes ~60% of revenue.
- **Statistical validation:** ANOVA p < 0.001 confirms segments are significantly different.
- **Method comparison:** 70-80% agreement between RFM scoring and K-Means clustering.
- **Stability testing:** >80% assignment consistency when changing parameters (quartiles → quintiles).
- **CLV insight:** Champions £6,732 vs Hibernating £222 (~30× difference).

**Tech stack:** Python, Pandas, scikit-learn, SciPy (ANOVA), Seaborn  
**Business value:** Retention prioritization, lifecycle marketing, churn prevention  
**Project:** `./retail-customer-segmentation/`

---

### 6) 🧪 ToxPred AI: ADMET Screening Platform (Cheminformatics)
**Objective:** Accelerate early-stage drug discovery by predicting molecular properties before synthesis.

**Highlights**
- **Solubility prediction:** Random Forest on Delaney (ESOL) dataset (R² ≈ 0.87).
- **Toxicity screening:** Classifier on ClinTox dataset (76% accuracy) to flag clinical trial failures.
- **BBB permeability:** Predicts CNS penetration for neuro-drug discovery (ROC-AUC ≈ 0.85).
- **Structural intelligence:** Uses Morgan Fingerprints (ECFP4, 2048-bit) for substructure analysis.
- **Streamlit web app:** Interactive deployment with real-time predictions and Lipinski Rule of Five.

**Tech stack:** Python, RDKit, scikit-learn, Streamlit, DeepChem datasets  
**Target audience:** Pharma R&D, computational chemistry, medicinal chemistry  
**Project:** `./toxpred/`

---

## Technical skills
**Programming & tools:** Python (Pandas, NumPy, scikit-learn, SHAP), SQL, Git/GitHub, Jupyter, VS Code, Linux/Bash  
**ML & analytics:** regression/classification, tree-based models, SVM, cross-validation, explainability (SHAP), anomaly detection  
**Time-series & sensors:** rolling/trend features, drift monitoring, stability analysis, QA/QC mindset  
**Domain:** analytical instrumentation (LC–MS, GC–MS, HPLC, spectroscopy), sensor systems, diagnostics contexts

---

## Repository structure
```text
data-science-portfolio/
├── README.md                                     # This file - portfolio overview
├── CONTRIBUTING.md                               # Repository structure and guidelines
├── LICENSE                                       # MIT License
├── requirements.txt                              # Streamlit Cloud deployment dependencies
├── packages.txt                                  # System packages for cloud deployment
├── data/
│   └── human_cachexia.csv
├── GuardianCGM/                                     # 🩸 MedTech glucose prediction
│   ├── 01_Signal_Processing_and_EDA.ipynb
│   ├── 02_Model_Training_and_Clinical_Evaluation.ipynb
│   ├── 03_Model_Deployment_and_Inference.ipynb
│   ├── data/processed_biomarkers.csv
│   ├── models/glucose_rf_v1.pkl
│   ├── README.md
│   └── requirements.txt
├── metabolomics-biomarker-discovery/                # 🔬 Diagnostics biomarker ML
│   ├── 01_chemometric_eda.ipynb
│   ├── 02_biomarker_ml.ipynb
│   ├── 03_shap_interpretation.ipynb
│   ├── README.md
│   └── requirements.txt
├── gas-sensor-drift-monitoring/                     # 📊 Concept drift analytics
│   ├── 01_visualizing_the_drift.ipynb
│   ├── 02_model_decay_analysis.ipynb
│   ├── 03_adaptive_calibration.ipynb
│   ├── README.md
│   └── requirements.txt
├── nasa-turbofan-predictive-maintenance/            # 🔧 Time-series RUL prediction
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_quality_and_drift.ipynb
│   ├── 03_predictive_modeling.ipynb
│   └── README.md
├── retail-customer-segmentation/                    # 🛒 RFM + K-Means segmentation
│   ├── RFM_Customer_Segmentation.ipynb
│   ├── README.md
│   └── requirements.txt
└── toxpred/                                         # 🧪 Cheminformatics ADMET app
    ├── toxpred_app.py
    ├── setup_models.py
    ├── README.md
    └── requirements.txt
```

**Note:** Large data files (gas-sensor batches, turbofan datasets, retail data) are gitignored. For local reproduction, see individual project READMEs for data source links.

**Repository Information:**
- 📖 **[CONTRIBUTING.md](CONTRIBUTING.md)** - Project structure guidelines and development workflow
- 📄 **[LICENSE](LICENSE)** - MIT License

---

## 📫 Let's Connect

**Seeking:** Data Scientist / ML Engineer roles in Germany

**Target Industries:** 
- 🧬 Life Sciences & Pharma (Roche, Bayer, Merck, Sartorius)
- 🔬 Diagnostics & Medical Devices (Siemens Healthineers, Bruker, Thermo Fisher)
- 🏭 Industry 4.0 / IIoT (Siemens, Bosch, SAP)
- 🧪 Analytical Instrumentation (PerkinElmer, Agilent)

**Based in:** Germany (2020-2024) | Open to relocation within Germany, Netherlands, Denmark

**Contact:**
- 📧 **Email:** [alexdbatista@gmail.com](mailto:alexdbatista@gmail.com)
- 🔗 **LinkedIn:** [linkedin.com/in/alexdbatista](https://linkedin.com/in/alexdbatista)
- 💻 **GitHub:** [github.com/alexdbatista](https://github.com/alexdbatista)

---

## 🎓 Academic Credentials Summary
*For German employers familiar with academic titles:*

- **Dr. rer. nat. (equivalent)** - PhD, Universidade de São Paulo (USP)
- **Humboldt Research Fellow** - Alexander von Humboldt Foundation (2020-2021)
- **Former Professor** (UFU, Brazil, 2015-2021) - 6 years teaching & research
- **Research Group Leader** (Hahn-Schickard, Germany, 2022-2024)
- **50 peer-reviewed publications** | h-index: 18 | 1,266 citations

**Languages:** Portuguese (Native) | English (Fluent) | German (B1 Intermediate)

