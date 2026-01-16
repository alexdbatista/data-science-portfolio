# Data Science Portfolio
**Alex Domingues Batista, PhD**
Analytical Chemist | Data Scientist | 10+ Years in Research & Diagnostics

---

## 👨‍🔬 About Me

I am an Analytical Chemist (PhD, USP-Brazil) applying my research expertise to **data science and machine learning** in industry. My background includes 6 years as **Professor at Universidade Federal de Uberlândia** (2015-2021) and 2+ years as **Research Group Leader at Hahn-Schickard Institute, Germany** (2022-2024), where I developed analytical methods and led R&D projects.

Now, I'm focused on **applied data science**—using my domain knowledge in instrumentation, chemistry, and experimental design to build better ML models for real-world problems in pharma, diagnostics, and industrial analytics. My research background (50 publications, 1,266 citations, h-index 18) gives me a unique advantage: I understand the **physical systems behind the data**, enabling me to build more robust and interpretable models.

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

### 1. [LC-MS Metabolomics Biomarker Discovery](./metabolomics-biomarker-discovery/)
**Objective:** Identify biological markers for muscle wasting (Cachexia) using ML on high-dimensional chemical data.

**Highlights:**
- Analyzed real human cachexia dataset (76 samples, 63 metabolites) with high biological variability.
- Performed chemometric QC using **Volcano Plots** and **PCA** to validate sample separation.
- Compared **Lasso Regression** (for feature selection) vs. **Random Forest** (for non-linearity).
- Identified key metabolic drivers (e.g., Glucose, 3-Hydroxybutyrate) using **SHAP values**.

**Tech Stack:** Python, Pandas, Scikit-Learn, SHAP, Seaborn (Volcano Plots)
**Business Impact:** Accelerates biomarker discovery pipelines by prioritizing high-confidence candidates for clinical validation.

**[View Project →](./metabolomics-biomarker-discovery/)**

---

### 2. [Gas Sensor Drift & Calibration Transfer](./gas-sensor-drift-monitoring/)
**Objective:** Solve "Concept Drift" in industrial chemical sensors to extend hardware lifespan.

**Highlights:**
- Analyzed a 3-year longitudinal dataset (13,910 measurements) from 16 chemical sensors.
- Visualized **Concept Drift** using PCA, showing how sensor aging degrades model performance.
- Quantified the "Cost of Inaction": Static models lost **66.9% accuracy** over 36 months.
- Implemented an **Adaptive Calibration** strategy (active retraining) that recovered accuracy to **>90%**.

**Tech Stack:** Python, Scikit-Learn (PCA, Random Forest), Drift Detection
**Business Impact:** Reduces calibration costs and extends the operational life of remote IIoT sensor networks.

**[View Project →](./gas-sensor-drift-monitoring/)**

---

### 3. [NASA Turbofan Predictive Maintenance](./nasa-turbofan-predictive-maintenance/)
**Objective:** Predict the Remaining Useful Life (RUL) of aircraft engines using sensor time-series.

**Highlights:**
- Processed multivariate time-series data from 100 turbofan engines (NASA C-MAPSS).
- Engineered **Rolling Statistics** and **Trend Features** to distinguish true degradation from signal noise.
- Trained a **Random Forest Regressor** to predict failure cycles (RMSE: ~20 cycles).
- Validated the model using a "Leave-One-Group-Out" strategy to prevent data leakage.

**Tech Stack:** Python, Time-Series Analysis, Random Forest, Matplotlib
**Business Impact:** Enables predictive maintenance scheduling, reducing unplanned downtime and optimizing parts inventory.

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

📫 Let's Connect

Looking for: Applied Data Scientist / Data Scientist roles in Industrial Analytics, Pharma, Diagnostics, or Manufacturing. Seeking opportunities to apply domain expertise to solve complex data problems.

📧 Email: alexdbatista@gmail.com

🔗 LinkedIn: linkedin.com/in/alexdbatista

💻 GitHub: github.com/alexdbatista

Languages: Portuguese (Native) | English (Fluent) | German (B1/Intermediate)
