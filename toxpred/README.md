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

## 💻 Installation & Usage

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/toxpred.git](https://github.com/your-username/toxpred.git)
    cd toxpred
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Generate the AI Models:**
    ```bash
    python step_models.py
    ```
    
    **Note:** This will download datasets from DeepChem and train three Random Forest models:
    - `solubility_model.pkl` (~9 MB)
    - `toxicity_model.pkl` (~3 MB)
    - `bbb_model.pkl` (~5 MB)
    
    These models are not tracked in git due to their size. You must generate them locally before running the app.

4.  **Run the App:**
    ```bash
    streamlit run toxpred_app.py
    ```

## 🧪 Example Use Cases

* **Aspirin:** Predicted as **Safe** and **Soluble**.
* **Dopamine:** Predicted as **BBB Impermeable** (correctly identifying it cannot treat Parkinson's directly).
* **Dieldrin (Pesticide):** Flagged as **Toxic** due to chlorinated ring substructures.

---
*Created by Alex as a Capstone Project for Data Science.*