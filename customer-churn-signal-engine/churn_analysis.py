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

last_activity = df.groupby('customer_id')['order_purchase_timestamp'].max().reset_index()
last_activity.columns = ['customer_id', 'last_activity_date']

# ---- ORDER COUNT (FREQUENCY) ----
order_count = df.groupby('customer_id').size().reset_index(name='total_orders')

# ---- MERGE FEATURES ----
user_df = pd.merge(last_activity, order_count, on='customer_id')

# ---- CURRENT DATE ----
current_date = df['order_purchase_timestamp'].max()

# ---- DAYS INACTIVE ----
user_df['days_inactive'] = (
    current_date - user_df['last_activity_date']
).dt.days

# ---- CHURN CLASSIFICATION ----
def classify_churn(row):
    if row['days_inactive'] <= 30:
        return "Active"
    elif row['days_inactive'] <= 90:
        return "At Risk"
    else:
        return "Churned"

user_df['churn_status'] = user_df.apply(classify_churn, axis=1)

# ---- INSIGHTS ----
print("\n---- SUMMARY ----")
print(user_df['churn_status'].value_counts())

print("\n---- AVG ORDERS BY SEGMENT ----")
print(user_df.groupby('churn_status')['total_orders'].mean())

# ---- SAVE OUTPUT ----
user_df.to_csv("output.csv", index=False)
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

last_activity = df.groupby('customer_id')['order_purchase_timestamp'].max().reset_index()
last_activity.columns = ['customer_id', 'last_activity_date']

# ---- ORDER COUNT (FREQUENCY) ----
order_count = df.groupby('customer_id').size().reset_index(name='total_orders')

# ---- MERGE FEATURES ----
user_df = pd.merge(last_activity, order_count, on='customer_id')

# ---- CURRENT DATE ----
current_date = df['order_purchase_timestamp'].max()

# ---- DAYS INACTIVE ----
user_df['days_inactive'] = (
    current_date - user_df['last_activity_date']
).dt.days

# ---- CHURN CLASSIFICATION ----
def classify_churn(row):
    if row['days_inactive'] <= 30:
        return "Active"
    elif row['days_inactive'] <= 90:
        return "At Risk"
    else:
        return "Churned"

user_df['churn_status'] = user_df.apply(classify_churn, axis=1)

# ---- INSIGHTS ----
print("\n---- SUMMARY ----")
print(user_df['churn_status'].value_counts())

print("\n---- AVG ORDERS BY SEGMENT ----")
print(user_df.groupby('churn_status')['total_orders'].mean())
# ---- CREATE SUMMARY ----
summary = user_df['churn_status'].value_counts().reset_index()
summary.columns = ['churn_status', 'user_count']

summary['percentage'] = (summary['user_count'] / len(user_df)) * 100

# ---- SAVE OUTPUT ----
user_df.to_csv("output.csv", index=False)
summary.to_csv("summary.csv", index=False)
