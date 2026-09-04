
import pandas as pd

import matplotlib.pyplot as plt

df = pd.read_csv("data/btc_usd_daily_raw.csv", parse_dates=["date"])

df = df.sort_values("date").reset_index(drop=True)

# --- Sanity checks 

print("Rows:", len(df))

print("Date range:", df["date"].min(), "to", df["date"].max())

print("Missing values:\n", df.isnull().sum())

print("Duplicate dates:", df["date"].duplicated().sum())

full_range = pd.date_range(df["date"].min(), df["date"].max(), freq="D")

missing_days = full_range.difference(df["date"])

print("Missing calendar days:", len(missing_days))

# --- Returns and rolling volatility 

df["return_1d"] = df["close"].pct_change()

df["vol_7d"] = df["return_1d"].rolling(7).std()

# --- Plot 1: raw price 

plt.figure(figsize=(10, 4))

plt.plot(df["date"], df["close"])

plt.title("BTC/USD Closing Price")

plt.xlabel("Date")

plt.ylabel("Price (USD)")

plt.tight_layout()

plt.savefig("plots/01_price.png")

plt.close()

# --- Plot 2: daily returns 

plt.figure(figsize=(10, 4))

plt.plot(df["date"], df["return_1d"])

plt.title("BTC/USD Daily Returns")

plt.xlabel("Date")

plt.ylabel("Daily Return")

plt.tight_layout()

plt.savefig("plots/02_returns.png")

plt.close()

# --- Plot 3: rolling volatility 

plt.figure(figsize=(10, 4))

plt.plot(df["date"], df["vol_7d"])

plt.title("BTC/USD 7-Day Rolling Volatility")

plt.xlabel("Date")

plt.ylabel("Rolling Std Dev of Returns")

plt.tight_layout()

plt.savefig("plots/03_volatility.png")

plt.close()

print("\nSaved plots to plots/01_price.png, plots/02_returns.png, plots/03_volatility.png")

