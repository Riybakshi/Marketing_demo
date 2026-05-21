# Agentic Campaign Optimization Engine

A Streamlit workshop application demonstrating how an AI agent can autonomously analyze marketing performance data, identify underperforming segments, optimize ad creative, and reallocate budgets.

## Project Structure
- `streamlit_app.py`: Main Streamlit application shell with page navigation.
- `data/data_generation.py`: Generates dummy marketing data and exports it to `data/marketing_data.xlsx`.
- `requirements.txt`: Python dependencies for the project.

## Getting Started
1. Create a Python environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run streamlit_app.py
   ```

## Features
- Interactive campaign dashboard with Plotly charts.
- Anomaly detection page for underperforming segments.
- Simulated AI agent creative optimization.
- Budget reallocation engine with projected conversion improvements.

## Notes
The app currently includes the initial shell and dummy data generation. Future iterations will refine the agent logic, add richer visuals, and improve the UI experience.
