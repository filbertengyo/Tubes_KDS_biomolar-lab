"""Unit tests untuk modul klasifikasi."""
import pytest
import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent.parent))

from src.modules.klasifikasi import klasifikasi_osmolaritas, deteksi_kondisi_klinis


def test_normal():
    assert klasifikasi_osmolaritas(285) == "Normal"


def test_hipoosmolar():
    assert klasifikasi_osmolaritas(260) == "Hipoosmolar"


def test_hiperosmolar():
    assert klasifikasi_osmolaritas(310) == "Hiperosmolar"


def test_deteksi_hipernatremia():
    sampel = {"na": 162, "k": 4.0, "hco3": 25, "glukosa_mgdl": 90, "bun_mgdl": 14}
    kondisi = deteksi_kondisi_klinis(sampel)
    assert "Hipernatremia" in kondisi


def test_deteksi_hiperglikemia():
    sampel = {"na": 138, "k": 4.0, "hco3": 25, "glukosa_mgdl": 480, "bun_mgdl": 14}
    kondisi = deteksi_kondisi_klinis(sampel)
    assert any("Hiperglikemia" in k for k in kondisi)


def test_normal_no_kondisi():
    sampel = {"na": 140, "k": 4.0, "hco3": 25, "glukosa_mgdl": 90, "bun_mgdl": 14}
    kondisi = deteksi_kondisi_klinis(sampel)
    assert kondisi == ["Tidak ada kelainan terdeteksi"]
