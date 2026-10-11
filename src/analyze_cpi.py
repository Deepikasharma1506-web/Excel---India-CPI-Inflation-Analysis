from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TABLES = ROOT / "outputs" / "tables"
CHARTS = ROOT / "outputs" / "charts"
TABLES.mkdir(parents=True, exist_ok=True)
CHARTS.mkdir(parents=True, exist_ok=True)

MONTH_FIX = {"Marcrh": "March"}
FOOD_COMPONENTS = [
    "Cereals and products", "Meat and fish", "Egg", "Milk and products",
    "Oils and fats", "Fruits", "Vegetables", "Pulses and products",
    "Sugar and Confectionery", "Spices", "Non-alcoholic beverages",
    "Prepared meals, snacks, sweets etc."
]

def save_chart(path):
    plt.tight_layout()
    plt.savefig(path, dpi=160, bbox_inches="tight")
    plt.close()

def main():
    raw = pd.read_csv(DATA / "all_india_cpi_index.csv")
    df = raw.copy()
    df["Month"] = df["Month"].astype(str).str.strip().replace(MONTH_FIX)
    value_cols = list(df.columns[3:])
    for col in value_cols:
        df[col] = pd.to_numeric(df[col].replace("-", np.nan), errors="coerce")
    df["Date"] = pd.to_datetime(df["Year"].astype(str) + "-" + df["Month"] + "-01", errors="coerce")
    df = df[["Date", "Sector", "Year", "Month"] + value_cols]
    df = df.sort_values(["Date", "Sector"]).reset_index(drop=True)
    df.to_csv(TABLES / "cleaned_cpi_data.csv", index=False)

    missing = df.isna().sum().rename_axis("Column").reset_index(name="Missing cells")
    missing.to_csv(TABLES / "missing_value_audit.csv", index=False)

    ru = df[df["Sector"].eq("Rural+Urban")].sort_values("Date").copy().reset_index(drop=True)
    ru["YoY General Inflation %"] = ru["General index"].pct_change(12, fill_method=None) * 100
    ru["MoM General Change %"] = ru["General index"].pct_change(fill_method=None) * 100
    ru["YoY Food Inflation %"] = ru["Food and beverages"].pct_change(12, fill_method=None) * 100
    ru["MoM Food Change %"] = ru["Food and beverages"].pct_change(fill_method=None) * 100

    trend = ru.loc[ru["Date"].ge("2017-01-01"),
                   ["Date", "General index", "YoY General Inflation %", "MoM General Change %",
                    "Food and beverages", "YoY Food Inflation %", "MoM Food Change %"]]
    trend.to_csv(TABLES / "monthly_yoy_mom_trends.csv", index=False)

    # Q1: equal-weight proxy; no official expenditure weights are present.
    latest = ru.dropna(subset=["General index"]).iloc[-1]
    buckets = {
        "Food": FOOD_COMPONENTS,
        "Pan, tobacco & intoxicants": ["Pan, tobacco and intoxicants"],
        "Clothing & footwear": ["Clothing", "Footwear"],
        "Housing": ["Housing"],
        "Fuel & light": ["Fuel and light"],
        "Household goods & services": ["Household goods and services"],
        "Health": ["Health"],
        "Transport & communication": ["Transport and communication"],
        "Recreation & amusement": ["Recreation and amusement"],
        "Education": ["Education"],
        "Personal care & effects": ["Personal care and effects"],
    }
    rows = []
    for bucket, cols in buckets.items():
        vals = latest[cols].astype(float)
        rows.append({
            "Broader category": bucket,
            "Latest month": latest["Date"].strftime("%Y-%m"),
            "Average index": vals.mean(),
            "Available component count": int(vals.notna().sum()),
            "Underlying columns": "; ".join(cols),
        })
    broad = pd.DataFrame(rows)
    denom = broad["Average index"].sum(min_count=1)
    broad["Equal-weight proxy contribution %"] = broad["Average index"] / denom * 100
    broad["Caveat"] = "Proxy only; official expenditure weights are not supplied."
    broad.to_csv(TABLES / "broad_category_proxy.csv", index=False)

    # Q2: monthly YoY trend and annual-average YoY comparison.
    annual_rows = []
    for year in sorted(ru["Year"].dropna().unique()):
        year = int(year)
        if year < 2017:
            continue
        current = ru.loc[ru["Year"].eq(year), "General index"].mean()
        previous = ru.loc[ru["Year"].eq(year - 1), "General index"].mean()
        annual_rows.append({
            "Year": year,
            "Annual average General Index": current,
            "Previous year annual average": previous,
            "Annual average change %": (current / previous - 1) * 100 if pd.notna(previous) and previous else np.nan
        })
    pd.DataFrame(annual_rows).to_csv(TABLES / "annual_average_inflation.csv", index=False)

    plot = trend.dropna(subset=["YoY General Inflation %"])
    plt.figure(figsize=(11, 5))
    plt.plot(plot["Date"], plot["YoY General Inflation %"], linewidth=1.8)
    plt.title("India CPI: Monthly YoY General Inflation (Rural+Urban)")
    plt.xlabel("Month"); plt.ylabel("YoY change (%)"); plt.grid(True, alpha=.25)
    save_chart(CHARTS / "monthly_yoy_general_inflation.png")

    # Q3: 12 months ending May 2023.
    food12 = ru[ru["Date"].between("2022-06-01", "2023-05-01")].copy()
    food12["MoM food change (index points)"] = food12["Food and beverages"].diff()
    food12["MoM food inflation %"] = food12["Food and beverages"].pct_change(fill_method=None) * 100
    food12[["Date", "Food and beverages", "MoM food change (index points)", "MoM food inflation %"]].to_csv(
        TABLES / "food_inflation_jun2022_may2023.csv", index=False)
    start = ru.loc[ru["Date"].eq(pd.Timestamp("2022-06-01"))].iloc[0]
    end = ru.loc[ru["Date"].eq(pd.Timestamp("2023-05-01"))].iloc[0]
    food_rows = []
    for col in FOOD_COMPONENTS:
        a, b = start[col], end[col]
        food_rows.append({
            "Food subcategory": col, "Index Jun-2022": a, "Index May-2023": b,
            "Index-point change": b-a,
            "Percent change": (b/a-1)*100 if pd.notna(a) and a != 0 and pd.notna(b) else np.nan
        })
    pd.DataFrame(food_rows).to_csv(TABLES / "food_component_changes.csv", index=False)
    plt.figure(figsize=(10, 5))
    plt.plot(food12["Date"], food12["Food and beverages"], marker="o")
    plt.title("Food & Beverages CPI Index (June 2022–May 2023)")
    plt.xlabel("Month"); plt.ylabel("Index"); plt.grid(True, alpha=.25)
    save_chart(CHARTS / "food_index_12_months.png")

    # Q4: average YoY changes across specified periods.
    covid = ru[ru["Date"].ge("2017-01-01")].copy()
    for col, label in [
        ("General index", "General YoY %"), ("Food and beverages", "Food YoY %"),
        ("Health", "Health YoY %"), ("Fuel and light", "Fuel YoY %"),
        ("Transport and communication", "Transport YoY %")
    ]:
        covid[label] = covid[col].pct_change(12, fill_method=None) * 100
    periods = [
        ("Pre-COVID comparison (Mar 2019-Feb 2020)", "2019-03-01", "2020-02-01"),
        ("COVID onset/year 1 (Mar 2020-Feb 2021)", "2020-03-01", "2021-02-01"),
        ("Year 2 (Mar 2021-Feb 2022)", "2021-03-01", "2022-02-01"),
        ("Inflation surge (Mar 2022-Feb 2023)", "2022-03-01", "2023-02-01"),
    ]
    period_rows = []
    for label, start_date, end_date in periods:
        sub = covid[covid["Date"].between(start_date, end_date)]
        period_rows.append({
            "Period": label,
            "Average General YoY %": sub["General YoY %"].mean(),
            "Average Food YoY %": sub["Food YoY %"].mean(),
            "Average Health YoY %": sub["Health YoY %"].mean(),
            "Average Fuel YoY %": sub["Fuel YoY %"].mean(),
            "Average Transport YoY %": sub["Transport YoY %"].mean(),
            "Months with General YoY data": sub["General YoY %"].count(),
        })
    pd.DataFrame(period_rows).to_csv(TABLES / "covid_period_comparison.csv", index=False)
    covid[["Date", "General YoY %", "Food YoY %", "Health YoY %", "Fuel YoY %", "Transport YoY %"]].to_csv(
        TABLES / "covid_monthly_trends.csv", index=False)

    # Q5: oil changes joined with national CPI.
    oil = pd.read_csv(DATA / "indian_basket_crude_oil.csv", parse_dates=["Date"])
    merged = oil.merge(ru[["Date", "General index", "Fuel and light",
                           "Transport and communication", "Food and beverages"]], on="Date", how="left")
    merged["Oil MoM change %"] = merged["Indian_Basket_USD_per_barrel"].pct_change(fill_method=None) * 100
    for col in ["General index", "Fuel and light", "Transport and communication", "Food and beverages"]:
        merged[col + " MoM change %"] = merged[col].pct_change(fill_method=None) * 100
    merged.to_csv(TABLES / "oil_cpi_monthly_changes_and_correlations.csv", index=False)
    pairs = [
        ("General index MoM change %", "General index"),
        ("Fuel and light MoM change %", "Fuel and light"),
        ("Transport and communication MoM change %", "Transport and communication"),
        ("Food and beverages MoM change %", "Food and beverages"),
    ]
    corrs = []
    for change_col, name in pairs:
        corrs.append({"CPI category": name,
                      "Correlation with oil MoM change": merged["Oil MoM change %"].corr(merged[change_col])})
    pd.DataFrame(corrs).to_csv(TABLES / "oil_cpi_correlations.csv", index=False)
    plt.figure(figsize=(10, 5))
    plt.plot(merged["Date"], merged["Oil MoM change %"], label="Indian Basket crude oil")
    plt.plot(merged["Date"], merged["Fuel and light MoM change %"], label="CPI Fuel & Light")
    plt.axhline(0, linewidth=.8)
    plt.title("Monthly percentage changes: crude oil and CPI Fuel & Light")
    plt.xlabel("Month"); plt.ylabel("MoM change (%)"); plt.legend(); plt.grid(True, alpha=.25)
    save_chart(CHARTS / "oil_vs_fuel_mom_changes.png")

    print("Analysis complete.")
    print(f"Latest CPI month: {latest['Date']:%B %Y}")
    print(f"Outputs saved under: {ROOT / 'outputs'}")
    print("Reminder: broad-category percentages are an equal-weight proxy, not official CPI weights.")

if __name__ == "__main__":
    main()
