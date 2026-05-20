"""
Perhitungan osmolaritas plasma dengan dua metode:
1. Dorwart-Chalmers (klinis standar)
2. Van't Hoff extended (semua ion)
"""


def dorwart_chalmers(na: float, glukosa_mgdl: float, bun_mgdl: float) -> float:
    """
    Formula klinis standar.
    Osm = 2[Na+] + [Glukosa]/18 + [BUN]/2.8
    Satuan: mOsm/kg
    """
    return 2 * na + (glukosa_mgdl / 18) + (bun_mgdl / 2.8)


def vant_hoff_extended(na: float, k: float, cl: float, hco3: float,
                        glukosa_mgdl: float, bun_mgdl: float) -> float:
    """
    Formula Van't Hoff diperluas untuk semua ion utama.
    Osm = 2(Na + K + Cl + HCO3) + Glukosa/18 + BUN/2.8
    Satuan: mOsm/kg
    """
    return 2 * (na + k + cl + hco3) + (glukosa_mgdl / 18) + (bun_mgdl / 2.8)


def osmolal_gap(osm_dc: float, osm_vh: float) -> float:
    """Selisih antara dua metode perhitungan."""
    return osm_vh - osm_dc


def kontribusi_per_ion(na: float, k: float, cl: float, hco3: float,
                        glukosa_mgdl: float, bun_mgdl: float) -> dict:
    """Hitung kontribusi osmotik masing-masing ion (mOsm/kg)."""
    return {
        "na":   2 * na,
        "k":    2 * k,
        "cl":   2 * cl,
        "hco3": 2 * hco3,
        "glukosa": glukosa_mgdl / 18,
        "bun":  bun_mgdl / 2.8,
    }
