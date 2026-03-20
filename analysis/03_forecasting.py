# ============================================================
# 03_forecasting.py
# Project : E-Commerce Sales & Revenue Forecasting
# Author  : Data Analyst Portfolio Project
# Desc    : Time-series revenue forecasting using statsmodels
#           (Compatible with Python 3.12+)
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os, warnings
warnings.filterwarnings("ignore")

# ── Auto-install if needed ───────────────────────────────────
try:
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
    from statsmodels.tsa.seasonal import seasonal_decompose
except ImportError:
    print("  Installing statsmodels...")
    os.system("pip install statsmodels -q")
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
    from statsmodels.tsa.seasonal import seasonal_decompose

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
# PREPARE — Aggregate to monthly revenue
# ════════════════════════════════════════════════════════════
monthly = (
    df.groupby(df["order_date"].dt.to_period("M"))["sales"]
    .sum()
    .reset_index()
)
monthly["order_date"] = monthly["order_date"].dt.to_timestamp()
monthly = monthly.sort_values("order_date").reset_index(drop=True)
monthly.rename(columns={"order_date": "ds", "sales": "y"}, inplace=True)

# Set datetime index for statsmodels
ts = monthly.set_index("ds")["y"]
ts.index = pd.DatetimeIndex(ts.index.values, freq="MS")

print(f"  Monthly data points : {len(ts)}")
print(f"  Range               : {ts.index.min().date()} → {ts.index.max().date()}")

# ════════════════════════════════════════════════════════════
# MODEL — Holt-Winters Exponential Smoothing
# Best for data with trend + seasonality
# ════════════════════════════════════════════════════════════
print("\n  Training Holt-Winters model...")

model = ExponentialSmoothing(
    ts,
    trend="add",
    seasonal="add",
    seasonal_periods=12,
    initialization_method="estimated"
)
fit = model.fit(optimized=True)
print("  ✔ Model trained")

# ════════════════════════════════════════════════════════════
# FORECAST
# ════════════════════════════════════════════════════════════
forecast_values = fit.forecast(FORECAST_MONTHS)

last_date      = ts.index[-1]
forecast_dates = pd.date_range(
    start=last_date + pd.DateOffset(months=1),
    periods=FORECAST_MONTHS,
    freq="MS"
)
forecast_series = pd.Series(forecast_values.values, index=forecast_dates)

fitted     = fit.fittedvalues
residuals  = ts - fitted
std_resid  = residuals.std()
lower      = forecast_series - 1.5 * std_resid
upper      = forecast_series + 1.5 * std_resid

# ════════════════════════════════════════════════════════════
# CHART 1 — Full Forecast Plot
# ════════════════════════════════════════════════════════════
print("\n  Generating charts...")

fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(ts.index, ts.values,
        label="Actual Revenue", color="#2196F3",
        linewidth=2.5, marker="o", markersize=4)
ax.plot(fitted.index, fitted.values,
        label="Model Fit", color="#4CAF50",
        linewidth=1.5, linestyle="--", alpha=0.7)
ax.plot(forecast_series.index, forecast_series.values,
        label=f"Forecast ({FORECAST_MONTHS} months)",
        color="#FF5722", linewidth=2.5,
        linestyle="--", marker="s", markersize=5)
ax.fill_between(forecast_series.index, lower, upper,
                alpha=0.15, color="#FF5722",
                label="Confidence Interval")
ax.axvline(last_date, color="gray", linestyle=":",
           linewidth=1.5, label="Forecast Start")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
ax.set_title(f"Revenue Forecast — Next {FORECAST_MONTHS} Months",
             fontsize=15, fontweight="bold", pad=12)
ax.set_xlabel("Date")
ax.set_ylabel("Revenue ($)")
ax.legend()
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/08_revenue_forecast.png", dpi=150)
plt.close()
print("  ✔ 08_revenue_forecast.png saved")

# ════════════════════════════════════════════════════════════
# CHART 2 — Seasonal Decomposition
# ════════════════════════════════════════════════════════════
decomp = seasonal_decompose(ts, model="additive", period=12)

fig, axes = plt.subplots(4, 1, figsize=(14, 10))
components = [
    (ts,               "Observed",    "#2196F3"),
    (decomp.trend,     "Trend",       "#FF5722"),
    (decomp.seasonal,  "Seasonality", "#4CAF50"),
    (decomp.resid,     "Residual",    "#9C27B0"),
]
for ax, (data, title, color) in zip(axes, components):
    ax.plot(data.index, data.values, color=color, linewidth=1.8)
    ax.set_ylabel(title, fontsize=10)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    ax.grid(True, alpha=0.3)

axes[0].set_title("Revenue — Seasonal Decomposition",
                  fontsize=14, fontweight="bold", pad=10)
axes[-1].set_xlabel("Date")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/09_seasonal_decomposition.png", dpi=150)
plt.close()
print("  ✔ 09_seasonal_decomposition.png saved")

# ════════════════════════════════════════════════════════════
# FORECAST TABLE
# ════════════════════════════════════════════════════════════
forecast_df = pd.DataFrame({
    "Month"             : forecast_series.index.strftime("%b %Y"),
    "Forecasted Revenue": forecast_series.values,
    "Lower Bound"       : lower.values,
    "Upper Bound"       : upper.values,
})

display_df = forecast_df.copy()
for col in ["Forecasted Revenue", "Lower Bound", "Upper Bound"]:
    display_df[col] = display_df[col].map("${:,.2f}".format)

print("\n" + "=" * 62)
print(f"  REVENUE FORECAST — NEXT {FORECAST_MONTHS} MONTHS")
print("=" * 62)
print(display_df.to_string(index=False))

mae  = np.mean(np.abs(ts.values - fitted.values))
mape = np.mean(np.abs((ts.values - fitted.values) / ts.values)) * 100
print(f"\n  Model Quality:")
print(f"    MAE  (Mean Abs Error)   : ${mae:,.2f}")
print(f"    MAPE (Mean Abs % Error) : {mape:.2f}%")
print(f"    Accuracy                : {100 - mape:.2f}%")

forecast_df.to_csv("outputs/revenue_forecast.csv", index=False)
print("\n  ✔ Forecast saved → outputs/revenue_forecast.csv")
print("\n  Forecasting Complete! ✅\n")
