import pandas as pd

# Load data
df = pd.read_csv("raw.csv")

# Convert to datetime
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

print("Data Loaded:", df.shape)
