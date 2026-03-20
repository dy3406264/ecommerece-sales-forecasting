# ============================================================
# 01_data_cleaning.py
# Project : E-Commerce Sales & Revenue Forecasting
# Author  : Data Analyst Portfolio Project
# Desc    : Load, clean and validate the Superstore dataset
# ============================================================

import pandas as pd
import numpy as np
import os

# ── Config ───────────────────────────────────────────────────
RAW_PATH    = "data/superstore.csv"
OUTPUT_PATH = "data/superstore_clean.csv"

# ── 1. Load ───────────────────────────────────────────────────
print("=" * 55)
print("  STEP 1: Loading dataset...")
print("=" * 55)

df = pd.read_csv(RAW_PATH, encoding="latin-1")
print(f"  Rows    : {df.shape[0]}")
print(f"  Columns : {df.shape[1]}")

# ── 2. Inspect ────────────────────────────────────────────────
print("\n  STEP 2: Column Overview")
print("=" * 55)
print(df.dtypes)

print("\n  Missing Values:")
missing = df.isnull().sum()
print(missing[missing > 0] if missing.any() else "  None ✔")

print(f"\n  Duplicate Rows: {df.duplicated().sum()}")

# ── 3. Clean ──────────────────────────────────────────────────
print("\n  STEP 3: Cleaning...")
print("=" * 55)

# Standardise column names → snake_case
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("-", "_")
)
print("  ✔ Column names standardised")

# Parse dates
df["order_date"] = pd.to_datetime(df["order_date"], dayfirst=False)
df["ship_date"]  = pd.to_datetime(df["ship_date"],  dayfirst=False)
print("  ✔ Dates parsed")

# Drop duplicates
before = len(df)
df.drop_duplicates(inplace=True)
print(f"  ✔ Duplicates removed : {before - len(df)} rows dropped")

# Drop rows where revenue / profit are null
df.dropna(subset=["sales", "profit"], inplace=True)
print("  ✔ Null sales/profit rows dropped")

# Enforce numeric types
for col in ["sales", "profit", "quantity", "discount"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")
print("  ✔ Numeric types enforced")

# ── 4. Feature Engineering ────────────────────────────────────
print("\n  STEP 4: Feature Engineering...")
print("=" * 55)

df["year"]          = df["order_date"].dt.year
df["month"]         = df["order_date"].dt.month
df["month_name"]    = df["order_date"].dt.strftime("%b")
df["quarter"]       = df["order_date"].dt.quarter
df["year_month"]    = df["order_date"].dt.to_period("M").astype(str)
df["profit_margin"] = (df["profit"] / df["sales"].replace(0, np.nan)) * 100
df["shipping_days"] = (df["ship_date"] - df["order_date"]).dt.days

print("  ✔ year, month, quarter, year_month")
print("  ✔ profit_margin (%)")
print("  ✔ shipping_days")

# ── 5. Summary ────────────────────────────────────────────────
print("\n  STEP 5: Final Summary")
print("=" * 55)
print(f"  Rows          : {df.shape[0]:,}")
print(f"  Columns       : {df.shape[1]}")
print(f"  Date Range    : {df['order_date'].min().date()} → {df['order_date'].max().date()}")
print(f"  Total Revenue : ${df['sales'].sum():,.2f}")
print(f"  Total Profit  : ${df['profit'].sum():,.2f}")
print(f"  Avg Margin    : {df['profit_margin'].mean():.2f}%")

# ── 6. Save ───────────────────────────────────────────────────
os.makedirs("data", exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False)
print(f"\n  ✔ Clean file saved → {OUTPUT_PATH}")
print("\n  Data Cleaning Complete! ✅\n")
