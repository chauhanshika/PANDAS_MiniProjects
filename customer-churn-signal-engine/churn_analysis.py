import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv("raw.csv")

# Convert timestamp
df['order_purchase_timestamp'] = pd.to_datetime(
    df['order_purchase_timestamp'], errors='coerce'
)

# Sort data
df = df.sort_values(by=['customer_id', 'order_purchase_timestamp'])

# --LAST ACTIVITY PER USER --
last_activity = df.groupby('customer_id')['order_purchase_timestamp'].max().reset_index()
last_activity.columns = ['customer_id', 'last_activity_date']

# ---- CURRENT DATE (REFERENCE) ----
current_date = df['order_purchase_timestamp'].max()

# --- DAYS SINCE LAST ACTIVITY ---
last_activity['days_inactive'] = (
    current_date - last_activity['last_activity_date']
).dt.days

print("\n---- LAST ACTIVITY ----")
print(last_activity.head())

# ---- BASIC STATS ----
print("\n---- INACTIVITY STATS ----")
print(last_activity['days_inactive'].describe())

# Save output
last_activity.to_csv("output.csv", index=False)
