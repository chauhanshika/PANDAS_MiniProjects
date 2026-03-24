import pandas as pd

# Load data
df = pd.read_csv("raw.csv")

# Convert datetime
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

# Extract month
df['order_month'] = df['order_purchase_timestamp'].dt.to_period('M')

# Get cohort (first purchase month)
df['cohort_month'] = df.groupby('customer_id')['order_month'].transform('min')

print(df[['customer_id', 'order_month', 'cohort_month']].head())
