#!/bin/bash
# ============================================================
# run_all.sh
# Run the full E-Commerce Sales & Revenue Forecasting pipeline
# Usage: bash run_all.sh
# ============================================================

set -e  # stop on any error

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║   E-Commerce Sales & Revenue Forecasting Pipeline   ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# Create output folders
mkdir -p data outputs/charts

# Check superstore.csv exists
if [ ! -f "data/superstore.csv" ]; then
  echo "  ❌ ERROR: data/superstore.csv not found!"
  echo "  Please upload your Superstore CSV to the data/ folder."
  exit 1
fi

echo "  📦 Installing dependencies..."
pip install -r requirements.txt -q
echo "  ✔ Dependencies ready"
echo ""

echo "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  STEP 1/3 — Data Cleaning"
echo "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python analysis/01_data_cleaning.py

echo "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  STEP 2/3 — Exploratory Data Analysis"
echo "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python analysis/02_eda.py

echo "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  STEP 3/3 — Revenue Forecasting"
echo "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python analysis/03_forecasting.py

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║              Pipeline Complete! ✅                   ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "  📊 Charts   →  outputs/charts/"
echo "  📄 Forecast →  outputs/revenue_forecast.csv"
echo "  🧹 Clean Data → data/superstore_clean.csv"
echo ""
