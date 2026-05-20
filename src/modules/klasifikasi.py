"""
Klasifikasi status osmolaritas dan kondisi klinis sampel.
"""
import json
from pathlib import Path


def load_ref():
    path = Path(__file__).parent.parent.parent / "data" / "ion_reference_ranges.json"
    with open(path) as f:
        return json.load(f)


def klasifikasi_osmolaritas(osm: float) -> str:
    """
    Klasifikasi osmolaritas plasma:
    - Hipoosmolar : < 275 mOsm/kg
    - Normal      : 275–295 mOsm/kg
    - Hiperosmolar: > 295 mOsm/kg
    """
    ref = load_ref()["osmolaritas"]
    if osm < ref["hipoosmolar_batas"]:
        return "Hipoosmolar"
    elif osm > ref["hiperosmolar_batas"]:
        return "Hiperosmolar"
    else:
        return "Normal"


def deteksi_kondisi_klinis(sampel: dict) -> list[str]:
    """
    Deteksi kondisi patologis berdasarkan profil ion.
    Returns list kondisi yang terdeteksi.
    """
    kondisi = []
    na = sampel.get("na", 140)
    k  = sampel.get("k", 4.0)
    gluc = sampel.get("glukosa_mgdl", 90)
    bun  = sampel.get("bun_mgdl", 14)
    hco3 = sampel.get("hco3", 25)

    if na > 145:
        kondisi.append("Hipernatremia")
    elif na < 136:
        kondisi.append("Hiponatremia")

    if k > 5.0:
        kondisi.append("Hiperkalemia")
    elif k < 3.5:
        kondisi.append("Hipokalemia")

    if gluc > 180:
        kondisi.append("Hiperglikemia (kemungkinan DM)")

    if bun > 20:
        kondisi.append("Azotemia (kemungkinan gangguan ginjal)")

    if hco3 < 22:
        kondisi.append("Asidosis metabolik")
    elif hco3 > 28:
        kondisi.append("Alkalosis metabolik")

    if not kondisi:
        kondisi.append("Tidak ada kelainan terdeteksi")

    return kondisi


def ringkasan_sampel(sample_id: str, sampel: dict, osm_dc: float, osm_vh: float) -> dict:
    """Buat ringkasan lengkap hasil analisis satu sampel."""
    return {
        "sample_id": sample_id,
        "kondisi_dataset": sampel.get("kondisi", "-"),
        "osmolaritas_DC": round(osm_dc, 2),
        "osmolaritas_VH": round(osm_vh, 2),
        "osmolal_gap": round(osm_vh - osm_dc, 2),
        "status": klasifikasi_osmolaritas(osm_dc),
        "kondisi_klinis": deteksi_kondisi_klinis(sampel),
    }
