"""Unit tests for the ToxPred featurisation utilities (no network needed)."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

pytest.importorskip("rdkit")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "featured" / "toxpred-explainable"))

from toxpred_core import (  # noqa: E402
    FP_BITS,
    SOL_DESCRIPTORS,
    featurize,
    get_fingerprint,
    model_features,
    murcko_scaffold,
)

ASPIRIN = "CC(=O)OC1=CC=CC=C1C(=O)O"
CAFFEINE = "CN1C=NC2=C1C(=O)N(C(=O)N2C)C"


def test_fingerprint_shape_and_binary():
    fp = get_fingerprint(ASPIRIN)
    assert fp.shape == (FP_BITS,)
    assert set(np.unique(fp)) <= {0, 1}
    assert fp.sum() > 0


@pytest.mark.parametrize("bad", ["", "not_a_smiles", "C1CC", None])
def test_invalid_smiles_returns_none(bad):
    assert get_fingerprint(bad) is None
    assert model_features(bad, "solubility") is None


def test_fingerprint_is_deterministic_and_discriminative():
    assert np.array_equal(get_fingerprint(ASPIRIN), get_fingerprint(ASPIRIN))
    assert not np.array_equal(get_fingerprint(ASPIRIN), get_fingerprint(CAFFEINE))


def test_solubility_features_prepend_descriptors():
    feats = model_features(ASPIRIN, "solubility")
    assert feats.shape == (len(SOL_DESCRIPTORS) + FP_BITS,)
    mol_wt = feats[list(SOL_DESCRIPTORS).index("MolWt")]
    assert mol_wt == pytest.approx(180.16, abs=0.05)


def test_classifier_features_are_fingerprint_only():
    assert model_features(CAFFEINE, "toxicity").shape == (FP_BITS,)


def test_murcko_scaffold():
    assert murcko_scaffold(ASPIRIN) == "c1ccccc1"
    assert murcko_scaffold("CCO") == ""  # acyclic


def test_featurize_drops_invalid_rows():
    smiles = pd.Series([ASPIRIN, "garbage", CAFFEINE])
    X, y, kept = featurize(smiles, pd.Series([1.0, 2.0, 3.0]))
    assert X.shape == (2, FP_BITS)
    assert list(y) == [1.0, 3.0]
    assert kept == [ASPIRIN, CAFFEINE]
