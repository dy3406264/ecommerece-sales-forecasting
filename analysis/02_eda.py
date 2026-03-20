# ============================================================
# 02_eda.py
# Project : E-Commerce Sales & Revenue Forecasting
# Author  : Data Analyst Portfolio Project
# Desc    : Exploratory Data Analysis — trends, KPIs, segments
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

# ── Config ───────────────────────────────────────────────────
DATA_PATH  = "data/superstore_clean.csv"
OUTPUT_DIR = "outputs/charts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

PALETTE = ["#2196F3", "#FF5722", "#4CAF50", "#FFC107", "#9C27B0", "#00BCD4"]
sns.set_theme(style="whitegrid", font_scale=1.1)

# ── Load ─────────────────────────────────────────────────────
df = pd.read_csv(DATA_PATH, parse_dates=["order_date"])
print(f"  Loaded {len(df):,} rows\n")

# ════════════════════════════════════════════════════════════
# KPI SUMMARY
# ════════════════════════════════════════════════════════════
print("=" * 55)
print("  📊 KEY PERFORMANCE INDICATORS")
print("=" * 55)
print(f"  Total Revenue    : ${df['sales'].sum():>13,.2f}")
print(f"  Total Profit     : ${df['profit'].sum():>13,.2f}")
print(f"  Avg Order Value  : ${df['sales'].mean():>13,.2f}")
print(f"  Avg Profit Margin: {df['profit_margin'].mean():>12.2f}%")
print(f"  Total Orders     : {df['order_id'].nunique():>13,}")
print(f"  Total Customers  : {df['customer_id'].nunique():>13,}")
print(f"  Total Products   : {df['product_id'].nunique():>13,}")

# ════════════════════════════════════════════════════════════
# CHART 1 — Monthly Revenue Trend
# ════════════════════════════════════════════════════════════
print("\n  [1/7] Monthly Revenue Trend...")
monthly = df.groupby("year_month")["sales"].sum().reset_index()

fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(monthly["year_month"], monthly["sales"],
        color=PALETTE[0], linewidth=2.5, marker="o", markersize=4)
ax.fill_between(monthly["year_month"], monthly["sales"],
                alpha=0.12, color=PALETTE[0])
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
plt.xticks(rotation=45, ha="right", fontsize=8)
ax.set_title("Monthly Revenue Trend", fontsize=15, fontweight="bold", pad=12)
ax.set_xlabel("Month"); ax.set_ylabel("Revenue ($)")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/01_monthly_revenue.png", dpi=150)
plt.close()
print("     ✔ Saved")

# ════════════════════════════════════════════════════════════
# CHART 2 — Yearly Revenue & Profit
# ════════════════════════════════════════════════════════════
print("  [2/7] Yearly Revenue & Profit...")
yearly = df.groupby("year")[["sales", "profit"]].sum().reset_index()

fig, ax = plt.subplots(figsize=(8, 5))
x = range(len(yearly))
ax.bar([i - 0.2 for i in x], yearly["sales"],  width=0.38, label="Revenue", color=PALETTE[0])
ax.bar([i + 0.2 for i in x], yearly["profit"], width=0.38, label="Profit",  color=PALETTE[2])
ax.set_xticks(list(x)); ax.set_xticklabels(yearly["year"])
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
ax.set_title("Yearly Revenue vs Profit", fontsize=15, fontweight="bold", pad=12)
ax.legend(); plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/02_yearly_revenue_profit.png", dpi=150)
plt.close()
print("     ✔ Saved")

# ════════════════════════════════════════════════════════════
# CHART 3 — Sales & Profit by Category
# ════════════════════════════════════════════════════════════
print("  [3/7] Sales & Profit by Category...")
cat = df.groupby("category")[["sales", "profit"]].sum().reset_index().sort_values("sales", ascending=False)

fig, ax = plt.subplots(figsize=(8, 5))
x = range(len(cat))
ax.bar([i - 0.2 for i in x], cat["sales"],  width=0.38, label="Sales",  color=PALETTE[0])
ax.bar([i + 0.2 for i in x], cat["profit"], width=0.38, label="Profit", color=PALETTE[1])
ax.set_xticks(list(x)); ax.set_xticklabels(cat["category"])
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
ax.set_title("Sales & Profit by Category", fontsize=15, fontweight="bold", pad=12)
ax.legend(); plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/03_category_performance.png", dpi=150)
plt.close()
print("     ✔ Saved")

