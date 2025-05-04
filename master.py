import pandas as pd

# Download and read CSV directly into a DataFrame
url = "https://images.dhan.co/api-data/api-scrip-master.csv"
df = pd.read_csv(url)

# Optionally save it locally
df.to_csv("api-scrip-master.csv", index=False)

print("✅ File downloaded and saved as 'api-scrip-master.csv'")
