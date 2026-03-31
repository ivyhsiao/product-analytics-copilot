import pandas as pd
import random

print("Script started")

df = pd.read_excel("data/Online Retail.xlsx")
print("Original rows:", len(df))
print("Columns:", list(df.columns))

df = df.dropna(subset=["CustomerID", "InvoiceDate", "Quantity", "UnitPrice"])
df = df[df["Quantity"] > 0]
df = df[df["UnitPrice"] > 0]

print("Rows after cleaning:", len(df))

events = []

for _, row in df.iterrows():
    user_id = int(row["CustomerID"])
    timestamp = row["InvoiceDate"]
    amount = float(row["Quantity"]) * float(row["UnitPrice"])
    country = row["Country"]

    user_type = "returning" if random.random() > 0.5 else "new"
    payment_method = random.choice(["card", "paypal", "apple_pay"])

    events.append({
        "user_id": user_id,
        "event": "visit",
        "timestamp": timestamp,
        "amount": 0,
        "user_type": user_type,
        "payment_method": payment_method,
        "country": country
    })

    if random.random() < 0.8:
        events.append({
            "user_id": user_id,
            "event": "checkout",
            "timestamp": timestamp,
            "amount": 0,
            "user_type": user_type,
            "payment_method": payment_method,
            "country": country
        })

        success_prob = 0.75
        if user_type == "new":
            success_prob -= 0.10
        if payment_method == "paypal":
            success_prob -= 0.10

        if random.random() < success_prob:
            events.append({
                "user_id": user_id,
                "event": "payment",
                "timestamp": timestamp,
                "amount": round(amount, 2),
                "user_type": user_type,
                "payment_method": payment_method,
                "country": country
            })
        else:
            events.append({
                "user_id": user_id,
                "event": "payment_failed",
                "timestamp": timestamp,
                "amount": 0,
                "user_type": user_type,
                "payment_method": payment_method,
                "country": country
            })

event_df = pd.DataFrame(events)
event_df.to_csv("data/transformed_events.csv", index=False)

print("Done! Rows created:", len(event_df))
print(event_df.head())