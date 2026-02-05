# ⚡ Electrocatalyst Data Analysis: Experimental Campaign Intelligence

**Target Role:** Chemical Data Scientist at Dunia  
**Domain:** Electrochemistry • Materials Discovery • Experimental Data QA

---

## 🎯 Project Overview

This project demonstrates end-to-end data analysis for **high-throughput electrocatalyst screening campaigns**, showcasing skills directly relevant to materials discovery loops and experimental data science.

**Key capabilities demonstrated:**
- ✅ **Experimental data quality assessment** - Identifying artifacts, anomalies, and failure modes
- ✅ **Multi-campaign learning** - Tracking understanding evolution across experiments
- ✅ **Signal vs noise discrimination** - Statistical methods for reliable trend detection
- ✅ **Scientific communication** - Clear, concise digests for cross-functional teams
- ✅ **Electrochemistry expertise** - Domain knowledge applied to data interpretation

---

## 📊 What's Inside

### Notebook 1: Experimental Data QA & Anomaly Detection
**File:** `01_experimental_data_quality.ipynb`

**Objective:** Assess data quality from an electrocatalyst screening campaign and identify experimental artifacts.

**Key analyses:**
- Voltage/current stability checks (detecting electrode fouling, reference drift)
- Temperature drift effects on electrochemical measurements
- Replicate consistency (CV reproducibility, charge transfer resistance)
- Missing data patterns (sensor failures, measurement gaps)
- Statistical outlier detection with electrochemical context

**Why this matters for Dunia:**  
Shows ability to interrogate experimental data and distinguish real effects from artifacts - critical for the "Be the scientific sense-maker" aspect of the role.

---

### Notebook 2: Multi-Campaign Comparison & Learning
**File:** `02_campaign_comparison_learning.ipynb`

**Objective:** Compare results across multiple experimental campaigns and track how understanding evolves.

**Key analyses:**
- Campaign-to-campaign performance trends
- Batch effects and systematic biases
- Feature importance evolution (which descriptors predict activity)
- Success rate metrics and failure mode classification
- Recommendation prioritization for next experiments

**Why this matters for Dunia:**  
Demonstrates "Make learning compound, not fragment" - tracking understanding across campaigns, not just within them.

---

### Notebook 3: Scientific Digest & Reporting
**File:** `03_scientific_communication.ipynb`

**Objective:** Create clear, actionable summaries that align cross-functional teams.

**Deliverables:**
- **Executive digest** - Key findings in 1 page for program managers
- **Lab feedback report** - Specific recommendations on experimental design and quality
- **ML feature recommendations** - Which signals should inform model design
- **Computational validation priorities** - Which discrepancies merit DFT/simulation follow-up

**Why this matters for Dunia:**  
Shows ability to "Raise the bar for how scientific progress is communicated internally" - translating complex analysis into actionable insights.

---

## 🧪 Technical Stack

**Core libraries:**
```python
pandas, numpy              # Data manipulation
matplotlib, seaborn        # Visualization
scikit-learn              # Statistical modeling, PCA, clustering
scipy.stats               # Statistical tests (t-tests, ANOVA, correlation)
```

**Electrochemistry-specific:**
```python
# Domain knowledge applied through:
# - Butler-Volmer kinetics interpretation
# - Tafel slope analysis
# - Impedance spectroscopy (Nyquist plots)
# - Cyclic voltammetry (CV) metrics
```

**Materials science integration (future):**
```python
pymatgen                  # Crystal structure analysis, composition features
ASE                       # Atomic structure manipulation
RDKit                     # Molecular descriptors (for molecular catalysts)
```

---

## 🎓 Domain Expertise Applied

**From PhD in Electrochemistry:**
- Understanding of electrode kinetics and mass transport
- Recognition of common artifacts (iR drop, double-layer charging, surface poisoning)
- Knowledge of reference electrode stability and measurement protocols
- Awareness of environmental effects (temperature, pH, electrolyte composition)

**Data science approach:**
- Statistical rigor in experimental comparison
- Uncertainty quantification for concentration estimates
- Reproducibility assessment and batch effect correction
- Clear communication of limitations and confidence levels

---

## 🚀 Key Takeaways for Hiring Managers

**What this project proves:**

1. **Chemistry + Data Science integration**  
   Not just applying ML blindly - using electrochemical intuition to interpret patterns

2. **Experimental data maturity**  
   Understanding that raw data ≠ analysis-ready data; QA is critical

3. **Scientific judgment**  
   Distinguishing real trends from noise, identifying when more data is needed

4. **Communication excellence**  
   Creating outputs useful for lab scientists, ML engineers, and program managers

5. **Systems thinking**  
   Not just analyzing data - influencing pipelines, experimental design, and infrastructure

---

## 🔗 Relevance to Dunia's Mission

**Your mission:** *"Turn Dunia's experimental output into an understanding that drives better decisions"*

**How this project aligns:**

| Dunia Requirement | Demonstrated in This Project |
|-------------------|------------------------------|
| Interrogate electrocatalyst campaign data | Notebook 1: Systematic data quality assessment |
| Identify patterns, anomalies, failure modes | Notebook 1: Artifact detection, outlier analysis |
| Develop intuition for where experiments lie | Throughout: Electrochemical context in interpretation |
| Decide which signals inform ML features | Notebook 2: Feature importance, descriptor evolution |
| Give lab teams feedback on quality | Notebook 3: Actionable experimental recommendations |
| Track understanding evolution across campaigns | Notebook 2: Multi-campaign comparison framework |
| Create clear, concise digests | Notebook 3: Stakeholder-specific reporting |
| Influence data pipelines by using them | Analysis suggests "analysis-ready" data requirements |

---

## 📁 Project Structure

```
electrocatalyst-data-analysis/
├── README.md                           # This file
├── 01_experimental_data_quality.ipynb  # Data QA & anomaly detection
├── 02_campaign_comparison_learning.ipynb # Multi-campaign analysis
├── 03_scientific_communication.ipynb   # Reporting & digests
├── data/
│   ├── campaign_1_results.csv         # Simulated electrocatalyst data
│   ├── campaign_2_results.csv
│   └── campaign_3_results.csv
├── outputs/
│   ├── executive_digest.md            # 1-page summary for managers
│   ├── lab_feedback_report.md         # Experimental recommendations
│   └── figures/                        # Key visualizations
└── requirements.txt                    # Project dependencies
```

---

## 🎯 Target Audience

**Roles this project is designed to impress:**
- Chemical Data Scientist (Dunia)
- Materials Informatics Engineer
- Computational Chemistry / ML Scientist
- R&D Data Science (electrochemistry/energy materials focus)

**Companies:**
- Dunia (clean energy materials discovery)
- Acceleration Consortium (self-driving labs)
- Materials Project / National Lab partnerships
- Battery companies (QuantumScape, Solid Power)
- Catalyst companies (Johnson Matthey, BASF)

---

## 📧 Contact

**Alex Domingues Batista, PhD**  
📧 alexdbatista@gmail.com  
🔗 [LinkedIn](https://linkedin.com/in/alexdbatista) | [GitHub](https://github.com/alexdbatista)

**Background:** 10+ years electrochemistry research, PhD in Analytical Chemistry, former Humboldt Fellow, Research Group Leader at Hahn-Schickard Institute (Germany)
