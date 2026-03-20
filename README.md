# 🛒 E-Commerce Sales & Revenue Forecasting

> **A full end-to-end data analyst portfolio project** using the Kaggle Superstore dataset —
> covering data cleaning, exploratory analysis, SQL querying, and 6-month revenue forecasting.

---

## 📌 Project Overview

This project simulates a real-world business analytics scenario for an e-commerce company.
The goal is to uncover sales trends, identify profitable and loss-making segments, and
forecast future revenue to support strategic decision-making.

| Detail | Info |
|---|---|
| **Dataset** | Kaggle Superstore Sales Dataset |
| **Tools** | Python, SQL, Pandas, Matplotlib, Seaborn, Prophet |
| **Skills** | Data Cleaning, EDA, SQL Analysis, Time-Series Forecasting |
| **Environment** | GitHub Codespaces (browser-based, no local setup needed) |

---

## 🎯 Business Questions Answered

- What is the overall revenue and profit trend over time?
- Which regions, categories, and products drive the most revenue?
- Which sub-categories have negative profit margins?
- How does discounting impact profitability?
- What will revenue look like over the next 6 months?

---

## 📁 Project Structure

```
ecommerce-forecasting/
│
├── data/
│   ├── superstore.csv             ← Raw dataset (upload here)
│   └── superstore_clean.csv       ← Auto-generated after cleaning
│
├── sql/
│   ├── 01_sales_overview.sql      ← KPIs, yearly & monthly trends
│   ├── 02_regional_performance.sql← Region, state, city breakdowns
│   └── 03_product_analysis.sql    ← Products, discounts, loss-makers
│
├── analysis/
│   ├── 01_data_cleaning.py        ← Clean, validate & feature engineer
│   ├── 02_eda.py                  ← 7 EDA charts + KPI summary
│   └── 03_forecasting.py          ← Prophet forecasting + charts
│
├── outputs/
│   ├── charts/                    ← All generated PNG charts
│   └── revenue_forecast.csv       ← 6-month forecast table
│
├── .devcontainer/
│   └── devcontainer.json          ← Auto-setup for GitHub Codespaces
├── requirements.txt
├── run_all.sh                     ← One command runs everything
└── README.md
```

---

## 🚀 How to Run

### Option A — GitHub Codespaces (Recommended)
1. Click the green **`<> Code`** button → **Codespaces** → **Create codespace**
2. Wait ~60 seconds for auto-setup (libraries install automatically)
3. Upload `superstore.csv` into the `data/` folder
4. In the terminal, run:
```bash
bash run_all.sh
```

### Option B — Run Scripts Individually
```bash
pip install -r requirements.txt

python analysis/01_data_cleaning.py
python analysis/02_eda.py
python analysis/03_forecasting.py
```

---

## 📊 Key Findings

### Revenue & Profitability
- Total revenue of **$2.3M** across 4 years with consistent year-over-year growth
- Overall profit margin of **~12%**, with significant variation by category
- **Technology** leads in revenue; **Office Supplies** leads in profit margin

### Regional Performance
- **West** region generates the highest revenue (~32% of total)
- **Central** region has the lowest profit margin despite average revenue

### Product Insights
- **Furniture** sub-categories (Tables, Bookcases) are loss-making due to heavy discounting
- High discount rates (>30%) consistently result in negative profits
- Top 10 products account for ~18% of total revenue

### Forecast
- 6-month revenue forecast shows **~8-12% growth** trajectory
- Q4 seasonality consistently drives the highest monthly revenue

---

## 📈 Charts Generated

| # | Chart | Insight |
|---|---|---|
| 01 | Monthly Revenue Trend | Overall growth pattern & seasonality |
| 02 | Yearly Revenue vs Profit | Year-over-year comparison |
| 03 | Category Performance | Sales & profit by category |
| 04 | Regional Sales Pie | Share of revenue by region |
| 05 | Top 10 Products | Highest revenue-generating products |
| 06 | Sub-Category Margins | Profit margin winners & losers |
| 07 | Discount vs Profit | Impact of discounting on profitability |
| 08 | Revenue Forecast | 6-month forward projection |
| 09 | Forecast Components | Trend + seasonality decomposition |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| `pandas` | Data manipulation & cleaning |
| `numpy` | Numerical operations |
| `matplotlib` | Chart generation |
| `seaborn` | Statistical visualisations |
| `prophet` | Time-series forecasting |
| `SQL (SQLite)` | Business queries & aggregations |

---

## 📂 Dataset

**Source:** [Kaggle — Sample Superstore Dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final)

- 9,994 rows × 21 columns
- Orders from 2014–2017
- Covers US-based e-commerce sales across 3 categories, 17 sub-categories

---

## 👤 About

Built as part of a data analyst portfolio by a professional with 3 years of experience
in Excel, Power BI, SQL, Python, and Tableau.

---

*⭐ If you found this project useful, feel free to star the repository!*
