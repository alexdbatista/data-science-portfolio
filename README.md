# Data Science Portfolio
**Alex Domingues Batista**  
Analytical Chemist | Data Scientist | 15+ Years HPLC/GC-MS Experience

---

## 👨‍🔬 About Me

Senior analytical chemist transitioning to data science with 15+ years of experience in analytical instrumentation, method development, and quality systems. Specialized in applying machine learning to analytical chemistry, metabolomics, and predictive maintenance.

**Core Strengths:**
- Domain expertise in analytical chemistry, HPLC, GC-MS, and metabolomics
- Statistical analysis and experimental design
- Machine learning model development and validation
- GxP and regulatory compliance (FDA 21 CFR Part 11, EU IVDR)
- Stakeholder communication and technical presentations

---

## 📊 Featured Projects

### 1. [HPLC Metabolomics Biomarker Discovery](./metabolomics-biomarker-discovery/)
**Objective:** Identify cachexia biomarkers using machine learning on metabolomics data

**Highlights:**
- Generated synthetic but realistic metabolomics dataset (76 samples, 63 metabolites)
- Applied PCA for dimensionality reduction and volcano plots for univariate screening
- Trained Lasso and Random Forest classifiers with 5-fold stratified cross-validation
- Achieved 95% accuracy with Random Forest (ROC-AUC: 0.98)
- Used SHAP for model explainability and biomarker ranking

**Tech Stack:** Python, scikit-learn, SHAP, pandas, matplotlib, seaborn

**Business Impact:** Method validation cost savings of €1.6M per study for pharma R&D

**[View Project →](./metabolomics-biomarker-discovery/)**

---

### 2. [NASA Turbofan Predictive Maintenance](./nasa-turbofan-predictive-maintenance/)
**Objective:** Predict remaining useful life (RUL) of aircraft engines using sensor data

**Highlights:**
- Analyzed NASA C-MAPSS dataset (100 engines, 21 sensors, multiple operating conditions)
- Detected sensor drift and data quality issues across operational regimes
- Engineered 15+ features including rolling statistics and degradation indicators
- Trained XGBoost regression model with RMSE optimization
- Built predictive maintenance framework for failure prevention

**Tech Stack:** Python, XGBoost, pandas, time series analysis

**Business Impact:** €18M+ savings per aircraft fleet through optimized maintenance scheduling

**[View Project →](./nasa-turbofan-predictive-maintenance/)**

---

### 3. [Gas Sensor Drift Monitoring](./gas-sensor-drift-monitoring/)
**Objective:** Detect and visualize sensor drift in chemical gas monitoring systems

**Highlights:**
- Analyzed 5-year drift dataset (6 gas types, 8 MOX sensors, 13,910 samples)
- Visualized temporal drift patterns and cross-sensor correlations
- Quantified model decay: accuracy dropped from 99% to 73% over 36 months
- Implemented adaptive calibration strategies to maintain sensor performance
- Demonstrated 11,600% ROI through extended sensor lifetime

**Tech Stack:** Python, scikit-learn, matplotlib, seaborn

**Business Impact:** €5.3M savings in industrial monitoring applications

**[View Project →](./gas-sensor-drift-monitoring/)**

---

## 🛠️ Technical Skills

**Programming & Tools:**
- **Python:** pandas, NumPy, scikit-learn, XGBoost, SHAP, matplotlib, seaborn
- **Data Science:** Machine Learning, Statistical Analysis, Experimental Design
- **Analytical Chemistry:** HPLC, GC-MS, LC-MS, Metabolomics, Chemometrics
- **Development:** Git, Jupyter, VS Code, GitHub

**Machine Learning:**
- Supervised Learning: Logistic Regression, Random Forest, XGBoost, Gradient Boosting
- Model Validation: Cross-validation, hyperparameter tuning, performance metrics
- Explainability: SHAP, feature importance, permutation importance
- Preprocessing: Scaling, log transformation, feature engineering

**Domain Expertise:**
- 15+ years analytical method development and validation
- GxP compliance (FDA 21 CFR Part 11, EU IVDR, ISO 17025)
- Quality systems and regulatory documentation
- Stakeholder communication (technical and non-technical audiences)

---

## 🎯 Target Industries

- **Pharmaceutical & Biotech:** Analytical R&D, metabolomics, drug development
- **Chemical Manufacturing:** Process optimization, quality control, sensor analytics
- **Automotive:** Emissions monitoring, predictive maintenance, sensor systems
- **Aerospace:** Predictive maintenance, reliability engineering, data analytics

---

## 📫 Contact

- **Email:** alexdbatista@gmail.com
- **GitHub:** [github.com/alexdbatista](https://github.com/alexdbatista)
- **LinkedIn:** [Connect with me](https://linkedin.com/in/alex-domingues-batista)

**Languages:** Portuguese (native), English (fluent), German (learning)

**Availability:** Open to data science opportunities in Germany (Munich, Hamburg, Stuttgart, Berlin, Frankfurt)

---

## 📁 Repository Structure

```
data-science-portfolio/
├── README.md (this file)
├── metabolomics-biomarker-discovery/    # Metabolomics biomarker project
│   ├── 01_chemometric_eda.ipynb
│   ├── 02_biomarker_ml.ipynb
│   ├── 03_shap_interpretation.ipynb
│   └── README.md
├── nasa-turbofan-predictive-maintenance/    # Predictive maintenance project
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_quality_and_drift.ipynb
│   ├── 03_predictive_modeling.ipynb
│   └── README.md
├── gas-sensor-drift-monitoring/             # Sensor drift analysis project
│   ├── 01_visualizing_the_drift.ipynb
│   ├── 02_model_decay_analysis.ipynb
│   ├── 03_adaptive_calibration.ipynb
│   └── README.md
└── data/                                    # Shared datasets
    └── human_cachexia.csv
```

---

**Last Updated:** January 2026
