# AI Product Analytics Copilot

An AI-powered tool that helps product and operations teams identify where users drop off, why revenue underperforms, and what experiments to run next without needing a data analyst.

## Overview
This project uses the UCI Online Retail dataset as a real-world transaction base and transforms it into simulated product funnel events such as visits, checkouts, payments, and failed payments. It then applies funnel analysis, segment analysis, and LLM-generated product insights to help identify conversion friction and recommend experiments.

## The Problem
Product and ops teams often sit on top of rich transaction data but lack the bandwidth or technical resources to consistently surface actionable insights. Dashboards show what happened, but recommendations for next step usually require more manual work.

## What I Built
An end-to-end analytics tool that takes raw transaction data, simulates product funnel events (visits, checkouts, payments, failures), and surfaces conversion friction and revenue drivers through an interactive dashboard powered by LLM-generated root-cause analysis and A/B test recommendations.
Instead of a static report, users can ask natural language questions and receive AI-generated hypotheses and experiment suggestions grounded in the actual data.

## AI Tools Used
- OpenAI API (GPT-4): generates root-cause insights and experiment recommendations from funnel metrics
- Prompt engineering: structured prompts guide the model to reason about segment-level drop-offs and prioritize actionable next steps

## Key Features
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
