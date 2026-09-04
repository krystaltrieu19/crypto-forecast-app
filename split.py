import pandas as pd

def train_test_split_ts(input_path="data/btc_usd_features.csv", train_frac=0.8):
    df = pd.read_csv(input_path, parse_dates=["date"])
    df = df.sort_values("date").reset_index(drop=True)

    split_idx = int(len(df) * train_frac)
    train = df.iloc[:split_idx].reset_index(drop=True)
    test = df.iloc[split_idx:].reset_index(drop=True)

    return train, test

if __name__ == "__main__":
    train, test = train_test_split_ts()

    train.to_csv("data/train.csv", index=False)
    test.to_csv("data/test.csv", index=False)

    print(f"Train: {len(train)} rows, {train['date'].min()} to {train['date'].max()}")
    print(f"Test:  {len(test)} rows, {test['date'].min()} to {test['date'].max()}")
