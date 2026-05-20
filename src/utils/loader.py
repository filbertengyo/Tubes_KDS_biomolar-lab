"""
Load dataset dari file CSV.
"""
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent.parent / "data"


def load_plasma_samples() -> pd.DataFrame:
    """Load semua sampel plasma dari CSV."""
    return pd.read_csv(DATA_DIR / "plasma_samples.csv")


def load_sample_by_id(sample_id: str) -> dict:
    """Load satu sampel berdasarkan ID."""
    df = load_plasma_samples()
    row = df[df["sample_id"] == sample_id]
    if row.empty:
        raise ValueError(f"Sample ID '{sample_id}' tidak ditemukan.")
    return row.iloc[0].to_dict()
