"""
Validasi input data sampel plasma.
"""
import json
from pathlib import Path


def load_referensi() -> dict:
    path = Path(__file__).parent.parent.parent / "data" / "ion_reference_ranges.json"
    with open(path) as f:
        return json.load(f)


def validasi_sampel(sampel: dict) -> dict:
    """
    Validasi nilai ion dalam sampel terhadap rentang referensi.
    Returns dict berisi status tiap ion: 'normal', 'tinggi', atau 'rendah'.
    """
    ref = load_referensi()
    hasil = {}
    for ion, info in ref["ion"].items():
        if ion not in sampel:
            continue
        nilai = sampel[ion]
        if nilai < info["min"]:
            hasil[ion] = {"status": "rendah", "nilai": nilai, "ref": info}
        elif nilai > info["max"]:
            hasil[ion] = {"status": "tinggi", "nilai": nilai, "ref": info}
        else:
            hasil[ion] = {"status": "normal", "nilai": nilai, "ref": info}
    return hasil
