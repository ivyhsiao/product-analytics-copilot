def build_prompt(summary: dict, user_metrics: str, payment_metrics: str, country_metrics: str) -> str:
    return f"""
You are a product manager analyzing funnel and payment performance.

Based on the metrics below, respond in exactly these sections:

## Key Insights
Give 3 concrete insights based on the data.

## Likely Root Causes
Explain why these patterns may be happening.

## Recommended Experiments
Suggest 3 specific A/B tests or product changes.

Rules:
- Be specific
- Reference user segments or payment methods when relevant
- Focus on conversion, friction, and revenue
- Avoid generic advice
- Write like a PM preparing recommendations for a product team

Overall metrics:
{summary}

User type metrics:
{user_metrics}

Payment method metrics:
{payment_metrics}

Country metrics:
{country_metrics}
"""