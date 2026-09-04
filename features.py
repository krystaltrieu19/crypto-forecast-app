import pandas as pd

def build_features(input_path="data/btc_usd_daily_raw.csv"):
    df = pd.read_csv(input_path, parse_dates=["date"])
    df = df.sort_values("date").reset_index(drop=True)

    # Daily return: % change from the previous day
    df["return_1d"] = df["close"].pct_change()

    # Lagged returns: yesterday's and the day before's return used as inputs
    df["lag_1"] = df["return_1d"].shift(1)
    df["lag_2"] = df["return_1d"].shift(2)
    df["lag_3"] = df["return_1d"].shift(3)

    # Rolling volatility: how turbulent the last 7 days have been
    df["vol_7"] = df["return_1d"].rolling(7).std()

    # Target: tomorrow's return - what our model will predict.
    df["target"] = df["return_1d"].shift(-1)

    df = df.dropna().reset_index(drop=True)
    return df

if __name__ == "__main__":
    df = build_features()
    df.to_csv("data/btc_usd_features.csv", index=False)
    print(f"Built feature table: {len(df)} rows, {len(df.columns)} columns")
    print(df.columns.tolist())
