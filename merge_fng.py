import pandas as pd

features = pd.read_csv("data/btc_usd_features.csv", parse_dates=["date"])
fng = pd.read_csv("data/fear_greed_daily.csv", parse_dates=["date"])

merged = features.merge(fng, on="date", how="inner")
print(f"Features: {len(features)} rows | Fear&Greed: {len(fng)} rows | Merged: {len(merged)} rows")
print(f"Merged date range: {merged['date'].min()} to {merged['date'].max()}")

merged.to_csv("data/btc_usd_features_fng.csv", index=False)
