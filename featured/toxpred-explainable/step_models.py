"""Train the three ToxPred Random Forest models on the full datasets.

Run once before launching the app:  python step_models.py
For honest performance estimates see evaluate.py (scaffold-split CV).
"""
import os
import pickle

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from toxpred_core import load_dataset

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUTS = {
    "solubility": "solubility_model.pkl",
    "toxicity": "toxicity_model.pkl",
    "bbb": "bbb_model.pkl",
}


def build_model(task: str):
    if task == "regression":
        return RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    return RandomForestClassifier(
        n_estimators=100, class_weight="balanced", random_state=42, n_jobs=-1
    )


def main() -> None:
    for name, filename in OUTPUTS.items():
        print(f"Training {name} model...")
        X, y, _, task = load_dataset(name)
        model = build_model(task).fit(X, y)
        with open(os.path.join(CURRENT_DIR, filename), "wb") as f:
            pickle.dump(model, f)
        print(f"  saved {filename} ({len(y)} molecules)")
    print("All 3 models ready.")


if __name__ == "__main__":
    main()
