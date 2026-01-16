# RFM Customer Segmentation (RFM + K-Means) — Validation-Focused Analytics

Customer segmentation project using the UCI Online Retail dataset (~540k transactions) to create actionable customer groups. Emphasis on **robust methodology**: comparing approaches, validating segment separability, and testing stability of assignments.

**Tech:** Python, pandas, scikit-learn, scipy, matplotlib/seaborn  
**Notebook:** `RFM_Customer_Segmentation.ipynb`  
**Author:** Alex Domingues Batista (Analytics + statistics background)

---

## Key Results (TL;DR)
- Segmented **4,372 customers** into **5 actionable groups**
- **Revenue concentration:** top segment contributes ~**60%** of revenue
- **Statistical validation:** segments significantly different (**ANOVA p < 0.001**)
- **Method agreement:** **70–80%** consistency between RFM scoring and K-Means
- **Stability test:** **>80%** assignment stability when switching quartiles → quintiles
- **CLV signal:** Champions ~£6,732 vs Hibernating ~£222 (≈30×)

---

## Problem
E-commerce businesses need a simple, interpretable segmentation to prioritize retention, win-back, and lifecycle marketing. This project builds customer segments and validates that they are:
1) **Distinct** (statistically separable)  
2) **Stable** (robust to parameter choices)  
3) **Actionable** (easy to communicate to stakeholders)

---

## Data
**UCI Online Retail Dataset** (13 months of UK e-commerce transactions).  
Download: https://archive.ics.uci.edu/ml/datasets/online+retail  
File: `Online Retail.xlsx` (place in repo root)

---

## Approach
1. **Data cleaning**
   - Removed invalid records and prepared customer-level aggregates
2. **RFM feature engineering**
   - Recency, Frequency, Monetary features (customer-level)
3. **Two segmentation methods**
   - **RFM scoring** (quartiles; also tested quintiles)
   - **K-Means clustering** (k=5 with scaling)
4. **Validation**
   - Segment separability: **ANOVA**
   - Agreement between methods: assignment overlap (70–80%)
   - Sensitivity/stability: quartiles vs quintiles (>80% stable)

---

## Business Actions (example playbook)
| Segment | Action |
|---|---|
| Champions | VIP retention, early access, high-touch support |
| Loyal Customers | Cross-sell, referrals, subscription/loyalty program |
| Potential Loyalists | Incentivize second purchase, onboarding sequences |
| At Risk | Win-back offers, churn diagnostics |
| Hibernating | Low-cost reactivation or suppression |

---

## What I Tested (and why it matters)
- **Quartiles vs quintiles:** tested robustness of scoring choices (stability >80%)
- **RFM vs K-Means:** compared interpretability vs data-driven clusters (70–80% agreement)
- **Assumptions & structure:** checked distributions and correlation (e.g., F–M correlation)

---

## Tech Stack
- Data: `pandas`, `numpy`, `openpyxl`
- Stats: `scipy` (ANOVA, tests), correlation analysis
- ML: `scikit-learn` (StandardScaler, KMeans, silhouette)
- Viz: `matplotlib`, `seaborn`

---

## Project Structure
retail-customer-segmentation/ │ ├── RFM_Customer_Segmentation.ipynb # Main analysis notebook ├── README.md # Project overview ├── .gitignore # Excludes local files (e.g., data) └── Online Retail.xlsx # Downloaded separately (not committed)

---

## Reproducibility (How to run)
```bash
git clone https://github.com/alexdbatista/retail-customer-segmentation.git
cd retail-customer-segmentation
pip install -r requirements.txt
jupyter notebook RFM_Customer_Segmentation.ipynb
