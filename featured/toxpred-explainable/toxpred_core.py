"""Shared featurisation and data utilities for ToxPred.

Used by ``step_models.py`` (training), ``evaluate.py`` (benchmarking) and the
test suite, so every code path builds molecules the same way.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from rdkit import Chem, RDLogger
from rdkit.Chem import Crippen, Descriptors, rdFingerprintGenerator
from rdkit.Chem.Scaffolds import MurckoScaffold

RDLogger.DisableLog("rdApp.*")

FP_RADIUS = 2
FP_BITS = 2048

DATA_BASE = "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets"
DATASETS = {
    # name: (file, smiles column, target column, task)
    "solubility": ("delaney-processed.csv", "smiles",
                   "measured log solubility in mols per litre", "regression"),
    "toxicity": ("clintox.csv.gz", "smiles", "CT_TOX", "classification"),
    "bbb": ("BBBP.csv", "smiles", "p_np", "classification"),
}

_GENERATOR = rdFingerprintGenerator.GetMorganGenerator(radius=FP_RADIUS, fpSize=FP_BITS)


def get_fingerprint(smiles: str) -> np.ndarray | None:
    """Return a 2048-bit Morgan (ECFP4) fingerprint, or None for invalid SMILES."""
    if not isinstance(smiles, str) or not smiles:
        return None
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    return _GENERATOR.GetFingerprintAsNumPy(mol).astype(np.uint8)


# Physicochemical descriptors used (with the fingerprint) by the solubility model.
# Fingerprints alone generalise poorly to new scaffolds for LogS (R2 ~0.1 under
# scaffold CV); adding these lifts it to ~0.8. See evaluate.py.
SOL_DESCRIPTORS = {
    "MolLogP": Crippen.MolLogP,
    "MolWt": Descriptors.MolWt,
    "TPSA": Descriptors.TPSA,
    "NumRotatableBonds": Descriptors.NumRotatableBonds,
    "NumHDonors": Descriptors.NumHDonors,
    "NumHAcceptors": Descriptors.NumHAcceptors,
    "NumAromaticRings": Descriptors.NumAromaticRings,
    "FractionCSP3": Descriptors.FractionCSP3,
    "RingCount": Descriptors.RingCount,
    "HeavyAtomCount": Descriptors.HeavyAtomCount,
}


def descriptor_vector(smiles: str) -> np.ndarray | None:
    """Physicochemical descriptor vector (see SOL_DESCRIPTORS), or None if invalid."""
    mol = Chem.MolFromSmiles(smiles) if isinstance(smiles, str) and smiles else None
    if mol is None:
        return None
    return np.array([f(mol) for f in SOL_DESCRIPTORS.values()], dtype=float)


def model_features(smiles: str, task_name: str) -> np.ndarray | None:
    """Feature vector for a given model: descriptors + fingerprint for solubility,
    fingerprint only for the classifiers."""
    fp = get_fingerprint(smiles)
    if fp is None:
        return None
    if task_name == "solubility":
        return np.concatenate([descriptor_vector(smiles), fp])
    return fp.astype(float)


def murcko_scaffold(smiles: str) -> str:
    """Bemis-Murcko scaffold SMILES (empty string for acyclic molecules)."""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return ""
    return MurckoScaffold.MurckoScaffoldSmiles(mol=mol, includeChirality=False)


def featurize(smiles: pd.Series, target: pd.Series, task_name: str = "toxicity"
              ) -> tuple[np.ndarray, np.ndarray, list[str]]:
    """Featurise a SMILES column, dropping molecules RDKit cannot parse."""
    X, y, kept = [], [], []
    for smi, t in zip(smiles, target):
        fp = model_features(smi, task_name)
        if fp is not None and pd.notna(t):
            X.append(fp)
            y.append(t)
            kept.append(smi)
    return np.vstack(X), np.asarray(y), kept


def load_dataset(name: str, base: str = DATA_BASE) -> tuple[np.ndarray, np.ndarray, list[str], str]:
    """Download (or read from a local dir) one DeepChem dataset and featurise it."""
    file, smi_col, target_col, task = DATASETS[name]
    df = pd.read_csv(f"{base}/{file}").dropna(subset=[target_col])
    X, y, smiles = featurize(df[smi_col], df[target_col], name)
    if task == "classification":
        y = y.astype(int)
    return X, y, smiles, task
