# Applied Data Science Architectures

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Machine Learning](https://img.shields.io/badge/ML-scikit--learn-orange?logo=scikit-learn&logoColor=white)
![Healthcare AI](https://img.shields.io/badge/Healthcare-AI-red?logo=heart&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

**Alex Domingues Batista, PhD**  
**Data Scientist | Python • ML • Experimental Analytics • Healthcare AI • Time-Series**  
📍 **Based in Germany** | 🇪🇺 Full EU Working Rights

> 📖 **New to this repo?** Check out [CONTRIBUTING.md](CONTRIBUTING.md) for repository structure and guidelines.

A collection of end-to-end data science architectures spanning **healthcare/clinical AI**, **predictive maintenance**, **sensor analytics & concept drift**, **experimental data QA**, **customer intelligence**, and **cheminformatics** — built with a validation-first mindset emphasizing data quality, reproducibility, and explainability across diverse domains.

---

## 📋 Table of Contents

- [Quick Project Navigation](#-quick-project-navigation)
- [Start Here (2 minutes)](#start-here-2-minutes)
- [Quick Summary](#quick-summary)
- [Germany Experience](#germany-experience-20202024)
- [Featured Projects](#featured-projects)
- [Technical Skills](#technical-skills)
- [Repository Structure](#repository-structure)
- [Contact](#-lets-connect)

---

## 📂 Business Impact & Technical Complexity

| Project | Business Output | Technical Complexity | Domain |
|---------|-----------------|----------------------|--------|
| 🌾 **[Sugarcane Weed Predictor](Sugarcane%20Canopy%20Weed%20Emergence%20Predictor/)** | Optimizes ag-chemical supply chains and maximizes yields via precision herbicide scheduling. | XGBoost, Sub-canopy Physics, FastAPI | Agritech / Precision Ag |
| 🩸 **[GuardianCGM](GuardianCGM/)** | Enables preventative clinical intervention, improving patient outcomes through predictive analytics. | Regulatory-aware ML (Clarke Grid), Uncertainty Qty. | Clinical AI / MedTech |
| 📊 **[Gas Sensor Drift](gas-sensor-drift-monitoring/)** | Prevents silent model failures in industrial IoT arrays, reducing unplanned maintenance costs. | Statistical drift tracking, Windowed adaptive retraining | Concept Drift / IoT |
| 🔬 **[Metabolomics Biomarker](metabolomics-biomarker-discovery/)** | Accelerates diagnostic assay development, significantly reducing R&D costs by prioritizing key features. | Sparse linear models (Lasso), Network SHAP interpretation | Diagnostics / LC-MS |
| 🧪 **[ToxPred](toxpred/)** | Filters non-viable drug candidates early in the pipeline, saving costly wet-lab synthesis resources. | Molecule parsing (RDKit), ADMET profiling, Model Inference | Cheminformatics |
| ⚡ **[Electrocatalyst Data Analysis](electrocatalyst-data-analysis/)** | Detects experimental artifacts to accelerate self-driving laboratory loops. | Domain-grounded anomaly detection, Physical chemistries | Materials Science |

---

## Start here (2 minutes)
- **🌾 Sugarcane Canopy Weed Emergence Predictor** — microclimate-driven herbicide decision intelligence for Brazilian sugarcane  
  → `./Sugarcane Canopy Weed Emergence Predictor/`
- **🩸 GuardianCGM: Clinical Glucose Prediction AI** — regulatory-aware MedTech pipeline with Clarke Error Grid validation + SHAP explainability  
  → `./GuardianCGM/`
- **📊 Gas Sensor Drift & Calibration Transfer** — concept drift + adaptive retraining to maintain performance over time  
  → `./gas-sensor-drift-monitoring/`
- **🔬 LC–MS Metabolomics Biomarker Prioritization** — explainable ML + feature selection for diagnostics-style data  
  → `./metabolomics-biomarker-discovery/`
- **⚡ Electrocatalyst Data Analysis** — experimental data QA, anomaly detection, multi-campaign learning for materials discovery  
  → `./electrocatalyst-data-analysis/`

---

## Technical Overview
**10+ years** working with analytical measurement systems and experimental data; now building modern DS/ML solutions in Python/SQL across diverse domains.

**Core strengths**
- **ML & analytics:** scikit-learn, SHAP, feature engineering, model evaluation, uncertainty-aware thinking
- **Production-ready pipelines:** FastAPI deployment, regulatory validation (Clarke Error Grid), explainability (SHAP)
- **Sensor/time-series:** drift monitoring, anomaly detection, degradation patterns, predictive maintenance, early-warning signals
- **Healthcare & diagnostics:** clinical AI (CGM forecasting), high-dimensional assay pipelines (LC–MS), biomarker discovery
- **Experimental data analysis:** PhD background (50+ publications), high-throughput campaign QA, artifact identification, multi-campaign learning
- **Business analytics:** customer segmentation, CLV modeling, statistical validation (ANOVA), churn prevention insights
- **Scientific communication:** translating complex analysis into actionable insights for technical and non-technical stakeholders



**Software Engineering & Compliance (EU/Germany Focus):**
- **Regulatory Awareness:** EU AI Act, Medical Device Regulation (EU-MDR), and DIN EN ISO 13485 workflows.
- **Data Privacy:** Designed pipelines with explicit DSGVO/GDPR compliance and data minimization principles.
- **Code Quality:** strict PEP8 compliance, modular architectures, and formal NumPy docstrings.
- **Reproducibility:** Containerized environments (Docker), requirements management, and explicit random seeds.
- **Testing & QA:** Validation checks, data quality assertions, and unit-testing mentalities to ensure robust deployments.

---

## Scientific Background
- **Humboldt Research Fellow — Ulm University (2020–2021)**  
  Applied ML-guided optimization in biosensing research; published results in peer-reviewed work.
- **Research Group Leader — Hahn-Schickard Institute (2022–2024)**  
  Led an applied diagnostics R&D team; collaborated with engineering and research stakeholders; built analytics workflows for sensor performance monitoring, data quality, and comparison across conditions.

**Languages:** Portuguese (Native) | English (Full Professional) | German (B1 — Actively pursuing B2)

---

## System Architectures

### 1) 🌾 Sugarcane Canopy Weed Emergence Predictor (Agritech)
**Objective:** Predict emergence timing of competitive weeds in sugarcane using microclimate telemetry and agronomically-grounded feature engineering.

**Highlights**
- Engineered physical features (Hydrothermal Time, Vapour Pressure Deficit, Canopy Density) based on NASA POWER microclimate data.
- Built a robust XGBoost classifier using strict time-series cross-validation (5-fold rolling window) to prevent data leakage.
- Designed comprehensive SHAP analytics (global, dot, and waterfall plots) to deliver transparent, actionable insights for field advisors.
- Deployed the model as an end-to-end containerised FastAPI service ready for precision agriculture integrations.

**Tech stack:** Python, XGBoost, SHAP, FastAPI, Docker, scikit-learn  
**Project:** `./Sugarcane Canopy Weed Emergence Predictor/`

---

### 2) 🩸 GuardianCGM: Clinical Glucose Prediction AI (MedTech)
**Objective:** Build a regulatory-aware, end-to-end pipeline for 30-minute glucose forecasting using Continuous Glucose Monitoring (CGM) data.

**Highlights**
- **Chemistry + Data Science:** Signal processing with Savitzky-Golay filtering and electrochemistry context from PhD background.
- **Clinical Validation:** Clarke Error Grid analysis showing **99.4% Zone A** (Zones A+B commonly used in CGM evaluation).
- **Model Comparison:** Tested baseline/Linear Regression/Random Forest; achieved **RMSE 4.81 mg/dL** (38.9% improvement over baseline).
- **Uncertainty Quantification:** 95% prediction intervals with **94.7% calibration coverage** for risk-aware clinical decisions.
- **Explainability:** SHAP analysis for regulatory transparency and clinical trust.
- **Production Ready:** FastAPI REST API example with Pydantic validation and async support.

**Tech stack:** Python, SciPy, scikit-learn, SHAP, FastAPI, Plotly  
**Project:** `./GuardianCGM/`

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

### 4) 🔬 Explainable AI for Biomarker Prioritization (LC–MS Metabolomics)
**Objective:** Build an interpretable ML pipeline to prioritize candidate biomarkers from high-dimensional assay data.

**Highlights**
- Preprocessed and analyzed a cachexia metabolomics dataset; performed QC with PCA and volcano-style inspection.
- Benchmarked sparse linear models (feature selection) vs tree-based models (non-linearity).
- Used **SHAP** to interpret drivers and communicate which features matter and why.
- Emphasis on **reproducibility** and **stakeholder-friendly interpretation** (what to validate next and how to reduce scope).

**Tech stack:** Python, Pandas, scikit-learn, SHAP, Seaborn  
**Project:** `./metabolomics-biomarker-discovery/`

---

### 5) 🧪 ToxPred AI: ADMET Screening Platform (Cheminformatics)
**Objective:** Accelerate early-stage drug discovery by predicting molecular properties before synthesis.

**Highlights**
- **Solubility prediction:** Random Forest on Delaney (ESOL) dataset (R² ≈ 0.87).
- **Toxicity screening:** Classifier on ClinTox dataset (76% accuracy) to flag clinical trial failures.
- **BBB permeability:** Predicts CNS penetration for neuro-drug discovery (ROC-AUC ≈ 0.85).
- **Structural intelligence:** Uses Morgan Fingerprints (ECFP4, 2048-bit) for substructure analysis.
- **Streamlit web app:** Interactive deployment with real-time predictions and Lipinski Rule of Five.

**Tech stack:** Python, RDKit, scikit-learn, Streamlit, DeepChem datasets  
**Project:** `./toxpred/`

---

### 6) ⚡ Electrocatalyst Data Analysis: Experimental Campaign Intelligence
**Objective:** Demonstrate end-to-end analysis of high-throughput screening campaigns with experimental data QA and multi-campaign learning.

**Highlights**
- **Experimental data QA:** Systematic identification of artifacts (reference drift, temperature effects, electrode fouling).
- **Multi-campaign learning:** Track understanding evolution across campaigns - how success rates improve as protocols are refined.
- **Anomaly detection:** Statistical methods with domain context to distinguish signal from noise.
- **Scientific communication:** Executive digests, lab feedback reports, ML feature recommendations.
- **Domain expertise applied:** PhD-level knowledge used to interpret patterns and guide analysis.

**Tech stack:** Python, Pandas, scikit-learn, SciPy (statistical tests), Seaborn  
**Project:** `./electrocatalyst-data-analysis/`

---

## Technical skills
**Programming & tools:** Python (Pandas, NumPy, scikit-learn, SHAP, SciPy), SQL, Git/GitHub, Jupyter, VS Code, Linux/Bash  
**ML & analytics:** regression/classification, tree-based models, SVM, cross-validation, explainability (SHAP), anomaly detection, PCA  
**Time-series & sensors:** rolling/trend features, drift monitoring, stability analysis, QA/QC mindset  
**Electrochemistry & materials:** electrode kinetics, cyclic voltammetry, impedance spectroscopy, catalyst characterization, experimental artifact identification  
**Cheminformatics:** RDKit (molecular descriptors, fingerprints), exposure to pymatgen/ASE for materials science  
**Domain:** analytical instrumentation (LC–MS, GC–MS, HPLC, spectroscopy, electrochemical workstations), sensor systems, diagnostics, high-throughput screening

---

## Repository structure
```text
data-science-portfolio/
├── README.md                                        # This file - portfolio overview
├── Sugarcane Canopy Weed Emergence Predictor/       # 🌾 Agritech spatial weed prediction
│   ├── 01_data_ingestion.py
│   ├── 02_feature_engineering.py
│   ├── 03_model_training.py
│   ├── app/main.py
│   ├── README.md
│   └── requirements.txt
├── GuardianCGM/                                     # 🩸 MedTech glucose prediction
│   ├── 01_Signal_Processing_and_EDA.ipynb
│   ├── 02_Model_Training_and_Clinical_Evaluation.ipynb
│   ├── 03_Model_Deployment_and_Inference.ipynb
│   ├── data/processed_biomarkers.csv
│   ├── models/glucose_rf_v1.pkl
│   ├── README.md
│   └── requirements.txt
├── gas-sensor-drift-monitoring/                     # 📊 Concept drift analytics
│   ├── 01_visualizing_the_drift.ipynb
│   ├── 02_model_decay_analysis.ipynb
│   ├── 03_adaptive_calibration.ipynb
│   ├── README.md
│   └── requirements.txt
├── metabolomics-biomarker-discovery/                # 🔬 Diagnostics biomarker ML
│   ├── 01_chemometric_eda.ipynb
│   ├── 02_biomarker_ml.ipynb
│   ├── 03_shap_interpretation.ipynb
│   ├── README.md
│   └── requirements.txt
├── toxpred/                                         # 🧪 Cheminformatics ADMET app
│   ├── toxpred_app.py
│   ├── step_models.py
│   ├── README.md
│   └── requirements.txt
└── electrocatalyst-data-analysis/                   # ⚡ Materials discovery campaign analysis
    ├── 01_experimental_data_quality.ipynb
    ├── 02_campaign_comparison_learning.ipynb
    ├── 03_scientific_communication.ipynb
    ├── data/campaign_*.csv
    ├── README.md
    └── requirements.txt
```

**Note:** Large data files (gas-sensor batches) are gitignored. For local reproduction, see individual project READMEs for data source links.

**Repository Information:**
- 📖 **[CONTRIBUTING.md](CONTRIBUTING.md)** - Project structure guidelines and development workflow
- 📄 **[LICENSE](LICENSE)** - MIT License

**Getting Started:**
1. **Browse projects**: Use the [Quick Project Navigation](#-quick-project-navigation) table above
2. **Clone the repository**: `git clone https://github.com/alexdbatista/data-science-portfolio.git`
3. **Navigate to a project**: `cd data-science-portfolio/[project-name]/`
4. **Follow project README**: Each project has its own setup instructions and requirements.txt
5. **Root-level files** (`requirements.txt`, `packages.txt`): Used for Streamlit Cloud deployment of ToxPred app

---

## Author

**Alex Domingues Batista, PhD**
- **Dr. rer. nat. (equivalent)** - PhD, Universidade de São Paulo (USP)
- **Humboldt Research Fellow** - Alexander von Humboldt Foundation (2020-2021)
- **Former Professor** (UFU, Brazil, 2015-2021) 
- **Research Group Leader** (Hahn-Schickard, Germany, 2022-2024)
- **50 peer-reviewed publications** | h-index: 18 | 1,266 citations

**Languages:** Portuguese (Native) | English (Full Professional) | German (B1 — Actively pursuing B2)