"""Shared pytest helpers."""
import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
FEATURED = REPO_ROOT / "featured"


def load_module(path: Path, name: str):
    """Import a module from a file path (needed for numbered files like 03_*.py)."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return REPO_ROOT
