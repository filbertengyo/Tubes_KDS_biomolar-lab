"""
Modul perhitungan molaritas dan pengenceran larutan biologis.
"""
from src.utils.converter import hitung_molaritas, hitung_pengenceran, BERAT_MOLEKUL


def hitung_dari_input(nama_zat: str, massa_gram: float, volume_liter: float) -> dict:
    """
    Hitung molaritas larutan dari nama zat, massa, dan volume.
    Returns dict berisi molaritas dalam M, mM, dan μM.
    """
    if nama_zat not in BERAT_MOLEKUL:
        raise ValueError(f"Zat '{nama_zat}' tidak ada dalam database. "
                         f"Pilihan: {list(BERAT_MOLEKUL.keys())}")
    bm = BERAT_MOLEKUL[nama_zat]
    M = hitung_molaritas(massa_gram, bm, volume_liter)
    return {
        "zat": nama_zat,
        "bm": bm,
        "massa_gram": massa_gram,
        "volume_liter": volume_liter,
        "molaritas_M": round(M, 6),
        "molaritas_mM": round(M * 1000, 4),
        "molaritas_uM": round(M * 1e6, 2),
    }


def seri_pengenceran(M_stok: float, V_akhir: float, jumlah_langkah: int,
                      faktor: float = 10) -> list[dict]:
    """
    Buat tabel pengenceran serial.
    Default faktor pengenceran = 10x.
    """
    hasil = []
    M = M_stok
    for i in range(jumlah_langkah):
        M2 = M / faktor
        V1 = hitung_v1_pengenceran(M, M2, V_akhir)
        hasil.append({
            "langkah": i + 1,
            "M_awal_M": round(M, 6),
            "M_akhir_M": round(M2, 6),
            "V_diambil_mL": round(V1 * 1000, 4),
            "V_akhir_mL": round(V_akhir * 1000, 2),
        })
        M = M2
    return hasil


def hitung_v1_pengenceran(M1: float, M2: float, V2: float) -> float:
    """V1 = M2 * V2 / M1"""
    return (M2 * V2) / M1
