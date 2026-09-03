import requests
import pandas as pd

def fetch_btc_daily(days=365):
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {"vs_currency": "usd", "days": days, "interval": "daily"}
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    prices = data["prices"]  # list of [timestamp_ms, price]
    df = pd.DataFrame(prices, columns=["timestamp", "close"])
    df["date"] = pd.to_datetime(df["timestamp"], unit="ms")
    df = df[["date", "close"]]
    return df

if __name__ == "__main__":
    df = fetch_btc_daily(days=365)
    df.to_csv("data/btc_usd_daily_raw.csv", index=False)
    print(f"Saved {len(df)} rows to data/btc_usd_daily_raw.csv")
    print(df.head())
    print(df.tail())
