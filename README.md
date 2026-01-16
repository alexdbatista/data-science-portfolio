# Data Science Portfolio
**Alex Domingues Batista, PhD**
Analytical Chemist | Data Scientist | 10+ Years in Research & Diagnostics

---

## 🎯 Quick Summary

**10+ years** combining analytical chemistry expertise with machine learning for pharma, diagnostics, and industrial analytics.

**Core Strengths:**
- ✅ **Python & ML:** Scikit-Learn, SHAP, PCA, Random Forest, Time-Series Analysis
- ✅ **Domain Expertise:** LC-MS, GC-MS, Sensor Instrumentation, Chemical Data
- ✅ **Real-World ML:** Biomarker Discovery, Predictive Maintenance, Sensor Drift Detection
- ✅ **Leadership:** Research Group Leader (Germany), Professor (Brazil), 50 Publications

**Target Industries:** Pharma • Diagnostics • Manufacturing • Industry 4.0 / Smart Factory

---

## 👨‍🔬 About Me

I am an Analytical Chemist (PhD, USP-Brazil) applying my research expertise to **data science and machine learning** in industry. My background includes 6 years as **Professor at Universidade Federal de Uberlândia** (2015-2021) and 2+ years as **Research Group Leader at Hahn-Schickard Institute, Germany** (2022-2024), where I developed analytical methods and led R&D projects.

Now, I'm focused on **applied data science**—using my domain knowledge in instrumentation, chemistry, and experimental design to build better ML models for real-world problems in pharma, diagnostics, and Industry 4.0 applications. My research background (50 publications, 1,266 citations, h-index 18) gives me a unique advantage: I understand the **physical systems behind the data**, enabling me to build more robust and interpretable models for predictive maintenance, sensor analytics, and smart manufacturing.

---

## 💡 What Makes This Portfolio Different

This portfolio showcases **data science with deep domain knowledge**. My analytical chemistry background gives me an advantage that typical data scientists lack:

- **I understand the physical systems generating the data** (sensors, instruments, chemical processes)
- **I know when models are wrong** (from years of validating analytical methods and troubleshooting instruments)
- **I think in experiments** (hypothesis testing, controls, validation—not just train/test splits)
- **I can bridge technical teams** (from lab scientists to data engineers)

Every project here demonstrates how domain expertise makes data science better:
- ✅ **Physics-Informed Features:** Engineering features based on how sensors actually behave
- ✅ **Rigorous Validation:** Applying laboratory QA/QC thinking to ML model validation
- ✅ **Explainable Models:** Using SHAP and chemometric techniques to build trust with domain experts
- ✅ **Real-World Robustness:** Accounting for drift, noise, and measurement uncertainty

I'm not just doing data science—I'm doing **better data science** because I understand what the data means.

---

## 📊 Featured Projects

### 1. [Explainable AI for Biomarker Prioritization](./metabolomics-biomarker-discovery/)
**Objective:** Accelerate biomarker validation by prioritizing high-confidence candidates using interpretable ML.

**Highlights:**
- Analyzed human cachexia dataset (76 samples, 63 metabolites) with high biological variability.
- Performed chemometric QC using **Volcano Plots** and **PCA** to validate sample separation.
- Compared **Lasso Regression** (57.9% accuracy, for feature selection) vs. **Random Forest** (48.6% accuracy, for non-linearity).
- Identified key metabolic drivers (e.g., Glucose, 3-Hydroxybutyrate) using **SHAP values**.
- **Business outcome:** €1.7M validation cost savings through SHAP prioritization (18,150% ROI).

**Tech Stack:** Python, Pandas, Scikit-Learn, SHAP, Seaborn (Volcano Plots)
**Business Impact:** Reduces 18,150 candidate tests to 50 high-confidence targets; €1.46M savings from single SHAP analysis.

**[View Project →](./metabolomics-biomarker-discovery/)**

---

### 2. [Gas Sensor Drift & Calibration Transfer](./gas-sensor-drift-monitoring/)
**Objective:** Solve "Concept Drift" in industrial chemical sensors to extend hardware lifespan.

**Highlights:**
- Analyzed a 3-year longitudinal dataset (13,910 measurements) from 16 chemical sensors.
- Visualized **Concept Drift** using PCA, showing how sensor aging degrades model performance.
- Quantified the "Cost of Inaction": Static models lost **67% accuracy** over 36 months (100% → 33%).
- Implemented an **Adaptive Calibration** strategy (windowed retraining) that maintained **100% accuracy** throughout.

**Tech Stack:** Python, Scikit-Learn (PCA, Random Forest), Drift Detection
**Business Impact:** Prevents $141.7B in false classifications; extends operational life of remote IIoT sensor networks.

**[View Project →](./gas-sensor-drift-monitoring/)**

---

