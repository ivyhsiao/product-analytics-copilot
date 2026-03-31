import pandas as pd

def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

def get_funnel_metrics(df: pd.DataFrame) -> dict:
    visits = (df["event"] == "visit").sum()
    checkouts = (df["event"] == "checkout").sum()
    payments = (df["event"] == "payment").sum()
    failures = (df["event"] == "payment_failed").sum()
    revenue = df.loc[df["event"] == "payment", "amount"].sum()

    return {
        "visits": int(visits),
        "checkouts": int(checkouts),
        "payments": int(payments),
        "failures": int(failures),
        "visit_to_checkout": checkouts / visits if visits else 0,
        "checkout_to_payment": payments / checkouts if checkouts else 0,
        "overall_conversion": payments / visits if visits else 0,
        "revenue": round(float(revenue), 2),
    }

def get_segment_metrics(df: pd.DataFrame, col: str) -> pd.DataFrame:
    rows = []
    for value, group in df.groupby(col):
        visits = (group["event"] == "visit").sum()
        checkouts = (group["event"] == "checkout").sum()
        payments = (group["event"] == "payment").sum()
        failures = (group["event"] == "payment_failed").sum()
        revenue = group.loc[group["event"] == "payment", "amount"].sum()

        rows.append({
            col: value,
            "visits": visits,
            "checkouts": checkouts,
            "payments": payments,
            "failures": failures,
            "conversion": payments / visits if visits else 0,
            "checkout_to_payment": payments / checkouts if checkouts else 0,
            "revenue": round(float(revenue), 2),
        })

    return pd.DataFrame(rows).sort_values("conversion")

def get_daily_revenue(df: pd.DataFrame) -> pd.DataFrame:
    paid = df[df["event"] == "payment"].copy()
    paid["date"] = paid["timestamp"].dt.date
    return paid.groupby("date", as_index=False)["amount"].sum().rename(columns={"amount": "revenue"})