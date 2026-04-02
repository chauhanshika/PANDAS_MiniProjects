import pandas as pd

# Load dataset
df = pd.read_csv("raw.csv")

# Convert timestamp
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

print("Data Loaded:", df.shape)
