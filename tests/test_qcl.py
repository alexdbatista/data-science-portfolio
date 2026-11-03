"""Tests for the QCL hyperspectral U-Net and its evaluation metrics (CPU, tiny tensors)."""
import re

import pytest

torch = pytest.importorskip("torch")

from conftest import FEATURED, load_module  # noqa: E402

QCL = FEATURED / "qcl-breast-cancer-diagnostics"


@pytest.fixture(scope="module")
def unet_cls():
    return load_module(QCL / "03_spatial_cnn_segmentation.py", "qcl_unet").HyperspectralUNet


@pytest.fixture(scope="module")
def training():
    pytest.importorskip("scipy")
    return load_module(QCL / "04_model_training.py", "qcl_training")


@pytest.mark.parametrize("size", [32, 30])  # 30 exercises the skip-connection padding
def test_unet_output_shape(unet_cls, size):
    model = unet_cls(in_channels=10, num_classes=4).eval()
    with torch.no_grad():
        out = model(torch.randn(2, 10, size, size))
    assert out.shape == (2, 4, size, size)
    assert torch.isfinite(out).all()


def test_unet_backward_pass(unet_cls):
    model = unet_cls(in_channels=5, num_classes=3)
    out = model(torch.randn(1, 5, 16, 16))
    loss = torch.nn.functional.cross_entropy(out, torch.randint(0, 3, (1, 16, 16)))
    loss.backward()
    assert all(p.grad is not None for p in model.parameters() if p.requires_grad)


def test_iou_dice_perfect_prediction(training):
    target = torch.tensor([[[0, 1], [2, 3]]])
    scores = training.compute_iou_dice(target.clone(), target, num_classes=4)
    assert scores["iou"] == pytest.approx([1.0] * 4)
    assert scores["dice"] == pytest.approx([1.0] * 4)


def test_iou_dice_partial_overlap(training):
    preds = torch.tensor([[[1, 1], [0, 0]]])
    target = torch.tensor([[[1, 0], [0, 0]]])
    scores = training.compute_iou_dice(preds, target, num_classes=2)
    assert scores["iou"][1] == pytest.approx(0.5, abs=1e-4)      # 1 / 2
    assert scores["dice"][1] == pytest.approx(2 / 3, abs=1e-4)   # 2*1 / (2+1)
    assert scores["iou"][0] == pytest.approx(2 / 3, abs=1e-4)    # 2 / 3


def test_artifact_manifest_is_well_formed():
    script = QCL / "scripts" / "download_artifacts.py"
    if not script.exists():
        pytest.skip("download script not present on this branch")
    manifest = load_module(script, "qcl_download").ARTIFACTS
    assert len(manifest) == 11
    for rel, sha in manifest:
        assert re.fullmatch(r"[0-9a-f]{64}", sha), rel
        assert rel.startswith(("data/", "models/"))
