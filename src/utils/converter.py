"""
Konversi satuan untuk larutan biologis.
"""

# Berat molekul umum (g/mol)
BERAT_MOLEKUL = {
    "NaCl": 58.44,
    "KCl": 74.55,
    "glukosa": 180.16,
    "urea": 60.06,
    "CaCl2": 110.98,
    "MgCl2": 95.21,
}


def mg_per_dl_ke_mmol_per_l(nilai: float, bm: float) -> float:
    """Konversi mg/dL ke mmol/L menggunakan berat molekul."""
    return (nilai / bm) * 10


def mmol_per_l_ke_meq_per_l(nilai: float, valensi: int) -> float:
    """Konversi mmol/L ke mEq/L."""
    return nilai * valensi


def meq_per_l_ke_mmol_per_l(nilai: float, valensi: int) -> float:
    """Konversi mEq/L ke mmol/L."""
    return nilai / valensi


def gram_ke_mol(massa_gram: float, bm: float) -> float:
    """Hitung jumlah mol dari massa (gram) dan berat molekul."""
    return massa_gram / bm


def hitung_molaritas(massa_gram: float, bm: float, volume_liter: float) -> float:
    """
    Hitung molaritas larutan.
    M = n / V  (mol/L)
    """
    if volume_liter <= 0:
        raise ValueError("Volume harus lebih dari 0 liter.")
    n = gram_ke_mol(massa_gram, bm)
    return n / volume_liter


def hitung_pengenceran(M1: float, V1: float, V2: float) -> float:
    """
    Hitung molaritas setelah pengenceran (M1V1 = M2V2).
    Returns M2.
    """
    if V2 <= 0:
        raise ValueError("Volume akhir harus lebih dari 0.")
    return (M1 * V1) / V2
