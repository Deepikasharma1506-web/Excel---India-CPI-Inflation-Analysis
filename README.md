# 📊 India CPI Inflation Analysis (2013–2023)

## 📌 Project Overview

This project analyzes India's Consumer Price Index (CPI) data to understand inflation trends, food price movements, category-level changes, and the relationship between crude oil prices and inflation.

Using Microsoft Excel and Python, the project explores historical CPI data to identify meaningful patterns and generate data-driven insights into India's inflation trends.

## 🎯 Project Objectives

- Analyze year-over-year (YoY) and month-over-month (MoM) CPI inflation.
- Compare broad consumer categories such as food, healthcare, fuel, education, and transportation.
- Investigate food inflation trends over a 12-month period.
- Examine CPI movements before and after the onset of COVID-19.
- Explore the relationship between international crude oil price fluctuations and CPI category changes.
- Clean and organize data for accurate analysis and visualization.

## 📂 Dataset Description

The primary dataset contains All-India CPI index values for Rural, Urban, and Rural+Urban sectors.

- **Time period:** January 2013 – May 2023
- **Sectors:** Rural, Urban, Rural+Urban
- **Data source:** All-India CPI dataset based on Government of India statistics
- **Additional dataset:** Monthly Indian Basket crude oil prices in USD per barrel for January 2021 – May 2023

**Important:** CPI index values represent relative price levels, not direct prices in rupees.

## 🛠️ Tools & Technologies

- **Microsoft Excel:** Data cleaning, formulas, percentage calculations, tables, and charts
- **Python:** Data analysis and visualization
- **Pandas:** Data manipulation and cleaning
- **NumPy:** Numerical calculations
- **Matplotlib:** Trend visualization
- **Statistical Analysis:** Percentage changes and correlation analysis

## 🔍 Analysis Performed

### 1. Broad-Category CPI Analysis

Grouped similar CPI components into broader categories, including Food, Clothing & Footwear, Fuel & Light, Healthcare, Education, and Transportation.

Calculated normalized equal-weight proxy percentages to compare category index levels.

**Limitation:** These percentages are analytical proxies, not official CPI expenditure weights or weighted contributions.

### 2. Year-over-Year Inflation Analysis

Calculated monthly YoY inflation using:

`YoY Inflation (%) = ((Current Month Index / Same Month Previous Year Index) - 1) × 100`

Analyzed General Index trends from 2017 onward to identify periods of relatively high inflation.

### 3. Food Inflation Analysis

Analyzed food inflation for the 12 months ending May 2023.

- Calculated monthly changes in the Food and Beverages index.
- Compared food subcategory index values between June 2022 and May 2023.
- Identified categories with the largest index increases and decreases.

### 4. COVID-19 Impact Analysis

Compared CPI inflation trends before and after March 2020.

Examined changes in:

- General CPI
- Food and Beverages
- Healthcare
- Fuel and Light
- Transport and Communication

The analysis is descriptive and does not establish that COVID-19 alone caused changes in inflation.

### 5. Crude Oil Price and Inflation Analysis

Compared monthly Indian Basket crude oil prices with changes in selected CPI categories.

Used correlation analysis to explore relationships between crude oil price fluctuations and CPI movements.

**Note:** Correlation does not imply causation, and indirect or delayed effects may not be captured by contemporaneous correlation.

## 📈 Key Findings

- The dataset enables historical CPI trend analysis across Rural, Urban, and combined sectors.
- YoY inflation highlights changes in the General Index relative to the same month in the previous year.
- Food subcategory comparisons reveal differences in the pace of index increases across food items.
- CPI patterns vary across the pre-COVID, COVID-onset, and later inflation periods.
- Crude oil fluctuations can be examined alongside fuel, transportation, food, and overall CPI changes.
- Missing values and the absence of official category expenditure weights are important limitations when interpreting results.

## 📁 Project Structure

```text
India-CPI-Inflation-Analysis/
│
├── data/
│   ├── all_india_cpi_index.csv
│   └── indian_basket_crude_oil.csv
│
├── src/
│   └── analyze_cpi.py
│
├── outputs/
│   ├── charts/
│   └── tables/
│
├── India_CPI_Inflation_Case_Study_Solved.xlsx
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ How to Run the Project

### Step 1: Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd India-CPI-Inflation-Analysis
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the Analysis

```bash
python src/analyze_cpi.py
```

The script generates processed datasets, analysis tables, and charts in the `outputs/` directory.

## 📚 Data Sources

- [Petroleum Planning & Analysis Cell (PPAC)](https://ppac.gov.in/prices/international-prices-of-crude-oil) — Indian Basket crude oil price reference.
- Government of India CPI statistics — source referenced by the supplied CPI dataset.

## 💡 Skills Demonstrated

- Data Cleaning and Preprocessing
- Exploratory Data Analysis (EDA)
- Microsoft Excel Formulas and Charts
- Python Data Analysis
- Time-Series Percentage Change Analysis
- Correlation Analysis
- Data Visualization
- Analytical Thinking and Insight Generation

## 👩‍💻 Author

**Deepika Sharma**

B.Tech Computer Science Engineering — Artificial Intelligence & Machine Learning

Interested in Data Analytics, Business Intelligence, and Machine Learning.

## ⚠️ Disclaimer

This project is intended for educational and portfolio purposes. Results depend on the supplied datasets, calculation methods, and selected time periods. Equal-weight category percentages should not be interpreted as official CPI expenditure contributions. Validate statistics against authoritative sources before using them in formal research or policy decisions.
