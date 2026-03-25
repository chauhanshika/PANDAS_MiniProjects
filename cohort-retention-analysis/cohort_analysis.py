import pandas as pd

# Load dataset
df = pd.read_csv("raw.csv")

# Convert timestamp
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

# Extract order month
df['order_month'] = df['order_purchase_timestamp'].dt.to_period('M')

# Assign cohort
df['cohort_month'] = df.groupby('customer_id')['order_month'].transform('min')

# Cohort index (months since first purchase)
df['cohort_index'] = (df['order_month'] - df['cohort_month']).apply(lambda x: x.n)

print(df[['customer_id', 'cohort_month', 'order_month', 'cohort_index']].head())
