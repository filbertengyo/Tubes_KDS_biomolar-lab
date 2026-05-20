"""
Visualisasi hasil analisis osmolaritas plasma.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent.parent / "output"


def plot_kontribusi_ion(kontribusi: dict, sample_id: str = ""):
    """Bar chart kontribusi osmotik tiap ion."""
    label_map = {"na": "Na⁺", "k": "K⁺", "cl": "Cl⁻",
                  "hco3": "HCO₃⁻", "glukosa": "Glukosa", "bun": "BUN"}
    colors = ["#378ADD", "#1D9E75", "#7F77DD", "#D85A30", "#EF9F27", "#D4537E"]

    ions = list(kontribusi.keys())
    vals = list(kontribusi.values())
    labels = [label_map.get(i, i) for i in ions]

    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.barh(labels, vals, color=colors, edgecolor="none", height=0.55)
    ax.bar_label(bars, fmt="%.1f", padding=4, fontsize=10)
    ax.set_xlabel("Kontribusi osmotik (mOsm/kg)")
    ax.set_title(f"Kontribusi ion per sampel {sample_id}", fontsize=12)
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    path = OUTPUT_DIR / f"kontribusi_{sample_id}.png"
    plt.savefig(path, dpi=150)
    plt.close()
    return path


def plot_perbandingan_metode(df_hasil: pd.DataFrame):
    """
    Scatter plot osmolaritas DC vs VH untuk semua sampel.
    Setiap titik diberi label sample_id dan diwarnai berdasarkan status.
    """
    color_map = {"Normal": "#1D9E75", "Hiperosmolar": "#E24B4A", "Hipoosmolar": "#378ADD"}
    colors = [color_map.get(s, "#888780") for s in df_hasil["status"]]

    fig, ax = plt.subplots(figsize=(7, 6))
    ax.scatter(df_hasil["osmolaritas_DC"], df_hasil["osmolaritas_VH"],
               c=colors, s=80, zorder=3)

    # Garis identitas
    lo = min(df_hasil["osmolaritas_DC"].min(), df_hasil["osmolaritas_VH"].min()) - 5
    hi = max(df_hasil["osmolaritas_DC"].max(), df_hasil["osmolaritas_VH"].max()) + 5
    ax.plot([lo, hi], [lo, hi], "--", color="#B4B2A9", linewidth=1, label="Identitas (DC = VH)")

    # Zona normal
    ax.axvspan(275, 295, alpha=0.07, color="#1D9E75", label="Zona normal (275–295)")

    for _, row in df_hasil.iterrows():
        ax.annotate(row["sample_id"], (row["osmolaritas_DC"], row["osmolaritas_VH"]),
                    textcoords="offset points", xytext=(5, 4), fontsize=9)

    patches = [mpatches.Patch(color=c, label=l) for l, c in color_map.items()]
    ax.legend(handles=patches + [plt.Line2D([0],[0], linestyle="--", color="#B4B2A9", label="Identitas")],
              fontsize=9, framealpha=0.5)
    ax.set_xlabel("Osmolaritas Dorwart-Chalmers (mOsm/kg)")
    ax.set_ylabel("Osmolaritas Van't Hoff (mOsm/kg)")
    ax.set_title("Perbandingan dua metode perhitungan osmolaritas", fontsize=12)
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    path = OUTPUT_DIR / "perbandingan_metode.png"
    plt.savefig(path, dpi=150)
    plt.close()
    return path


def plot_osmolal_gap(df_hasil: pd.DataFrame):
    """Bar chart osmolal gap antar sampel."""
    fig, ax = plt.subplots(figsize=(8, 4))
    colors = ["#E24B4A" if g > 10 else "#1D9E75" for g in df_hasil["osmolal_gap"]]
    bars = ax.bar(df_hasil["sample_id"], df_hasil["osmolal_gap"],
                  color=colors, edgecolor="none", width=0.5)
    ax.bar_label(bars, fmt="%.1f", padding=3, fontsize=10)
    ax.axhline(0, color="#B4B2A9", linewidth=0.8, linestyle="--")
    ax.set_ylabel("Osmolal gap (mOsm/kg)")
    ax.set_title("Osmolal gap per sampel (VH − DC)", fontsize=12)
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    path = OUTPUT_DIR / "osmolal_gap.png"
    plt.savefig(path, dpi=150)
    plt.close()
    return path
