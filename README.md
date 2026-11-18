🏏 IPL 2026 Stadium Intelligence Dashboard

Statistical Analysis of Stadium Occupancy, Ticket Demand & Revenue Simulation

An interactive sports analytics dashboard developed as part of our **Applied Probability Distributions (APD) Semester Project** at **Symbiosis Statistical Institute, Pune**.

The project demonstrates how probability distributions can be applied to real-world sports analytics to explore stadium occupancy, ticket-booking demand, uncertainty and potential revenue.

Built using **Python, Streamlit, Pandas, NumPy, SciPy and Plotly**.

---

📌 Project Overview

The IPL 2026 Stadium Intelligence Dashboard combines cricket analytics with probability and statistical modelling.

Using a compiled dataset of **74 IPL matches across 13 stadiums**, the dashboard enables users to explore stadium capacities, estimated attendance, indicative ticket prices and probability-based revenue scenarios.

The primary objective is to transform theoretical statistical concepts into interactive, practical applications.

✨ Key Features

📊 1. IPL Overview
- Interactive analysis of 74 IPL matches.
- Stadium-wise estimated attendance and occupancy comparisons.
- Filters for teams, stadiums, match stages and dates.
- Interactive bar charts and scatter plots.

🏟️ 2. Stadium Explorer
- Explore 13 IPL stadiums.
- Stadium seating illustrations and stand-wise pricing information.
- View stadium capacities and estimated occupancy.
- Compare indicative ticket categories.

🎟️ 3. Ticket Pricing Analysis
- Compare ticket-price categories across stadiums.
- Analyse minimum, median and maximum listed prices.
- Interactive visualisations of price variation.

🧪 4. Probability Distribution Lab

Binomial Distribution
- Models the number of occupied seats.
- Calculates the probability of achieving a target occupancy.

Beta Distribution
- Represents uncertainty in stadium occupancy percentages.
- Allows users to explore different occupancy assumptions.

Poisson Distribution
- Models hypothetical ticket-booking enquiries per hour.
- Calculates the probability of reaching a specified enquiry count.

💰 5. Monte Carlo Revenue Simulation
- Simulates possible stadium occupancy outcomes.
- Combines Beta and Binomial distributions.
- Estimates hypothetical gross ticket revenue.
- Displays average revenue, percentiles and revenue distributions.

🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive dashboard interface |
| Pandas | Data cleaning and analysis |
| NumPy | Numerical calculations and simulations |
| SciPy | Probability distributions |
| Plotly | Interactive visualisations |
| Excel & CSV | Dataset storage |
| HTML & CSS | Dashboard styling |

📂 Project Structure

IPL-2026-Stadium-Intelligence/
│
├── app.py
├── IPL 2026.xlsx
├── stadium_ticket_prices.csv
├── image_manifest.csv
├── ipl_background.webp
├── stadium_images/
│   └── [13 stadium images]
├── requirements.txt
└── README.md

🚀 Installation and Setup

1. Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/IPL-2026-Stadium-Intelligence.git
```

2. Navigate to the project**

```bash
cd IPL-2026-Stadium-Intelligence
```

3. Install dependencies**

```bash
pip install -r requirements.txt
```

4. Launch the Streamlit dashboard**

```bash
streamlit run app.py
```

The dashboard will open in your browser, typically at `http://localhost:8501`.

📈 Statistical Concepts Applied

| Distribution | Application |
|---|---|
| Binomial | Stadium seat-occupancy probability |
| Beta | Uncertainty in occupancy rates |
| Poisson | Ticket-booking enquiry frequency |
| Monte Carlo Simulation | Potential ticket revenue outcomes |

🎯 Project Objectives

1. Explore IPL match and stadium information through interactive visualisations.
2. Apply probability distributions to stadium occupancy and booking-demand scenarios.
3. Study uncertainty in occupancy rates.
4. Simulate possible ticket revenue under different assumptions.
5. Demonstrate the practical application of Applied Probability Distributions in sports analytics.

🔍 Key Insights

- Different probability distributions help answer different stadium-management questions.
- Binomial modelling demonstrates the likelihood of reaching specified occupancy targets.
- Beta modelling represents uncertainty in occupancy percentages.
- Poisson modelling demonstrates how booking-enquiry counts may vary over time.
- Monte Carlo simulation illustrates possible gross revenue outcomes under different assumptions.

⚠️ Data Disclaimer

This project is intended for academic and educational purposes.

- Stadium attendance figures are **modelled estimates**, not verified match-day attendance.
- Ticket prices are **indicative and illustrative**, not confirmed prices for every match.
- Booking-enquiry rates are hypothetical.
- Revenue calculations represent simulated scenarios rather than actual IPL earnings.
- Probability model parameters have not been validated against observed ticket sales.

🎓 Academic Information

Institution: Symbiosis Statistical Institute, Pune  
Programme: M.Sc. Applied Statistics with Data Science  
Course: Applied Probability Distributions (APD)  
Project: IPL 2026 Stadium Intelligence Dashboard

🌟 Conclusion

This project demonstrates how statistical distributions and simulation techniques can be integrated into an interactive dashboard to explore sports management problems.

By combining probability theory, data visualisation and Python-based development, the dashboard provides an educational framework for understanding stadium occupancy, ticket-booking demand and potential revenue under uncertainty.

---

⭐ If you found this project interesting, consider starring the repository!