# ════════════════════════════════════════════════════════════
# CHART 4 — Regional Sales Pie
# ════════════════════════════════════════════════════════════
print("  [4/7] Regional Sales Breakdown...")
region = df.groupby("region")["sales"].sum().reset_index()

fig, ax = plt.subplots(figsize=(7, 7))
ax.pie(region["sales"], labels=region["region"], autopct="%1.1f%%",
       colors=PALETTE[:len(region)], startangle=140,
       wedgeprops=dict(edgecolor="white", linewidth=2))
ax.set_title("Sales by Region", fontsize=15, fontweight="bold", pad=12)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/04_regional_sales.png", dpi=150)
plt.close()
print("     ✔ Saved")

# ════════════════════════════════════════════════════════════
# CHART 5 — Top 10 Products by Revenue
# ════════════════════════════════════════════════════════════
print("  [5/7] Top 10 Products by Revenue...")
top = df.groupby("product_name")["sales"].sum().nlargest(10).reset_index().sort_values("sales")

fig, ax = plt.subplots(figsize=(11, 6))
ax.barh(top["product_name"], top["sales"], color=PALETTE[0])
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
ax.set_title("Top 10 Products by Revenue", fontsize=15, fontweight="bold", pad=12)
ax.set_xlabel("Revenue ($)"); plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/05_top_products.png", dpi=150)
plt.close()
print("     ✔ Saved")

# ════════════════════════════════════════════════════════════
# CHART 6 — Profit Margin by Sub-Category
# ════════════════════════════════════════════════════════════
print("  [6/7] Profit Margin by Sub-Category...")
sub = df.groupby("sub_category")["profit_margin"].mean().reset_index().sort_values("profit_margin", ascending=False)
colors = [PALETTE[2] if v >= 0 else PALETTE[1] for v in sub["profit_margin"]]

fig, ax = plt.subplots(figsize=(11, 6))
ax.bar(sub["sub_category"], sub["profit_margin"], color=colors)
ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
ax.set_title("Avg Profit Margin by Sub-Category", fontsize=15, fontweight="bold", pad=12)
ax.set_ylabel("Profit Margin (%)"); plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/06_subcategory_margin.png", dpi=150)
plt.close()
print("     ✔ Saved")

# ════════════════════════════════════════════════════════════
# CHART 7 — Discount vs Profit Scatter
# ════════════════════════════════════════════════════════════
print("  [7/7] Discount vs Profit Scatter...")
fig, ax = plt.subplots(figsize=(9, 5))
sc = ax.scatter(df["discount"], df["profit"], alpha=0.3,
                c=df["sales"], cmap="Blues", s=20)
plt.colorbar(sc, label="Sales ($)")
ax.axhline(0, color="red", linestyle="--", linewidth=1)
ax.set_title("Discount vs Profit  (colour = Sales value)", fontsize=15, fontweight="bold", pad=12)
ax.set_xlabel("Discount Rate"); ax.set_ylabel("Profit ($)")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/07_discount_vs_profit.png", dpi=150)
plt.close()
print("     ✔ Saved")

# ════════════════════════════════════════════════════════════
# SEGMENT BREAKDOWN TABLE
# ════════════════════════════════════════════════════════════
print("\n" + "=" * 55)
print("  📋 SALES BY CUSTOMER SEGMENT")
print("=" * 55)
seg = df.groupby("segment").agg(
    Revenue=("sales", "sum"),
    Profit=("profit", "sum"),
    Orders=("order_id", "nunique"),
    Avg_Margin=("profit_margin", "mean")
).reset_index()
seg["Revenue"] = seg["Revenue"].map("${:,.2f}".format)
seg["Profit"]  = seg["Profit"].map("${:,.2f}".format)
seg["Avg_Margin"] = seg["Avg_Margin"].map("{:.2f}%".format)
print(seg.to_string(index=False))

print("\n  EDA Complete! ✅\n")
print(f"  All charts saved → {OUTPUT_DIR}/")
