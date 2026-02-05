# Data Science Portfolio

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Machine Learning](https://img.shields.io/badge/ML-scikit--learn-orange?logo=scikit-learn&logoColor=white)
![Healthcare AI](https://img.shields.io/badge/Healthcare-AI-red?logo=heart&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

**Alex Domingues Batista, PhD**  
**Data Scientist | Python • ML • Experimental Analytics • Healthcare AI • Time-Series**

> 📖 **New to this repo?** Check out [CONTRIBUTING.md](CONTRIBUTING.md) for repository structure and guidelines.

Portfolio of end-to-end data science projects spanning **healthcare/clinical AI**, **predictive maintenance**, **sensor analytics & concept drift**, **experimental data QA**, **customer intelligence**, and **cheminformatics** — built with a validation-first mindset emphasizing data quality, reproducibility, and explainability across diverse domains.

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

## 📂 Quick Project Navigation

| Project | Domain | Key Tech | Documentation |
|---------|--------|----------|---------------|
| 🩸 **GuardianCGM** | Clinical AI / MedTech | CGM, SHAP, FastAPI, Regulatory | [README](GuardianCGM/) |
| 🔧 **NASA Turbofan RUL** | Predictive Maintenance | Time-series, Gradient Boosting | [README](nasa-turbofan-predictive-maintenance/) |
| 📊 **Gas Sensor Drift** | Concept Drift / IoT | PCA, Adaptive Learning | [README](gas-sensor-drift-monitoring/) |
| 🔬 **Metabolomics Biomarker** | Diagnostics / LC-MS | SHAP, Feature Selection | [README](metabolomics-biomarker-discovery/) |
| 🛒 **Retail Segmentation** | Customer Analytics | RFM, K-Means, CLV | [README](retail-customer-segmentation/) |
| 🧪 **ToxPred** | Cheminformatics | RDKit, Streamlit, ADMET | [README](toxpred/) |
| ⚡ **Electrocatalyst Data Analysis** | Materials Science | Campaign QA, Multi-campaign Learning | [README](electrocatalyst-data-analysis/) |

---

## Start here (2 minutes)
- **🩸 GuardianCGM: Clinical Glucose Prediction AI** — regulatory-aware MedTech pipeline with Clarke Error Grid validation + SHAP explainability  
  → `./GuardianCGM/`
- **🔧 Predictive Maintenance (NASA Turbofan RUL)** — leakage-safe time-series evaluation + interpretable monitoring outputs  
  → `./nasa-turbofan-predictive-maintenance/`
- **📊 Gas Sensor Drift & Calibration Transfer** — concept drift + adaptive retraining to maintain performance over time  
  → `./gas-sensor-drift-monitoring/`
- **🔬 LC–MS Metabolomics Biomarker Prioritization** — explainable ML + feature selection for diagnostics-style data  
  → `./metabolomics-biomarker-discovery/`
- **⚡ Electrocatalyst Data Analysis** — experimental data QA, anomaly detection, multi-campaign learning for materials discovery  
  → `./electrocatalyst-data-analysis/`

---

## Quick summary
**10+ years** working with analytical measurement systems and experimental data; now building modern DS/ML solutions in Python/SQL across diverse domains.

**Core strengths**
- **ML & analytics:** scikit-learn, SHAP, feature engineering, model evaluation, uncertainty-aware thinking
- **Production-ready pipelines:** FastAPI deployment, regulatory validation (Clarke Error Grid), explainability (SHAP)
- **Sensor/time-series:** drift monitoring, anomaly detection, degradation patterns, predictive maintenance, early-warning signals
- **Healthcare & diagnostics:** clinical AI (CGM forecasting), high-dimensional assay pipelines (LC–MS), biomarker discovery
- **Experimental data analysis:** PhD background (50+ publications), high-throughput campaign QA, artifact identification, multi-campaign learning
- **Business analytics:** customer segmentation, CLV modeling, statistical validation (ANOVA), churn prevention insights
- **Scientific communication:** translating complex analysis into actionable insights for technical and non-technical stakeholders

**What I can deliver in 30–60 days:** a data-quality baseline, an interpretable model with validation metrics, and a dashboard/report your team can use.

**🩺 **Healthcare & MedTech** (Siemens Healthineers, Roche, Abbott, Philips)
- 🏭 **Industry 4.0 / IIoT** (Siemens, Bosch, SAP, ABB)
- 🧬 **Life Sciences & Pharma** (Bayer, Merck, Sartorius, Bruker, Thermo Fisher)
- 🌱 **Clean Energy & Materials** (Dunia, National Labs, Battery/Catalyst R&D)
- 📊 **Data-Driven Enterprises** (Consulting, Analytics, Retail Techealthineers, Bruker, Thermo Fisher)
- 🏭 **Industry 4.0 / IIoT** (Siemens, Bosch, SAP)

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

### 1) ⚡ Electrocatalyst Data Analysis: Experimental Campaign Intelligence (Materials Discovery)
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

### 3) 🔬 Explainable AI for Biomarker Prioritization (LC–MS Metabolomics)
**Objective:** Build an interpretable ML pipeline to prioritize candidate biomarkers from high-dimensional assay data.

**Highlights**
- Preprocessed and analyzed a cachexia metabolomics dataset; performed QC with PCA and volcano-style inspection.
- Benchmarked sparse linear models (feature selection) vs tree-based models (non-linearity).
- Used **SHAP** to interpret drivers and communicate which features matter and why.
- Emphasis on **reproducibility** and **stakeholder-friendly interpretation** (what to validate next and how to reduce scope).

**Tech stack:** Python, Pandas, scikit-learn, SHAP, Seaborn  
**Project:** `./metabolomics-biomarker-discovery/`

---

### 4) 📊 Gas Sensor Drift & Calibration Transfer (Concept Drift)
**Objective:** Quantify long-term drift and evaluate strategies to keep sensor models stable over time.

**Highlights**
- Analyzed a longitudinal sensor dataset and visualized drift behavior with PCA and performance decay curves.
- Measured how static models degrade as sensors age (concept drift).
- Implemented adaptive calibration / windowed retraining strategies to maintain performance under drift.
- Clear takeaway: how to design a practical monitoring + retraining policy for long-lived sensor deployments.

**Tech stack:** Python, scikit-learn (PCA, tree-based models), drift analysis  
**Project:** `./gas-sensor-drift-monitoring/`
2) 🔧 NASA Turbofan Predictive Maintenance (RUL)
**Objective:** Predict Remaining Useful Life (RUL) from multivariate engine sensor time-series and create monitoring-ready outputs.

**Highlights**
- Processed run-to-failure sensor time series from multiple engines (NASA C-MAPSS).
- Engineered rolling/trend features to capture degradation patterns.
- Trained and evaluated models with **engine-level splitting** to prevent data leakage.
- Achieved strong RUL predictive performance and translated outputs into early-warning/maintenance planning signals.

**Tech stack:** Python, time-series feature engineering, Gradient Boosting / Random Forest  
**Project:** `./nasa-turbofan-predictive-maintenance/`

---
5ject:** `./nasa-turbofan-predictive-maintenance/`

---

### 6) 🛒 RFM Customer Segmentation (Retail Analytics)
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

### 7) ⚡ Electrocatalyst Data Analysis: Experimental Campaign Intelligence
**Objective:** Demonstrate end-to-end analysis of high-throughput screening campaigns with experimental data QA and multi-campaign learning.

**Highlights**
- **Experimental data QA:** Systematic identification of artifacts (reference drift, temperature effects, electrode fouling).
- **Multi-campaign learning:** Track understanding evolution across campaigns - how success rates improve as protocols are refined.
- **Anomaly detection:** Statistical methods with domain context to distinguish signal from noise.
- **Scientific communication:** Executive digests, lab feedback reports, ML feature recommendations.
- **Domain expertise applied:** PhD-level knowledge used to interpret patterns and guide analysis.

**Tech stack:** Python, Pandas, scikit-learn, SciPy (statistical tests), Seaborn  
**Target audience:** Materials discovery, catalyst/battery R&D, high-throughput experimental labs  
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
├── README.md                                     # This file - portfolio overviewFastAPI, Jupyter, VS Code, Linux/Bash  
**ML & analytics:** regression/classification, tree-based models, SVM, cross-validation, explainability (SHAP), anomaly detection, PCA, statistical testing  
**Time-series & sensors:** rolling/trend features, drift monitoring, predictive maintenance, RUL forecasting, stability analysis  
**Healthcare & diagnostics:** clinical validation metrics (Clarke Error Grid), biomarker discovery, high-dimensional assay data (LC–MS), QC/QA workflows  
**Business analytics:** customer segmentation (RFM, K-Means), CLV modeling, ANOVA validation, churn analysis  
**Domain expertise:** analytical instrumentation (LC–MS, HPLC, spectroscopy, electrochemical systems), sensor systems, high-throughput screening  
**Cheminformatics:** RDKit (molecular descriptors, fingerprints), ADMET prediction, exposure to pymatgen/ASE
│   └── human_cachexia.csv
├── electrocatalyst-data-analysis/                  # ⚡ NEW: Materials discovery campaign analysis
│   ├── 01_experimental_data_quality.ipynb
│   ├── 02_campaign_comparison_learning.ipynb
│   ├── 03_scientific_communication.ipynb
│   ├── data/campaign_*.csv
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

**Getting Started:**
1. **Browse projects**: Use the [Quick Project Navigation](#-quick-project-navigation) table above
2. **Clone the repository**: `git clone https://github.com/alexdbatista/data-science-portfolio.git`
3. **Navigate to a project**: `cd data-science-portfolio/[project-name]/`
4. **Follow project README**: Each project has its own setup instructions and requirements.txt
5. **Root-level files** (`requirements.txt`, `packages.txt`): Used for Streamlit Cloud deployment of ToxPred app

---

## 📫 Let's Connect

**Seeking:** Chemical Data Scientist / Materials Informatics / ML Engineer roles

**Target Industries:** 
- 🌱 **Clean Energy & Materials Discovery** (Dunia, Materials Project, Acceleration Consortium, National Labs)
- 🔋 **Battery & Energy Storage** (QuantumScape, Solid Power, CATL, Northvolt)
- ⚗️ **Catalysis & Chemical Manufacturing** (BASF, Johnson Matthey, Clariant, Evonik)
- 🧬 **Life Sciences & Pharma** (Roche, Bayer, Merck, Sartorius)
- 🔬 **Diagnostics & Medical Devices** (Siemens Healthineers, Bruker, Thermo Fisher)
- 🏭 **Industry 4.0 / IIoT** (Siemens, Bosch, SAP)

**Based in:** Germany (2020-2024) | Open to relocation within Germany, Netherlands, Denmark, Switzerland
Data Scientist / ML Engineer / Analytics roles across industries

**Target Industries:** 
- 🩺 **Healthcare & MedTech** (Siemens Healthineers, Roche, Abbott, Philips)
- 🏭 **Industry 4.0 / IIoT / Manufacturing** (Siemens, Bosch, SAP, ABB)
- 🧬 **Life Sciences & Pharma** (Bayer, Merck, Sartorius, Bruker, Thermo Fisher)
- 🌱 **Clean Energy & Materials** (Dunia, National Labs, Battery/Catalyst R&D)
- 📊 **Data-Driven Enterprises** (Tech, Consulting, Analytics, Retail Tech
*For German employers familiar with academic titles:*

- **Dr. rer. nat. (equivalent)** - PhD, Universidade de São Paulo (USP)
- **Humboldt Research Fellow** - Alexander von Humboldt Foundation (2020-2021)
- **Former Professor** (UFU, Brazil, 2015-2021) - 6 years teaching & research
- **Research Group Leader** (Hahn-Schickard, Germany, 2022-2024)
- **50 peer-reviewed publications** | h-index: 18 | 1,266 citations

**Languages:** Portuguese (Native) | English (Fluent) | German (B1 Intermediate)

