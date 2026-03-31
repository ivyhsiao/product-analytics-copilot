# AI Product Analytics Copilot

An AI-powered analytics tool that surfaces funnel drop-offs, revenue drivers, and user behavior patterns from simulated product and payment event data.

## Overview
This project uses the UCI Online Retail dataset as a real-world transaction base and transforms it into simulated product funnel events such as visits, checkouts, payments, and failed payments. It then applies funnel analysis, segment analysis, and LLM-generated product insights to help identify conversion friction and recommend experiments.

## Features
- Funnel performance tracking
- Revenue trend visualization
- Segment-level conversion analysis
- Friction point identification
- AI-generated root-cause insights
- A/B test recommendations
- Interactive filtering by user type, payment method, and country

## Dataset
The project is based on the UCI Online Retail dataset and transforms transaction-level ecommerce data into simulated product and payment event flows.

## Tech Stack
- Python
- Pandas
- Streamlit
- Plotly
- OpenAI API

## How to Run
1. Clone the repo
2. Install dependencies with `pip install -r requirements.txt`
3. Add your OpenAI API key to `.env`
4. Place `Online Retail.xlsx` inside the `data/` folder
5. Run `python src/data_prep.py`
6. Run `streamlit run app.py`

## Example Questions
- Which user segment has the highest funnel friction?
- Which payment method underperforms?
- What experiments could improve conversion?

## Future Improvements
- Cohort retention analysis
- More realistic funnel simulation logic
- Experiment prioritization framework
- Deployment to Streamlit Cloud or Render