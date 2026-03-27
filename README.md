## Kitesurf School Analytics

An end-to-end data project — from raw operational data to interactive business dashboard.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-black?logo=pandas)
![SQLite](https://img.shields.io/badge/Database-SQLite-blue?logo=sqlite)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?logo=streamlit)
![Status](https://img.shields.io/badge/Project-Complete-brightgreen)

### Overview
This project simulates and analyzes the operations of a kitesurf school through a complete data pipeline — from synthetic data generation to an interactive Streamlit dashboard. The goal is to demonstrate how data systems and analytics can drive better decisions around pricing, instructor allocation, and seasonal strategy in a real-world business context.

### Project Architecture

seed.py → bookings.csv → watersports.db (SQLite)
                         → analysis.ipynb (pandas)
                         → app.py (Streamlit dashboard)

### Features

- **Data Engineering**
  - Synthetic dataset (300 bookings)
  - Seasonal pricing logic
  - SQLite database

- **Exploratory Analysis**
  - Revenue & profit analysis
  - Seasonality trends
  - Instructor performance
  - Equipment utilization

- **Interactive Dashboard**
  - KPI metrics (revenue, profit, bookings)
  - Filters (sport, instructor, status)
  - Trend visualizations
  - Built-in SQL Explorer

### Key Insights

| Area         | Finding |
|--------------|--------|
| Profitability | Avg. profit ≈ R$273/session; longer sessions yield lower margins |
| Seasonality   | Peak demand in Jan, Jul & Aug; low season in Apr–May |
| Instructors   | Pedro leads in both volume and efficiency; Marcos underperforms |
| Equipment     | Foil board & windsurf drive most revenue; kitesurf gear underutilized |

### Business Recommendations

- Adjust pricing for longer sessions to improve margins  
- Increase marketing during low season (Apr–May)  
- Allocate top instructors to high-value sessions  
- Invest more in high-demand equipment (foil, windsurf)  

### Quick Start
Prerequisites: Python 3.10+

```bash
# 1. Clone the repo
git clone https://github.com/emilly-kelda/kitesurf-school-analytics.git
cd kitesurf-school-analytics

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate the database
python seed.py

# 4. Launch the dashboard
streamlit run app.py
``` 
Optional: Open analysis.ipynb in Jupyter, VS Code, or Google Colab to explore the full analysis.

### Tech Stack
Python · pandas · SQLite · Streamlit · Plotly · Matplotlib

### Skills Demonstrated
Data engineering · Feature engineering · SQL design · Exploratory data analysis · Business storytelling · Dashboard development

### Conclusion

This project demonstrates how raw operational data can be transformed into actionable insights and interactive tools to support real business decisions.
