# 🧪 ToxPred AI: In-Silico ADMET Screening Platform

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![RDKit](https://img.shields.io/badge/Cheminformatics-RDKit-green)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red)
![Status](https://img.shields.io/badge/Status-Live-success)

**ToxPred** is a Machine Learning application designed to accelerate early-stage drug discovery. It predicts critical physicochemical and biological properties of small molecules before synthesis, helping chemists "fail early" and prioritize viable drug candidates.

## 🚀 Key Features

* **💧 Solubility Prediction (LogS):** Regressor trained on the **Delaney (ESOL)** dataset to predict aqueous solubility.
* **☠️ Toxicity Screening:** Classifier trained on the **ClinTox** dataset to flag compounds that failed clinical trials.
* **🧠 Blood-Brain Barrier (BBB) Permeability:** Classifier trained on **BBBP** data to predict CNS penetration (crucial for Neuro-drug discovery).
* **💊 Drug-Likeness:** Automatic calculation of **Lipinski’s Rule of Five** to assess oral bioavailability.
* **🧬 Structural Intelligence:** Uses **Morgan Fingerprints (ECFP4)** to analyze chemical substructures (2,048-bit vectors) rather than simple molecular weights.

## 📊 Model Performance

| Model | Dataset | Algorithm | Metric |
| :--- | :--- | :--- | :--- |
| **Solubility** | Delaney (ESOL) | Random Forest Regressor | R² ≈ 0.87 |
| **Toxicity** | ClinTox (FDA) | Random Forest Classifier | Acc ≈ 76% |
| **BBB Permeability** | BBBP | Random Forest Classifier | ROC-AUC ≈ 0.85 |

## 🛠️ Tech Stack

* **Language:** Python
* **Cheminformatics:** RDKit (Molecular Descriptor Calculation & Fingerprinting)
* **Machine Learning:** Scikit-Learn (Random Forest Ensemble)
* **Web Framework:** Streamlit
* **Data Source:** DeepChem & PubChem PUG REST API

## 📦 Pre-trained Models

**Note:** This repository includes pre-trained model files (`*.pkl`, ~18MB total) tracked in git. While this is generally not recommended for large files, these models are necessary for:
- **Streamlit Cloud deployment** - The app requires immediate access to models without training
- **Demo purposes** - Users can run the app instantly without waiting for model training
- **Reproducibility** - Ensures consistent predictions across deployments

To regenerate models locally (requires internet access):
```bash
python step_models.py  # Downloads datasets and trains models (~2-5 minutes)
```

## 💻 Installation & Usage

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/alexdbatista/data-science-portfolio.git
    cd data-science-portfolio/toxpred
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the App** (models are pre-trained and included):
    ```bash
    streamlit run toxpred_app.py
    ```

4.  **(Optional) Regenerate models from scratch:**
    ```bash
    python step_models.py
    ```
    
    **Note:** This downloads datasets from DeepChem and trains three Random Forest models:
    - `solubility_model.pkl` (~9 MB)
    - `toxicity_model.pkl` (~3 MB)
    - `bbb_model.pkl` (~5 MB)

## 🧪 Example Use Cases

* **Aspirin:** Predicted as **Safe** and **Soluble**.
* **Dopamine:** Predicted as **BBB Impermeable** (correctly identifying it cannot treat Parkinson's directly).
* **Dieldrin (Pesticide):** Flagged as **Toxic** due to chlorinated ring substructures.

---
*Created by Alex as a Capstone Project for Data Science.*