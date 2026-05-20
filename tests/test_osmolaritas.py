"""Unit tests untuk modul osmolaritas."""
import pytest
import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent.parent))

from src.modules.osmolaritas import dorwart_chalmers, vant_hoff_extended, osmolal_gap


def test_dorwart_chalmers_normal():
    hasil = dorwart_chalmers(na=140, glukosa_mgdl=90, bun_mgdl=14)
    assert 285 <= hasil <= 295, f"Expected ~290, got {hasil:.2f}"


def test_vant_hoff_lebih_besar_dari_dc():
    dc = dorwart_chalmers(140, 90, 14)
    vh = vant_hoff_extended(140, 4.0, 102, 25, 90, 14)
    assert vh > dc, "Van't Hoff harus lebih besar dari Dorwart-Chalmers"


def test_osmolal_gap_positif():
    dc = dorwart_chalmers(140, 90, 14)
    vh = vant_hoff_extended(140, 4.0, 102, 25, 90, 14)
    gap = osmolal_gap(dc, vh)
    assert gap > 0


def test_hiperglikemia_tingkatkan_osmolaritas():
    normal = dorwart_chalmers(140, 90, 14)
    hiperglik = dorwart_chalmers(140, 480, 14)
    assert hiperglik > normal
