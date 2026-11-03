#!/usr/bin/env python3
"""Download the QCL demo data cubes and trained U-Net checkpoint.

The files (~100 MB) are hosted on Hugging Face instead of Git LFS so the
repository stays small and clonable. Every file is verified with SHA-256.

Usage (from featured/qcl-breast-cancer-diagnostics/):
    python scripts/download_artifacts.py            # download missing files
    python scripts/download_artifacts.py --force    # re-download everything
"""
from __future__ import annotations

import argparse
import hashlib
import sys
import urllib.request
from pathlib import Path

HF_REPO = "alexdbatista/qcl-breast-cancer-diagnostics"
HF_REPO_TYPE = "spaces"
HF_REVISION = "main"
BASE_URL = f"https://huggingface.co/{HF_REPO_TYPE}/{HF_REPO}/resolve/{HF_REVISION}"

PROJECT_DIR = Path(__file__).resolve().parent.parent

# (relative path, sha256)
ARTIFACTS: list[tuple[str, str]] = [
    ("data/labels/001_labels.npy", "86b4ee94bc376f878ca841e11a88704acd8c5e5f36a39a06bfb5a1daf50d5c72"),
    ("data/labels/002_labels.npy", "b362983972251f4c38f08565b2e874d6bf7bb8ac8e9ff03b9231d163041fa47a"),
    ("data/labels/003_labels.npy", "f94880582a38593636d3a4cb650449991987a90d5a7d14ace1fdd516b7124d99"),
    ("data/labels/004_labels.npy", "538a3b66ac8ee5394385e62848e0a7eea4b4ce944e5da98eaa300d9c8fd6c130"),
    ("data/labels/005_labels.npy", "bd1696ce091b900a915b3ac9feefdae739e2839e5297c344e17e8db59d06563d"),
    ("data/processed/001_pca.npy", "0bebac9acf798a5633d02c8cbdf47af94e6f633e9e3a6d722696ce3c00fd236c"),
    ("data/processed/002_pca.npy", "aa7801a21a8878ff0bd6d6ec587fd18dbbff58ed30a557f79e4310b75c8d9d67"),
    ("data/processed/003_pca.npy", "02e7529f09097e1c991f17548581431b526febe976deb9d7e9dc7361576d3938"),
    ("data/processed/004_pca.npy", "938afe446eec541c5ea9601a58e58b9a9ce29e8adef35fa0e5e6a0d4759340c4"),
    ("data/processed/005_pca.npy", "61b537cd04d18d968502b661e0cbdbfdcc5447d526b85df2b7a678210dc2cfb9"),
    ("models/best_unet_qcl.pth", "2d069a8b22361d232a8a3c71844a7a5dc05d013d9ad332249a318f8e2ef79f53"),
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def download(rel: str, expected: str, force: bool = False) -> bool:
    dest = PROJECT_DIR / rel
    if dest.exists() and not force and sha256(dest) == expected:
        print(f"[ok]   {rel} (already present)")
        return True
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    url = f"{BASE_URL}/{rel}"
    print(f"[get]  {rel}")
    with urllib.request.urlopen(url) as r, tmp.open("wb") as f:
        while chunk := r.read(1 << 20):
            f.write(chunk)
    actual = sha256(tmp)
    if actual != expected:
        tmp.unlink(missing_ok=True)
        print(f"[FAIL] {rel}: checksum mismatch ({actual})", file=sys.stderr)
        return False
    tmp.replace(dest)
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--force", action="store_true", help="re-download all files")
    args = parser.parse_args()
    results = [download(rel, sha, args.force) for rel, sha in ARTIFACTS]
    if not all(results):
        return 1
    print(f"All {len(ARTIFACTS)} artifacts ready in {PROJECT_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
