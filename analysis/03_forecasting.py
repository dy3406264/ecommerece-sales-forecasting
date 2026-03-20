# ============================================================
# 03_forecasting.py
# Project : E-Commerce Sales & Revenue Forecasting
# Author  : Data Analyst Portfolio Project
# Desc    : Time-series revenue forecasting using Prophet
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os, warnings
warnings.filterwarnings("ignore")

try:
    from prophet import Prophet
except ImportError:
    print("  Installing Prophet...")
    os.system("pip install prophet -q")
    from prophet import Prophet

# ── Config ───────────────────────────────────────────────────
DATA_PATH       = "data/superstore_clean.csv"
OUTPUT_DIR      = "outputs/charts"
FORECAST_MONTHS = 6
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs("outputs", exist_ok=True)

# ── Load ─────────────────────────────────────────────────────
df = pd.read_csv(DATA_PATH, parse_dates=["order_date"])
print(f"  Loaded {len(df):,} rows")

# ════════════════════════════════════════════════════════════
# PREPARE monthly series  →  ds / y  (Prophet format)
# ════════════════════════════════════════════════════════════
monthly = (
    df.groupby(df["order_date"].dt.to_period("M"))["sales"]
    .sum().reset_index()
)
monthly["order_date"] = monthly["order_date"].dt.to_timestamp()
monthly.rename(columns={"order_date": "ds", "sales": "y"}, inplace=True)
monthly.sort_values("ds", inplace=True)

print(f"  Monthly points : {len(monthly)}")
print(f"  Range          : {monthly['ds'].min().date()} → {monthly['ds'].max().date()}")

# ════════════════════════════════════════════════════════════
# TRAIN
# ════════════════════════════════════════════════════════════
print("\n  Training Prophet model...")
model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=False,
    daily_seasonality=False,
    changepoint_prior_scale=0.1,
    seasonality_prior_scale=10,
    interval_width=0.90
)
model.fit(monthly)
print("  ✔ Model trained")

# ════════════════════════════════════════════════════════════
# FORECAST
# ════════════════════════════════════════════════════════════
future   = model.make_future_dataframe(periods=FORECAST_MONTHS, freq="MS")
forecast = model.predict(future)

merged = forecast[["ds","yhat","yhat_lower","yhat_upper"]].merge(
    monthly[["ds","y"]], on="ds", how="left"
)

forecast_start = monthly["ds"].max()

# ════════════════════════════════════════════════════════════
# CHART 1 — Full Forecast
# ════════════════════════════════════════════════════════════
print("\n  Generating charts...")
fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(merged["ds"], merged["y"],
        label="Actual Revenue", color="#2196F3", linewidth=2.5,
        marker="o", markersize=4)
ax.plot(merged["ds"], merged["yhat"],
        label="Forecast", color="#FF5722", linewidth=2, linestyle="--")
ax.fill_between(merged["ds"], merged["yhat_lower"], merged["yhat_upper"],
                alpha=0.15, color="#FF5722", label="90% Confidence Interval")
ax.axvline(forecast_start, color="gray", linestyle=":", linewidth=1.5, label="Forecast Start")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
ax.set_title(f"Revenue Forecast — Next {FORECAST_MONTHS} Months",
             fontsize=15, fontweight="bold", pad=12)
ax.set_xlabel("Date"); ax.set_ylabel("Revenue ($)")
ax.legend(); plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/08_revenue_forecast.png", dpi=150)
plt.close()
print("  ✔ 08_revenue_forecast.png saved")

# ════════════════════════════════════════════════════════════
# CHART 2 — Components
# ════════════════════════════════════════════════════════════
fig2 = model.plot_components(forecast)
fig2.suptitle("Forecast Components (Trend + Seasonality)", fontsize=13, fontweight="bold")
fig2.tight_layout()
fig2.savefig(f"{OUTPUT_DIR}/09_forecast_components.png", dpi=150)
plt.close()
print("  ✔ 09_forecast_components.png saved")

# ════════════════════════════════════════════════════════════
# FORECAST TABLE
# ════════════════════════════════════════════════════════════
future_only = forecast[forecast["ds"] > forecast_start][
    ["ds","yhat","yhat_lower","yhat_upper"]
].copy()
future_only.columns = ["Month","Forecasted Revenue","Lower Bound","Upper Bound"]
future_only["Month"]              = future_only["Month"].dt.strftime("%b %Y")
future_only["Forecasted Revenue"] = future_only["Forecasted Revenue"].map("${:,.2f}".format)
future_only["Lower Bound"]        = future_only["Lower Bound"].map("${:,.2f}".format)
future_only["Upper Bound"]        = future_only["Upper Bound"].map("${:,.2f}".format)

print("\n" + "=" * 60)
print(f"  REVENUE FORECAST — NEXT {FORECAST_MONTHS} MONTHS")
print("=" * 60)
print(future_only.to_string(index=False))

future_only.to_csv("outputs/revenue_forecast.csv", index=False)
print("\n  ✔ Forecast table → outputs/revenue_forecast.csv")
print("\n  Forecasting Complete! ✅\n")
