"""
Acquire/validate core Democracy + Economy blocks.
Canonical period: 2000-2023; 50 states; no interpolation.

This script is intentionally source-explicit. It does not mark a block acquired
unless the raw response/file is successfully read and validation gates pass.
"""

from pathlib import Path
import hashlib
import pandas as pd

YEARS = list(range(2000, 2024))
EXPECTED_ROWS = 50 * len(YEARS)

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def validate_panel(df, state_col="state", year_col="year", value_col=None):
    x = df.copy()
    x[year_col] = pd.to_numeric(x[year_col], errors="raise").astype(int)
    x = x[x[year_col].isin(YEARS)]
    if x.duplicated([state_col, year_col]).any():
        raise ValueError("Duplicate state-year keys detected")
    states = sorted(x[state_col].dropna().unique())
    report = {
        "rows": len(x),
        "states": len(states),
        "years": x[year_col].nunique(),
        "expected_rows": EXPECTED_ROWS,
        "complete_key_grid": len(x) == EXPECTED_ROWS and len(states) == 50 and x[year_col].nunique() == 24,
    }
    if value_col:
        report["value_missing"] = int(x[value_col].isna().sum())
    return x, report

def validate_sdi(raw_csv):
    df = pd.read_csv(raw_csv)
    required = {
        "state", "year", "democracy_mcmc",
        "democracy_mcmc_sd", "democracy_mcmc_se", "democracy_additive"
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"SDI missing required columns: {sorted(missing)}")
    x, report = validate_panel(df, value_col="democracy_mcmc")
    report["sha256"] = sha256_file(raw_csv)
    return x, report

def validate_bea_e1(df, state_col="state", year_col="year", value_col="real_gdp"):
    x, report = validate_panel(df, state_col, year_col, value_col)
    if report["value_missing"]:
        raise ValueError("BEA E1 contains missing canonical real-GDP values")
    return x, report

if __name__ == "__main__":
    print("Validator ready. No acquisition is claimed until source files are supplied/read successfully.")
