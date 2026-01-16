# Data Science Portfolio
**Alex Domingues Batista, PhD**
Analytical Chemist | Data Scientist | 10+ Years in Research & Diagnostics

---

## 👨‍🔬 About Me

I am an Analytical Chemist (PhD) transitioning to Data Science after 10+ years managing diagnostic systems and experimental research. I combine deep domain expertise in **instrumentation and signal processing** with modern machine learning to solve real-world problems in predictive maintenance, pharma, and industrial analytics.

My background is not just "analyzing numbers"—it is about verifying the physical reality behind the data. I bring a rigorous **validation mindset** (checking for drift, noise, and reproducibility) that is often missing in standard data science workflows.

---

## 💡 What Makes This Portfolio Different

Unlike typical bootcamp portfolios, every analysis here is treated like a scientific experiment:
- ✅ **Solves "Messy" Physical Problems:** Sensor drift, biological variability, and signal noise.
- ✅ **Focuses on Validation:** Using rigorous cross-validation and stability checks, not just "Accuracy scores."
- ✅ **Emphasizes Explainability:** Using SHAP and feature importance to tell the "Why," not just the "What."
- ✅ **Bridges Disciplines:** Translating concepts from **Instrument Calibration** directly to **Machine Learning**.

I am not learning data science from scratch—I am adding ML to a decade of analytical thinking.

---

## 📊 Featured Projects

### 1. [LC-MS Metabolomics Biomarker Discovery](./metabolomics-biomarker-discovery/)
**Objective:** Identify biological markers for muscle wasting (Cachexia) using ML on high-dimensional chemical data.

**Highlights:**
- Analyzed real human cachexia dataset (77 samples, 63 metabolites) with high biological variability.
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
- **Python:** Pandas, NumPy, Scikit-Learn, SHAP, Matplotlib, Seaborn
- **Data Engineering:** SQL, Data Cleaning, Feature Engineering
- **Workflow:** Git, GitHub, Jupyter Notebooks, VS Code, Linux/Bash

**Machine Learning Focus:**
- **Tabular & Time-Series:** Random Forest, Gradient Boosting, Lasso/Ridge
- **Validation:** Stratified Cross-Validation, Outlier Detection, Drift Monitoring
- **Explainability:** SHAP, Permutation Importance, Partial Dependence Plots

**Domain Expertise:**
- **10+ Years in Scientific Research:** Deep experience in experimental design and rigorous data validation.
- **Instrument Diagnostics:** Expert in validating sensor performance and characterizing signal drift.
- **Signal Processing:** Translating raw, noisy detector signals into reliable analytical results.
- **Technical Leadership:** Experience bridging the gap between R&D engineering and data analysis teams.

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

**Note:** Data files for gas-sensor and nasa-turbofan projects need to be downloaded separately (see individual project READMEs for links).
---

📫 Let's Connect

Looking for: Data Scientist / Analyst roles in Industrial Analytics, Pharma, or Predictive Maintenance.

📧 Email: alexdbatista@gmail.com

🔗 LinkedIn: linkedin.com/in/alexdbatista

💻 GitHub: github.com/alexdbatista

Languages: Portuguese (Native) | English (Fluent) | German (B1/Intermediate)
