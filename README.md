# Data Science Portfolio
**Alex Domingues Batista, PhD**  
**Applied Data Scientist (Sensor/Time-Series) | Diagnostics & Instrumentation Analytics | Python • SQL • ML**

Portfolio of end-to-end projects focused on **measurement/sensor data**, **concept drift**, **predictive maintenance**, and **diagnostics-style analytics** — built with a validation-first mindset (noise, reproducibility, interpretability).

---

## Start here (2 minutes)
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

**Target industries:** Instrumentation • Diagnostics • Life Sciences • Manufacturing • Industry 4.0 / IIoT

---

## Germany experience (2020–2024)
- **Humboldt Research Fellow — Ulm University (2020–2021)**  
  Applied ML-guided optimization in biosensing research; published results in peer-reviewed work.
- **Research Group Leader — Hahn-Schickard Institute (2022–2024)**  
  Led an applied diagnostics R&D team; collaborated with engineering and research stakeholders; built analytics workflows for sensor performance monitoring, data quality, and comparison across conditions.

**Languages:** Portuguese (Native) • English (Fluent) • German (B1)

---

## Featured projects

### 1) Explainable AI for Biomarker Prioritization (LC–MS Metabolomics)
**Objective:** Build an interpretable ML pipeline to prioritize candidate biomarkers from high-dimensional assay data.

**Highlights**
- Preprocessed and analyzed a cachexia metabolomics dataset; performed QC with PCA and volcano-style inspection.
- Benchmarked sparse linear models (feature selection) vs tree-based models (non-linearity).
- Used **SHAP** to interpret drivers and communicate which features matter and why.
- Emphasis on **reproducibility** and **stakeholder-friendly interpretation** (what to validate next and how to reduce scope).

**Tech stack:** Python, Pandas, scikit-learn, SHAP, Seaborn  
**Project:** `./metabolomics-biomarker-discovery/`

---

### 2) Gas Sensor Drift & Calibration Transfer (Concept Drift)
**Objective:** Quantify long-term drift and evaluate strategies to keep sensor models stable over time.

**Highlights**
- Analyzed a longitudinal sensor dataset and visualized drift behavior with PCA and performance decay curves.
- Measured how static models degrade as sensors age (concept drift).
- Implemented adaptive calibration / windowed retraining strategies to maintain performance under drift.
- Clear takeaway: how to design a practical monitoring + retraining policy for long-lived sensor deployments.

**Tech stack:** Python, scikit-learn (PCA, tree-based models), drift analysis  
**Project:** `./gas-sensor-drift-monitoring/`

---

### 3) NASA Turbofan Predictive Maintenance (RUL)
**Objective:** Predict Remaining Useful Life (RUL) from multivariate engine sensor time-series and create monitoring-ready outputs.

**Highlights**
- Processed run-to-failure sensor time series from multiple engines (NASA C-MAPSS).
- Engineered rolling/trend features to capture degradation patterns.
- Trained and evaluated models with **engine-level splitting** to prevent data leakage.
- Achieved strong RUL predictive performance and translated outputs into early-warning/maintenance planning signals.

**Tech stack:** Python, time-series feature engineering, Gradient Boosting / Random Forest  
**Project:** `./nasa-turbofan-predictive-maintenance/`

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
├── README.md
├── data/
│   └── human_cachexia.csv
├── metabolomics-biomarker-discovery/
│   ├── 01_chemometric_eda.ipynb
│   ├── 02_biomarker_ml.ipynb
│   ├── 03_shap_interpretation.ipynb
│   ├── README.md
│   └── requirements.txt
├── gas-sensor-drift-monitoring/
│   ├── 01_visualizing_the_drift.ipynb
│   ├── 02_model_decay_analysis.ipynb
│   ├── 03_adaptive_calibration.ipynb
│   ├── README.md
│   └── requirements.txt
└── nasa-turbofan-predictive-maintenance/
    ├── 01_data_exploration.ipynb
    ├── 02_data_quality_and_drift.ipynb
    ├── 03_predictive_modeling.ipynb
    └── README.md
```

**Note:** Large data files (gas-sensor batches, turbofan datasets, retail data) are gitignored. For local reproduction, see individual project READMEs for data source links.
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