### 3. [NASA Turbofan Predictive Maintenance](./nasa-turbofan-predictive-maintenance/)
**Objective:** Predict the Remaining Useful Life (RUL) of aircraft engines using sensor time-series.

**Highlights:**
- Processed multivariate time-series data from 100 turbofan engines (NASA C-MAPSS).
- Engineered **86 advanced features** (rolling statistics, lag features, cumulative trends, rate-of-change) to capture degradation patterns.
- Trained a **Gradient Boosting model achieving RMSE: 17.25 cycles** (8.6% of lifespan, 68.9% improvement over baseline).
- Achieved **state-of-the-art performance** (R² = 0.950) competitive with literature benchmarks (12-18 cycles).
- Validated the model using engine-level train/test split to prevent data leakage.

**Tech Stack:** Python, Time-Series Analysis, Gradient Boosting, Random Forest, Feature Engineering
**Business Impact:** Enables precise maintenance scheduling with 2-3 week lead time; €18M+ annual savings per 100-aircraft fleet.

**[View Project →](./nasa-turbofan-predictive-maintenance/)**

---

## 🛠️ Technical Skills

**Programming & Tools:**
- **Python:** Pandas, NumPy, Scikit-Learn, SHAP, Matplotlib, Seaborn, SciPy
- **Data Engineering:** SQL, Data Cleaning, Feature Engineering, ETL Pipelines
- **Analytical Instrumentation:** LC-MS, GC-MS, HPLC, Spectroscopy (UV-Vis, FTIR), Electrochemistry
- **Workflow:** Git, GitHub, Jupyter Notebooks, VS Code, Linux/Bash, LaTeX

**Machine Learning Focus:**
- **Chemometrics & ML:** PCA, HCA, Random Forest, Gradient Boosting, Lasso/Ridge Regression
- **Validation:** Stratified Cross-Validation, Outlier Detection, Drift Monitoring, DOE (Design of Experiments)
- **Explainability:** SHAP, Permutation Importance, Partial Dependence Plots
- **Time-Series:** Sensor drift detection, predictive maintenance, sequential data analysis

**Domain Expertise:**
- **Analytical Chemistry & Instrumentation:** PhD from USP-Brazil (CENA), specializing in chromatography, spectroscopy, and electroanalytical methods.
- **Biosensors & Smart Materials:** Developed molecularly imprinted polymers (MIPs) for SARS-CoV-2 detection (published in *Advanced Materials Interfaces*).
- **Academic Leadership:** Former Professor Adjunto at UFU (2015-2021), teaching analytical chemistry and coordinating graduate programs.
- **Industrial R&D Leadership:** Research Group Leader at Hahn-Schickard, Germany (2022-2024), managing EU-funded projects and industry partnerships.
- **Publications:** 50 peer-reviewed papers, 1,266 citations (Web of Science), h-index 18.
- **Green Chemistry & Sustainability:** Expertise in developing low-cost, portable analytical devices and environmentally friendly methods.

---

## 📁 Repository Structure

```text
data-science-portfolio/
├── README.md (this file)
├── data/
│   └── human_cachexia.csv              # Shared data folder
├── metabolomics-biomarker-discovery/    # Project 1: Pharma/Biotech
│   ├── 01_chemometric_eda.ipynb
│   ├── 02_biomarker_ml.ipynb
│   ├── 03_shap_interpretation.ipynb
│   ├── README.md
│   └── requirements.txt
├── gas-sensor-drift-monitoring/         # Project 2: QA/Industrial IoT
│   ├── 01_visualizing_the_drift.ipynb
│   ├── 02_model_decay_analysis.ipynb
│   ├── 03_adaptive_calibration.ipynb
│   ├── README.md
│   └── requirements.txt
└── nasa-turbofan-predictive-maintenance/# Project 3: Engineering
    ├── 01_data_exploration.ipynb
    ├── 02_data_quality_and_drift.ipynb
    ├── 03_predictive_modeling.ipynb
    └── README.md
```

**Note:** Large data files (gas-sensor batches, turbofan datasets, retail data) are gitignored. For local reproduction, see individual project READMEs for data source links.
---

## 📫 Let's Connect

Looking for: **Applied Data Scientist / Data Scientist** roles in Industry 4.0, Pharma, Diagnostics, or Manufacturing. Seeking opportunities to apply domain expertise to solve complex data problems.

- 📧 **Email:** [alexdbatista@gmail.com](mailto:alexdbatista@gmail.com)
- 🔗 **LinkedIn:** [linkedin.com/in/alexdbatista](https://linkedin.com/in/alexdbatista)
- 💻 **GitHub:** [github.com/alexdbatista](https://github.com/alexdbatista)

**Languages:** Portuguese (Native) | English (Fluent) | German (B1/Intermediate)
