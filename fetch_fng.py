import requests
import pandas as pd

url = "https://api.alternative.me/fng/"
params = {"limit": 0, "format": "json"}
data = requests.get(url, params=params).json()["data"]

df = pd.DataFrame(data)
df["date"] = pd.to_datetime(df["timestamp"].astype(int), unit="s").dt.normalize()
df["fng_value"] = df["value"].astype(int)
df = df[["date", "fng_value"]].sort_values("date").reset_index(drop=True)

df.to_csv("data/fear_greed_daily.csv", index=False)
print(f"Saved {len(df)} rows, {df['date'].min()} to {df['date'].max()}")
print(df.tail())
