"""
03_model_training.py
=====================
XGBoost Weed Emergence Classifier + SHAP Explainability

Trains a binary XGBoost model to predict Brachiaria decumbens emergence risk
within a 14-day window from agronomic microclimate features.

Pipeline:
  1. Load engineered features from 02_feature_engineering.py
  2. Build a time-aware train/test split (no data leakage across seasons)
  3. Handle class imbalance with scale_pos_weight
  4. Hyperparameter tune via TimeSeriesSplit cross-validation
  5. Evaluate with ROC-AUC, F1, precision-recall
  6. Generate SHAP global + local explanations
  7. Export model artefact for REST API serving
"""

import json
import warnings
import joblib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")                          # headless rendering for CI
import matplotlib.pyplot as plt
import shap
import xgboost as xgb
from pathlib import Path
from sklearn.metrics import (
    classification_report, roc_auc_score,
    average_precision_score, ConfusionMatrixDisplay
)
from sklearn.model_selection import TimeSeriesSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
DATA_DIR    = Path(__file__).parent / "data"
MODELS_DIR  = Path(__file__).parent / "models"
REPORTS_DIR = Path(__file__).parent / "reports"
MODELS_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

FEATURES_PATH = DATA_DIR / "features.csv"
MODEL_PATH    = MODELS_DIR / "xgb_weed_emergence.joblib"
SCALER_PATH   = MODELS_DIR / "scaler.joblib"
METRICS_PATH  = REPORTS_DIR / "model_metrics.json"


# ---------------------------------------------------------------------------
# Load & split
# ---------------------------------------------------------------------------

def load_and_split(path: Path, test_pct: float = 0.2):
    """
    Perform a chronological train/test split to prevent temporal data leakage.

    Splits the dataset using a hard year boundary (2021 train, 2022 test) to 
    respect the temporal autocorrelation inherent in microclimate telemetry.

    Parameters
    ----------
    path : Path
        Filesystem path to the engineered features CSV.
    test_pct : float, optional
        Target percentage for testing split (overridden by hard date boundaries).

    Returns
    -------
    tuple
        (X_train, X_test, y_train, y_test, features_list) holding the split arrays.
    """
    df = pd.read_csv(path, index_col="Date", parse_dates=True)
    df = df.dropna()

    TARGET = "emergence_risk_14d"
    features = [c for c in df.columns if c != TARGET]

    # Use year boundary instead of random split to respect temporal autocorrelation
    split_date = "2022-01-01"
    train = df.loc[:split_date]
    test  = df.loc[split_date:]

    X_train = train[features]
    y_train = train[TARGET]
    X_test  = test[features]
    y_test  = test[TARGET]

    print(f"[INFO] Train: {len(X_train)} rows ({y_train.sum()} positive)")
    print(f"[INFO] Test : {len(X_test)} rows ({y_test.sum()} positive)")

    return X_train, X_test, y_train, y_test, features


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------

def build_model(class_ratio: float) -> xgb.XGBClassifier:
    """
    Construct an XGBoost classifier configured for imbalanced time-series forecasting.

    Parameters
    ----------
    class_ratio : float
        The ratio of negative to positive class instances, used to dynamically
        scale the positive weight during gradient boosting.

    Returns
    -------
    xgb.XGBClassifier
        Compiled XGBoost estimator instance with regularized hyperparameters.
    """
    return xgb.XGBClassifier(
        n_estimators=300,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=class_ratio,
        use_label_encoder=False,
        eval_metric="logloss",
        random_state=42,
        n_jobs=-1,
    )


def time_series_cv(X_train: pd.DataFrame, y_train: pd.Series) -> dict:
    """
    Execute k-fold rolling-window cross-validation for time-series data.

    Ensures that validation sets strictly succeed training sets in time.

    Parameters
    ----------
    X_train : pd.DataFrame
        Training feature matrix (must be chronologically ordered).
    y_train : pd.Series
        Training target vector.

    Returns
    -------
    dict
        Dictionary containing the mean and standard deviation of ROC-AUC
        and Average Precision scores across all evaluated folds.
    """
    tscv = TimeSeriesSplit(n_splits=5)
    aucs, aps = [], []
    neg = (y_train == 0).sum()
    pos = (y_train == 1).sum()
    ratio = neg / max(pos, 1)

    for fold, (tr_idx, val_idx) in enumerate(tscv.split(X_train)):
        X_tr, X_val = X_train.iloc[tr_idx], X_train.iloc[val_idx]
        y_tr, y_val = y_train.iloc[tr_idx], y_train.iloc[val_idx]

        scaler = StandardScaler()
        X_tr_s = scaler.fit_transform(X_tr)
        X_val_s = scaler.transform(X_val)

        model = build_model(ratio)
        model.fit(X_tr_s, y_tr,
                  eval_set=[(X_val_s, y_val)],
                  verbose=False)

        proba = model.predict_proba(X_val_s)[:, 1]
        if y_val.nunique() > 1:
            auc = roc_auc_score(y_val, proba)
            ap  = average_precision_score(y_val, proba)
            aucs.append(auc)
            aps.append(ap)
            print(f"  Fold {fold+1}: ROC-AUC={auc:.4f}  AP={ap:.4f}")

    return {"cv_roc_auc_mean": float(np.mean(aucs)),
            "cv_roc_auc_std":  float(np.std(aucs)),
            "cv_ap_mean":      float(np.mean(aps))}


# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------

def evaluate(model, scaler, X_test, y_test) -> dict:
    X_test_s = scaler.transform(X_test)
    proba = model.predict_proba(X_test_s)[:, 1]
    pred  = (proba > 0.5).astype(int)

    roc_auc = roc_auc_score(y_test, proba) if y_test.nunique() > 1 else None
    ap      = average_precision_score(y_test, proba) if y_test.nunique() > 1 else None
    report  = classification_report(y_test, pred, output_dict=True)

    print("\n--- Test Set Evaluation ---")
    print(classification_report(y_test, pred))
    if roc_auc:
        print(f"ROC-AUC : {roc_auc:.4f}")
        print(f"Avg Prec: {ap:.4f}")

    # Confusion matrix
    fig, ax = plt.subplots(figsize=(5, 4))
    ConfusionMatrixDisplay.from_predictions(y_test, pred, ax=ax,
                                            colorbar=False, cmap="Greens")
    ax.set_title("Confusion Matrix — B. decumbens Emergence Risk")
    fig.tight_layout()
    fig.savefig(REPORTS_DIR / "confusion_matrix.png", dpi=150)
    plt.close(fig)

    return {"test_roc_auc": roc_auc, "test_avg_precision": ap, **report}


# ---------------------------------------------------------------------------
# SHAP Explanations
# ---------------------------------------------------------------------------

def explain_with_shap(model, scaler, X_test, feature_names):
    print("\n[INFO] Computing SHAP values ...")
    X_test_s = pd.DataFrame(
        scaler.transform(X_test),
        columns=feature_names,
        index=X_test.index
    )

    explainer    = shap.TreeExplainer(model)
    shap_values  = explainer.shap_values(X_test_s)

    # Global feature importance — beeswarm
    fig, ax = plt.subplots(figsize=(9, 6))
    shap.summary_plot(shap_values, X_test_s, show=False, plot_type="bar",
                      color="#2ecc71")
    plt.title("SHAP Feature Importance — Global", fontsize=13)
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / "shap_global_importance.png", dpi=150, bbox_inches="tight")
    plt.close()

    # Dot plot (distribution of SHAP impact)
    fig, ax = plt.subplots(figsize=(9, 6))
    shap.summary_plot(shap_values, X_test_s, show=False)
    plt.title("SHAP Value Distribution — Feature Impact", fontsize=13)
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / "shap_dot_plot.png", dpi=150, bbox_inches="tight")
    plt.close()

    # Local explanation — single highest-risk day
    proba = model.predict_proba(X_test_s.values)[:, 1]
    peak_idx = np.argmax(proba)
    shap_exp = shap.Explanation(
        values=shap_values[peak_idx],
        base_values=explainer.expected_value,
        data=X_test_s.iloc[peak_idx].values,
        feature_names=feature_names,
    )
    fig, ax = plt.subplots(figsize=(10, 4))
    shap.waterfall_plot(shap_exp, show=False)
    plt.title(f"SHAP Waterfall — Peak Risk Day: {X_test.index[peak_idx].date()}", fontsize=12)
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / "shap_waterfall_peak_day.png", dpi=150, bbox_inches="tight")
    plt.close()

    print(f"[INFO] SHAP plots saved to {REPORTS_DIR}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("[INFO] Loading features ...")
    X_train, X_test, y_train, y_test, feature_names = load_and_split(FEATURES_PATH)

    neg = (y_train == 0).sum()
    pos = (y_train == 1).sum()
    ratio = neg / max(pos, 1)
    print(f"[INFO] Class imbalance ratio (neg/pos): {ratio:.2f}")

    print("\n[INFO] Running time-series cross-validation ...")
    cv_metrics = time_series_cv(X_train, y_train)
    print(f"\n  CV ROC-AUC : {cv_metrics['cv_roc_auc_mean']:.4f} ± {cv_metrics['cv_roc_auc_std']:.4f}")
    print(f"  CV Avg Prec: {cv_metrics['cv_ap_mean']:.4f}")

    print("\n[INFO] Training final model on full training set ...")
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)

    final_model = build_model(ratio)
    final_model.fit(X_train_s, y_train, verbose=False)

    # Evaluate
    test_metrics = evaluate(final_model, scaler, X_test, y_test)

    # SHAP
    explain_with_shap(final_model, scaler, X_test, feature_names)

    # Save artefacts
    joblib.dump(final_model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)

    all_metrics = {**cv_metrics, **{k: v for k, v in test_metrics.items()
                                     if isinstance(v, float)}}
    with open(METRICS_PATH, "w") as f:
        json.dump(all_metrics, f, indent=2)

    print(f"\n[DONE] Model → {MODEL_PATH}")
    print(f"[DONE] Scaler → {SCALER_PATH}")
    print(f"[DONE] Metrics → {METRICS_PATH}")
