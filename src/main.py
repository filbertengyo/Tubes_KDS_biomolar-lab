"""
BioMolar Lab — Analisis Molaritas dan Osmolaritas Larutan Biologis
IF3211 Domain-Specific Computation
"""
import pandas as pd
from src.utils.loader import load_plasma_samples
from src.modules.osmolaritas import dorwart_chalmers, vant_hoff_extended, kontribusi_per_ion
from src.modules.klasifikasi import ringkasan_sampel
from src.modules.visualisasi import plot_perbandingan_metode, plot_osmolal_gap, plot_kontribusi_ion


def analisis_semua_sampel() -> pd.DataFrame:
    """Jalankan analisis osmolaritas untuk seluruh dataset."""
    df = load_plasma_samples()
    hasil_list = []

    for _, row in df.iterrows():
        sampel = row.to_dict()
        osm_dc = dorwart_chalmers(row["na"], row["glukosa_mgdl"], row["bun_mgdl"])
        osm_vh = vant_hoff_extended(row["na"], row["k"], row["cl"],
                                     row["hco3"], row["glukosa_mgdl"], row["bun_mgdl"])
        ringkasan = ringkasan_sampel(row["sample_id"], sampel, osm_dc, osm_vh)
        hasil_list.append(ringkasan)

        contrib = kontribusi_per_ion(row["na"], row["k"], row["cl"],
                                      row["hco3"], row["glukosa_mgdl"], row["bun_mgdl"])
        plot_kontribusi_ion(contrib, row["sample_id"])

    df_hasil = pd.DataFrame(hasil_list)
    return df_hasil


def cetak_hasil(df_hasil: pd.DataFrame):
    print("\n" + "="*60)
    print("  HASIL ANALISIS OSMOLARITAS PLASMA")
    print("="*60)
    for _, row in df_hasil.iterrows():
        print(f"\n[{row['sample_id']}] {row['kondisi_dataset']}")
        print(f"  Osmolaritas DC : {row['osmolaritas_DC']:.2f} mOsm/kg")
        print(f"  Osmolaritas VH : {row['osmolaritas_VH']:.2f} mOsm/kg")
        print(f"  Osmolal gap    : {row['osmolal_gap']:.2f} mOsm/kg")
        print(f"  Status         : {row['status']}")
        print(f"  Kondisi klinis : {', '.join(row['kondisi_klinis'])}")
    print("\n" + "="*60)


if __name__ == "__main__":
    print("Memuat dataset...")
    df_hasil = analisis_semua_sampel()

    cetak_hasil(df_hasil)

    print("\nMembuat visualisasi...")
    plot_perbandingan_metode(df_hasil)
    plot_osmolal_gap(df_hasil)

    df_hasil.to_csv("output/hasil_analisis.csv", index=False)
    print("Selesai. Output tersimpan di folder output/")
