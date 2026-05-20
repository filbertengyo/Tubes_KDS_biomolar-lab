"""Unit tests untuk modul molaritas dan converter."""
import pytest
import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent.parent))

from src.utils.converter import hitung_molaritas, hitung_pengenceran, gram_ke_mol


def test_hitung_mol_nacl():
    mol = gram_ke_mol(58.44, 58.44)
    assert abs(mol - 1.0) < 0.001


def test_molaritas_nacl_1M():
    M = hitung_molaritas(massa_gram=58.44, bm=58.44, volume_liter=1.0)
    assert abs(M - 1.0) < 0.001


def test_molaritas_setengah_volume():
    M = hitung_molaritas(massa_gram=58.44, bm=58.44, volume_liter=0.5)
    assert abs(M - 2.0) < 0.001


def test_pengenceran_m1v1_m2v2():
    M2 = hitung_pengenceran(M1=1.0, V1=0.1, V2=1.0)
    assert abs(M2 - 0.1) < 0.0001


def test_volume_nol_raises():
    with pytest.raises(ValueError):
        hitung_molaritas(10, 58.44, 0)
