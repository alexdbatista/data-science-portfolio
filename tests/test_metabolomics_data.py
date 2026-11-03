"""Sanity checks for the metabolomics dataset used by the notebooks."""
import numpy as np
import pandas as pd
import pytest

from conftest import REPO_ROOT

DATA = REPO_ROOT / "data" / "human_cachexia.csv"


@pytest.fixture(scope="module")
def df():
    return pd.read_csv(DATA)


def test_schema(df):
    assert list(df.columns[:2]) == ["Sample", "Condition"]
    assert df["Sample"].is_unique
    assert set(df["Condition"]) == {"Cachexic", "Control"}


def test_metabolite_matrix_is_clean(df):
    X = df.drop(columns=["Sample", "Condition"])
    assert X.shape[1] == 63
    assert len(X) >= 70
    assert all(np.issubdtype(t, np.number) for t in X.dtypes)
    assert not X.isna().any().any()
    assert (X > 0).all().all(), "log2 transform in the notebooks needs strictly positive values"
