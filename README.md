# Kitesurf School Analytics — End-to-End Data Project

End-to-end data analytics project: SQL, pandas & Streamlit dashboard for kitesurf school operations

## Overview

This project simulates and analyzes the operations of a kitesurf school using a complete data pipeline:

Data Generation → Database → Analysis → Interactive Dashboard

The goal is to demonstrate how data systems and analytics can improve pricing, operations, and profitability in the watersports industry.

## Project Architecture
seed.py → bookings.csv → SQLite (watersports.db)
        → analysis.ipynb (pandas + insights)
        → app.py (Streamlit dashboard)
        
## Tech Stack
Python (pandas)
SQLite (database)
Streamlit (dashboard)
Plotly & Matplotlib (visualization)

# What This Project Covers

### Data Engineering
Synthetic dataset generation (300 bookings)
Seasonal pricing logic
SQLite database creation

### Data Analysis (Colab / Notebook)
Revenue and profit analysis
Feature engineering (profit, revenue/hour)
Seasonality trends
Instructor performance
Equipment utilization

### Dashboard (Streamlit)
Interactive filters (sport, instructor, status)
KPI metrics (revenue, profit, bookings)
Visual insights:
Revenue by sport and location
Monthly trends
Profit vs duration
Instructor performance
SQL Explorer (run live queries)

## Key Business Insights

### Profitability
Average profit ≈ 273 per session
Profit decreases as session duration increases
→ Pricing inefficiency for longer sessions

### Seasonality
Peak months: January, July, August
Low season: April, May

→ Strong seasonal demand patterns

### Instructor Performance
Pedro: highest total and average profit
Marcos: lowest performance

→ Performance depends on both volume and efficiency

### Efficiency
Short sessions generate higher profit per session
Revenue per hour varies significantly by sport

### Equipment Strategy
Foil board and windsurf board drive most revenue
Kitesurf equipment underutilized

## Business Recommendations
Adjust pricing for longer sessions
Focus on high-margin segments (advanced users)
Optimize instructor allocation
Improve cancellation / no-show policies
Invest in high-demand equipment
Increase marketing during low season

## Skills Demonstrated
Data analysis (pandas)
SQL querying and database design
Feature engineering
Data visualization
Dashboard development (Streamlit)
Business problem solving

### Conclusion

This project demonstrates how raw operational data can be transformed into actionable insights and interactive tools to support decision-making in a real business context.

## How to Run the Project

Follow these steps to run the dashboard locally.

---

### 1. Clone the repository

Open your terminal and run:

```bash
git clone https://github.com/emilly-kelda/kitesurf-school-analytics.git
cd kitesurf-school-analytics
```

---

### 2. Install dependencies

Make sure you have Python installed (recommended: Python 3.10+)

Then run:

```bash
pip install -r requirements.txt
```

---

### 3. Generate the database

Run the script to create and populate the SQLite database:

```bash
python seed.py
```

This will create the file:

```
watersports.db
```

---

### 4. Run the Streamlit app

```bash
streamlit run app.py
```

---

### 5. Open the dashboard

After running the command, Streamlit will show a local URL like:

```
http://localhost:8501
```

Open this link in your browser to access the dashboard.

---

## Optional: Run the analysis notebook

You can explore the data analysis in:

```
analysis.ipynb
```

Open it in:

* Jupyter Notebook
* VS Code
* Google Colab

---

## Common Issues

* If `streamlit` is not found:

```bash
pip install streamlit
```

* If the database is missing:
  → Make sure you ran `python seed.py`

---

## Tip

Use the **filters on the left sidebar** inside the dashboard to explore:

* Different sports
* Instructor performance
* Booking status

---
