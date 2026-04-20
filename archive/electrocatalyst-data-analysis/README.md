# ⚡ Electrocatalyst Data Analysis: Experimental Campaign Intelligence

This repository details an end-to-end data analysis pipeline for **high-throughput electrocatalyst screening campaigns**, bridging the gap between raw electrochemical measurements and machine learning models.

**Core Pipeline Capabilities:**
- **Experimental Data Quality Assurance:** Programmatic identification of electrochemical artifacts (e.g., electrode fouling, reference drift, uncompensated resistance).
- **Multi-Campaign Learning:** Tracking evolutionary understanding and feature stability across iterative experimental batches.
- **Signal Definition:** Statistical isolation of authentic catalytic trends from combinatorial noise.
- **Cross-Functional Scientific Reporting:** Translating complex electrochemical/chemometric findings into actionable directives for synthetic chemists and ML engineers.

---

## 📊 What's Inside

### Module 1: Experimental Data QA & Anomaly Detection
**File:** `01_experimental_data_quality.ipynb`

**Objective:** Systematically assess data quality from an electrocatalyst screening campaign and flag physical artifacts before they corrupt downstream models.

**Technical Workflow:**
- Voltage/current stability monitoring (detecting surface poisoning and reference electrode drift).
- Temperature coefficient modeling on electrochemical kinetics.
- Replicate consistency scoring (Cyclic Voltammetry reproducibility, charge transfer resistance stability via EIS).
- Missing data physics (differentiating sensor failures from LOD truncation).
- Statistical outlier detection explicitly weighted by electrochemical context.

*Impact: Ensures downstream ML models learn actual surface chemistry rather than fitting to measurement artifacts.*

---

### Module 2: Multi-Campaign Comparison & Learning
**File:** `02_campaign_comparison_learning.ipynb`

**Objective:** Quantify the evolution of experimental understanding across sequential high-throughput campaigns.

**Technical Workflow:**
- Campaign-to-campaign performance baseline tracking.
- Batch effect quantification and systematic bias correction.
- Feature importance evolution (monitoring which molecular descriptors selectively predict catalytic activity over time).
- Statistical classification of failure modes vs. success rates.

*Impact: Establishes a compound-learning framework necessary for "self-driving" laboratory loops, rather than analyzing experimental batches in isolation.*

---

### Module 3: Scientific Digest & Reporting
**File:** `03_scientific_communication.ipynb`

**Objective:** Standardize the interface between automated analysis and human-in-the-loop laboratory decisions.

**Outputs Generated:**
- **Executive Digests:** Rapid assessment of campaign yield.
- **Laboratory Feedback Loops:** Direct, data-backed recommendations for refining experimental design.
- **ML Feature Scoping:** Identifying which physical signals contain sufficient variance for predictive modeling.
- **Computational Validation Targets:** Highlighting experimental anomalies that warrant DFT/computational investigation.

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

## 🎓 Domain Translation: Physical Chemistry to ML

A major friction point in materials informatics is the uncritical application of ML to raw sensor data. With 10+ years of electrochemistry research experience, this pipeline explicitly hard-codes physical constraints:

- **Electrode Kinetics:** Recognizing that non-linearities often map to strict Butler-Volmer kinetics or mass-transport limitations, not arbitrary data drift.
- **Artifact Flagging:** Preemptively filtering out ohmic drop (iR), double-layer capacitive charging masquerading as Faradaic current, and working electrode poisoning. 
- **Environmental Context:** Building specific data checks for reference electrode shifts (e.g., Ag/AgCl stability) and localized pH gradients at the interface.
- **Algorithmic Rigor:** Using standard ML stacks (scikit-learn, scipy) strictly constrained by physical boundaries and uncertainty quantification.

---

## 📁 Pipeline Architecture

```
electrocatalyst-data-analysis/
├── README.md                           
├── 01_experimental_data_quality.ipynb  # Data QA & artifact flagging
├── 02_campaign_comparison_learning.ipynb # Multi-campaign statistical analysis
├── 03_scientific_communication.ipynb   # Automated reporting schemas
├── data/
│   ├── campaign_1_results.csv         
│   ├── campaign_2_results.csv
│   └── campaign_3_results.csv
├── outputs/
│   ├── executive_digest.md            
│   ├── lab_feedback_report.md         
│   └── figures/                        
└── requirements.txt                    
```
