"""Benchmark ToxPred models with scaffold-split cross-validation.

Molecules are grouped by Bemis-Murcko scaffold so that test folds contain
chemotypes never seen in training - a much harder (and more realistic)
estimate than a random split. Each Random Forest is compared with a
logistic/ridge baseline and a trivial majority/mean predictor.

Usage:  python evaluate.py [--folds 5] [--data-dir PATH]
Writes: evaluation_results.csv and prints a Markdown table.
"""
from __future__ import annotations

import argparse
import os

import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import (
    average_precision_score,
    balanced_accuracy_score,
    mean_absolute_error,
    r2_score,
    roc_auc_score,
    root_mean_squared_error,
)
from sklearn.model_selection import GroupKFold
from toxpred_core import DATA_BASE, DATASETS, load_dataset, murcko_scaffold

SEED = 42


def models_for(task: str) -> dict:
    if task == "regression":
        return {
            "Random Forest": RandomForestRegressor(n_estimators=100, random_state=SEED, n_jobs=-1),
            "Ridge (baseline)": Ridge(alpha=10.0),
            "Mean predictor": DummyRegressor(),
        }
    return {
        "Random Forest": RandomForestClassifier(
            n_estimators=100, class_weight="balanced", random_state=SEED, n_jobs=-1),
        "Logistic Regression (baseline)": LogisticRegression(
            C=0.1, class_weight="balanced", max_iter=2000),
        "Majority class": DummyClassifier(strategy="most_frequent"),
    }


def score(task: str, y_true, pred, proba=None) -> dict:
    if task == "regression":
        return {"R2": r2_score(y_true, pred),
                "RMSE": root_mean_squared_error(y_true, pred),
                "MAE": mean_absolute_error(y_true, pred)}
    return {"ROC-AUC": roc_auc_score(y_true, proba),
            "PR-AUC": average_precision_score(y_true, proba),
            "Balanced Acc": balanced_accuracy_score(y_true, pred),
            "Accuracy": float(np.mean(y_true == pred))}


def evaluate(name: str, folds: int, base: str) -> pd.DataFrame:
    X, y, smiles, task = load_dataset(name, base)
    scaffolds = [murcko_scaffold(s) for s in smiles]
    groups = pd.factorize(pd.Series(scaffolds))[0]
    cv = GroupKFold(n_splits=folds, shuffle=True, random_state=SEED)
    rows = []
    for model_name, model in models_for(task).items():
        for fold, (tr, te) in enumerate(cv.split(X, y, groups)):
            if task == "classification" and len(np.unique(y[te])) < 2:
                continue
            model.fit(X[tr], y[tr])
            pred = model.predict(X[te])
            proba = model.predict_proba(X[te])[:, 1] if task == "classification" else None
            rows.append({"dataset": name, "model": model_name, "fold": fold,
                         **score(task, y[te], pred, proba)})
    out = pd.DataFrame(rows)
    pos = f", {y.mean():.1%} positive" if task == "classification" else ""
    print(f"{name}: {len(y)} molecules, {len(set(scaffolds))} scaffolds{pos}")
    return out


def summarise(df: pd.DataFrame) -> str:
    lines = []
    for name, sub in df.groupby("dataset", sort=False):
        metrics = [c for c in sub.columns if c not in ("dataset", "model", "fold")
                   and sub[c].notna().any()]
        lines += [f"\n**{name}**\n", "| Model | " + " | ".join(metrics) + " |",
                  "|---" * (len(metrics) + 1) + "|"]
        for model, m in sub.groupby("model", sort=False):
            cells = [f"{m[c].mean():.2f} ± {m[c].std():.2f}" for c in metrics]
            lines.append(f"| {model} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--folds", type=int, default=5)
    parser.add_argument("--data-dir", default=DATA_BASE,
                        help="URL or local folder containing the DeepChem CSVs")
    args = parser.parse_args()
    df = pd.concat([evaluate(n, args.folds, args.data_dir) for n in DATASETS])
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "evaluation_results.csv")
    df.to_csv(out, index=False)
    print(summarise(df))


if __name__ == "__main__":
    main()
