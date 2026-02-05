# Contributing to Data Science Portfolio

This document provides guidelines for maintaining and contributing to this portfolio repository.

## 📁 Repository Structure

This portfolio follows a project-based organization where each subdirectory is a self-contained data science project:

```
data-science-portfolio/
├── README.md                                  # Main portfolio overview
├── CONTRIBUTING.md                            # This file
├── LICENSE                                    # Repository license
├── .gitignore                                 # Global ignore rules
├── data/                                      # Shared datasets (small files only)
│   └── human_cachexia.csv
│
├── GuardianCGM/                              # 🩸 Clinical glucose prediction AI
│   ├── README.md                             # Project-specific documentation
│   ├── requirements.txt                      # Project dependencies
│   ├── 01_Signal_Processing_and_EDA.ipynb
│   ├── 02_Model_Training_and_Clinical_Evaluation.ipynb
│   ├── 03_Model_Deployment_and_Inference.ipynb
│   ├── 04_Bias_and_Fairness_Audit.ipynb
│   ├── 05_Drift_Monitoring_Strategy.py
│   └── 06_Drift_Monitoring_Demo.ipynb
│
├── metabolomics-biomarker-discovery/        # 🔬 LC-MS biomarker ML
│   ├── README.md
│   ├── requirements.txt
│   ├── 01_chemometric_eda.ipynb
│   ├── 02_biomarker_ml.ipynb
│   └── 03_shap_interpretation.ipynb
│
├── gas-sensor-drift-monitoring/             # 📊 Concept drift analytics
│   ├── README.md
│   ├── requirements.txt
│   ├── 01_visualizing_the_drift.ipynb
│   ├── 02_model_decay_analysis.ipynb
│   └── 03_adaptive_calibration.ipynb
│
├── nasa-turbofan-predictive-maintenance/    # 🔧 Time-series RUL prediction
│   ├── README.md
│   ├── requirements.txt
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_quality_and_drift.ipynb
│   ├── 03_predictive_modeling.ipynb
│   └── improve_model.py
│
├── retail-customer-segmentation/            # 🛒 RFM + K-Means segmentation
│   ├── README.md
│   ├── requirements.txt
│   ├── RFM_Customer_Segmentation.ipynb
│   └── RFM_Interview_Prep.ipynb
│
└── toxpred/                                  # 🧪 Cheminformatics ADMET app
    ├── README.md
    ├── requirements.txt
    ├── toxpred_app.py
    └── step_models.py
```

## 🎯 Project Organization Guidelines

### Each Project Should Include:

1. **README.md**
   - Clear project title with emoji
   - Problem statement and objectives
   - Key highlights and results
   - Tech stack
   - Installation and usage instructions
   - Example outputs or screenshots

2. **requirements.txt**
   - All Python dependencies with versions
   - Use `pip freeze > requirements.txt` after testing

3. **Numbered Notebooks** (for multi-part projects)
   - Use prefixes: `01_`, `02_`, `03_`, etc.
   - Clear, descriptive names
   - Execute in order

4. **Data Management**
   - Small datasets (<1MB): commit to `data/` folder
   - Large datasets: add to `.gitignore` and document download links in README
   - Include data provenance and source information

5. **Model Files**
   - **NEVER** commit large model files (`.pkl`, `.h5`, `.joblib`)
   - Provide training scripts to regenerate models
   - Document model generation in README

## 📝 Naming Conventions

### Directories
- Use lowercase with hyphens: `my-project-name/`
- Be descriptive but concise
- Avoid special characters

### Notebooks
- Use numbered prefixes for sequential workflows: `01_data_prep.ipynb`
- Use underscores for multi-word names
- Be descriptive: `02_model_training_and_evaluation.ipynb`

### Python Scripts
- Use snake_case: `drift_monitoring.py`
- Match the purpose: `setup_models.py`, `feature_engineering.py`

## 🚫 What NOT to Commit

The `.gitignore` file handles most exclusions, but be aware:

- **Large files** (>10MB)
- **Model artifacts** (`.pkl`, `.h5`, `.joblib`)
- **Virtual environments** (`venv/`, `env/`)
- **IDE settings** (`.vscode/`, `.idea/`)
- **Notebook checkpoints** (`.ipynb_checkpoints/`)
- **Temporary files** (`*.log`, `*.tmp`)
- **Sensitive data** (API keys, credentials)

## 📦 Dependencies

### Root-Level Files

- **requirements.txt**: Streamlit dependencies for cloud deployment
- **packages.txt**: System-level dependencies (Linux packages)

### Project-Level Files

Each project has its own `requirements.txt` for isolated environments.

## 🔧 Development Workflow

### Adding a New Project

1. Create a new directory at root level
2. Add a comprehensive README.md
3. Create requirements.txt
4. Add notebooks/scripts with clear naming
5. Test all code locally
6. Update main README.md with project link
7. Add project-specific `.gitignore` if needed

### Modifying Existing Projects

1. Test changes locally
2. Update README if behavior changes
3. Ensure notebooks run end-to-end
4. Update requirements.txt if adding dependencies
5. Keep commits atomic and well-described

## 🧪 Quality Standards

- **Reproducibility**: All code should run without errors
- **Documentation**: Clear inline comments and markdown cells
- **Code Style**: Follow PEP 8 guidelines
- **Modularity**: Break complex logic into functions
- **Visualization**: Professional plots with labels and titles

## 📊 Data Science Best Practices

1. **Avoid data leakage**: proper train/test splits
2. **Set random seeds**: for reproducibility
3. **Document assumptions**: clearly state limitations
4. **Version control**: commit working code frequently
5. **Validation**: use appropriate metrics for each problem

## 🔒 Security

- Never commit API keys, tokens, or credentials
- Use environment variables for sensitive data
- Review `.gitignore` before committing new file types

## 📞 Contact

For questions or suggestions about this portfolio structure:
- **Email**: alexdbatista@gmail.com
- **LinkedIn**: [linkedin.com/in/alexdbatista](https://linkedin.com/in/alexdbatista)
- **GitHub**: [github.com/alexdbatista](https://github.com/alexdbatista)

---

*This portfolio is maintained by Alex Domingues Batista, PhD - Data Scientist specializing in healthcare AI, sensor data, and ML engineering.*
