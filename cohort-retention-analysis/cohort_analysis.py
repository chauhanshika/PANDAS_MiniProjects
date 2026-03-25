import pandas as pd

# Load dataset
df = pd.read_csv("raw.csv")

# Convert timestamp
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

# Extract order month
df['order_month'] = df['order_purchase_timestamp'].dt.to_period('M')

# Assign cohort
df['cohort_month'] = df.groupby('customer_id')['order_month'].transform('min')

# Cohort index
df['cohort_index'] = (df['order_month'] - df['cohort_month']).apply(lambda x: x.n)

# Group users
cohort_data = df.groupby(['cohort_month', 'cohort_index'])['customer_id'].nunique().reset_index()

# Pivot
retention_matrix = cohort_data.pivot(index='cohort_month',
                                     columns='cohort_index',
                                     values='customer_id')

# Convert to percentage
retention_matrix = retention_matrix.divide(retention_matrix[0], axis=0)

print("\nRetention Percentage:")
print(retention_matrix.head())

# Save output
retention_matrix.to_csv("retention_matrix.csv")

print("\nRetention matrix saved as retention_matrix.csv")
