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

# ---- LAST ACTIVITY ----
last_activity = df.groupby('customer_id')['order_purchase_timestamp'].max().reset_index()
last_activity.columns = ['customer_id', 'last_activity_date']

# ---- CURRENT DATE ----
current_date = df['order_purchase_timestamp'].max()

# ---- DAYS INACTIVE ----
last_activity['days_inactive'] = (
    current_date - last_activity['last_activity_date']
).dt.days

# ---- CHURN CLASSIFICATION ----
def classify_churn(days):
    if days <= 30:
        return "Active"
    elif days <= 90:
        return "At Risk"
    else:
        return "Churned"

last_activity['churn_status'] = last_activity['days_inactive'].apply(classify_churn)

# ---- BUSINESS INSIGHTS ----
total_users = len(last_activity)

churned_users = len(last_activity[last_activity['churn_status'] == "Churned"])
at_risk_users = len(last_activity[last_activity['churn_status'] == "At Risk"])
active_users = len(last_activity[last_activity['churn_status'] == "Active"])

print("\n---- BUSINESS INSIGHTS ----")
print(f"Total Users: {total_users}")
print(f"Active Users: {active_users}")
print(f"At Risk Users: {at_risk_users}")
print(f"Churned Users: {churned_users}")

print("\n---- PERCENTAGE DISTRIBUTION ----")
print(f"Active: {round((active_users/total_users)*100, 2)}%")
print(f"At Risk: {round((at_risk_users/total_users)*100, 2)}%")
print(f"Churned: {round((churned_users/total_users)*100, 2)}%")

# ---- SAVE OUTPUT ----
last_activity.to_csv("output.csv", index=False)
