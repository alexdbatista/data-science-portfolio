# Contributing

Guidelines for maintaining this portfolio.

## Layout

```
data-science-portfolio/
├── README.md
├── data/                          # Small shared datasets (human_cachexia.csv)
├── featured/                      # Maintained projects
│   ├── toxpred-explainable/
│   ├── metabolomics-biomarker-discovery/
│   └── qcl-breast-cancer-diagnostics/
├── archive/                       # Older projects, kept for reference, not maintained
├── tests/                         # pytest suite, run in CI
├── .github/workflows/ci.yml       # ruff + pytest on every push and pull request
├── requirements.txt               # Root deps for the Streamlit Cloud ToxPred deployment
└── requirements-dev.txt           # Test/lint deps
```

Each featured project is self-contained: its own `README.md` and `requirements.txt`.

## Running checks locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
pip install torch --index-url https://download.pytorch.org/whl/cpu   # for the QCL tests
ruff check .
pytest
```

## Data and model files

- Don't commit large binaries. Git LFS is not used.
- QCL arrays and the U-Net checkpoint are hosted on Hugging Face and fetched with
  `featured/qcl-breast-cancer-diagnostics/scripts/download_artifacts.py`, which checks SHA-256 hashes.
- ToxPred models (`*.pkl`) are gitignored and trained on first launch of the app.
- Every dataset must state its source (URL and citation) in the project README.
  Synthetic data must be labelled as synthetic.

## Reporting results

- Numbers in a README must be reproducible from code in the repo, ideally from a script
  that writes a results file (for example `featured/toxpred-explainable/evaluation_results.csv`).
- Report the split strategy (scaffold, cross-validation, held-out) and a simple baseline next to each model.
- Report mean ± standard deviation across folds rather than a single best score.

## Commits

- One logical change per pull request; CI must pass before merging.
- Notebooks: restart and run all before committing so outputs match the code.
