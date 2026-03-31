import streamlit as st
import plotly.express as px
import pandas as pd

from src.metrics import load_data, get_funnel_metrics, get_segment_metrics, get_daily_revenue
from src.prompts import build_prompt
from src.ai_insights import generate_ai_insights

st.set_page_config(page_title="AI Product Analytics Copilot", layout="wide")

st.title("AI Product Analytics Copilot")
st.caption("Analyze funnel friction, payment conversion, and revenue trends from simulated product event data.")

@st.cache_data
def fetch_data():
    return load_data("data/transformed_events.csv")

df = fetch_data()

st.sidebar.header("Filters")

user_type_options = sorted(df["user_type"].dropna().unique().tolist())
payment_method_options = sorted(df["payment_method"].dropna().unique().tolist())
country_options = sorted(df["country"].dropna().unique().tolist())

selected_user_types = st.sidebar.multiselect("User Type", user_type_options, default=user_type_options)
selected_payment_methods = st.sidebar.multiselect("Payment Method", payment_method_options, default=payment_method_options)
selected_countries = st.sidebar.multiselect("Country", country_options, default=country_options[:10] if len(country_options) > 10 else country_options)

filtered_df = df[
    (df["user_type"].isin(selected_user_types)) &
    (df["payment_method"].isin(selected_payment_methods)) &
    (df["country"].isin(selected_countries))
]

summary = get_funnel_metrics(filtered_df)
user_metrics = get_segment_metrics(filtered_df, "user_type")
payment_metrics = get_segment_metrics(filtered_df, "payment_method")
country_metrics = get_segment_metrics(filtered_df, "country")
revenue_df = get_daily_revenue(filtered_df)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Visits", f"{summary['visits']:,}")
c2.metric("Checkouts", f"{summary['checkouts']:,}")
c3.metric("Payments", f"{summary['payments']:,}")
c4.metric("Revenue", f"£{summary['revenue']:,.2f}")

c5, c6, c7 = st.columns(3)
c5.metric("Visit → Checkout", f"{summary['visit_to_checkout']:.1%}")
c6.metric("Checkout → Payment", f"{summary['checkout_to_payment']:.1%}")
c7.metric("Overall Conversion", f"{summary['overall_conversion']:.1%}")

st.subheader("Funnel Stages")
funnel_df = pd.DataFrame({
    "stage": ["visit", "checkout", "payment", "payment_failed"],
    "count": [
        summary["visits"],
        summary["checkouts"],
        summary["payments"],
        summary["failures"]
    ]
})
st.bar_chart(funnel_df, x="stage", y="count")

st.subheader("Revenue Trend")
fig = px.line(revenue_df, x="date", y="revenue")
st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)

with left:
    st.subheader("User Type Metrics")
    st.dataframe(user_metrics, use_container_width=True)

with right:
    st.subheader("Payment Method Metrics")
    st.dataframe(payment_metrics, use_container_width=True)

st.subheader("Biggest Friction Points")
if not user_metrics.empty:
    worst_user = user_metrics.sort_values("conversion").iloc[0]
    st.write(
        f"Lowest-converting user segment: **{worst_user['user_type']}** "
        f"({worst_user['conversion']:.1%} conversion)"
    )

if not payment_metrics.empty:
    worst_payment = payment_metrics.sort_values("conversion").iloc[0]
    st.write(
        f"Lowest-converting payment method: **{worst_payment['payment_method']}** "
        f"({worst_payment['conversion']:.1%} conversion)"
    )

st.subheader("Suggested Experiments")
st.markdown("""
**1. Simplify checkout for new users**  
Target checkout-to-payment conversion for users with lower familiarity.

**2. Improve PayPal payment reliability or messaging**  
Investigate whether lower conversion is caused by payment friction or abandonment.

**3. Test segment-specific payment defaults**  
Prioritize the most successful payment method for lower-converting user segments.
""")

st.subheader("AI Product Insights")
if st.button("Generate Insights"):
    prompt = build_prompt(
        summary=summary,
        user_metrics=user_metrics.to_string(index=False),
        payment_metrics=payment_metrics.to_string(index=False),
        country_metrics=country_metrics.head(10).to_string(index=False),
    )
    with st.spinner("Generating PM-style insights..."):
        insights = generate_ai_insights(prompt)
    st.markdown(insights)

st.subheader("Ask a Product Question")
user_question = st.text_input("Example: Why is PayPal underperforming?")

if st.button("Answer Question") and user_question:
    custom_prompt = f"""
You are a product manager answering a question about funnel and payment performance.

Question:
{user_question}

Overall metrics:
{summary}

User type metrics:
{user_metrics.to_string(index=False)}

Payment method metrics:
{payment_metrics.to_string(index=False)}

Country metrics:
{country_metrics.head(10).to_string(index=False)}

Answer clearly and specifically.
"""
    with st.spinner("Thinking..."):
        answer = generate_ai_insights(custom_prompt)
    st.markdown(answer)