import warnings
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error
from statsmodels.tsa.statespace.sarimax import SARIMAX

warnings.filterwarnings("ignore")

df = pd.read_csv("data/btc_usd_features_fng.csv", parse_dates=["date"])
df = df.sort_values("date").reset_index(drop=True)
df["fng_lag1"] = df["fng_value"].shift(1)
df = df.dropna(subset=["fng_lag1"]).reset_index(drop=True)

lag_features = ["lag_1", "lag_2", "lag_3", "vol_7"]
n_folds = 6
fold_size = 30
start = len(df) - n_folds * fold_size

def score(y_true, y_pred):
    # reset_index avoids pandas refusing to compare two Series that
    # happen to carry different row labels, even when they line up
    y_true = pd.Series(y_true).reset_index(drop=True)
    y_pred = pd.Series(y_pred).reset_index(drop=True)
    mae = mean_absolute_error(y_true, y_pred)
    dir_acc = (y_true.apply(lambda x: x > 0) == y_pred.apply(lambda x: x > 0)).mean()
    return mae, dir_acc

results = {"naive": [], "mean": [], "linear_reg": [], "arima": [], "arimax_fng": []}

for i in range(n_folds):
    train_end = start + i * fold_size
    test_end = min(train_end + fold_size, len(df))
    train, test = df.iloc[:train_end], df.iloc[train_end:test_end]
    if len(test) == 0:
        continue
    y_test = test["target"]

    results["naive"].append(score(y_test, test["return_1d"]))
    results["mean"].append(score(y_test, pd.Series(train["target"].mean(), index=y_test.index)))

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(train[lag_features])
    X_test_s = scaler.transform(test[lag_features])
    lin = LinearRegression().fit(X_train_s, train["target"])
    results["linear_reg"].append(score(y_test, lin.predict(X_test_s)))

    arima_preds, arimax_preds, actuals = [], [], []
    for day in range(train_end, test_end):
        hist_endog = df["return_1d"].iloc[:day + 1]

        fit_a = SARIMAX(hist_endog, order=(3, 0, 0)).fit(disp=False)
        arima_preds.append(fit_a.forecast(steps=1).iloc[0])

        hist_exog = df[["fng_lag1"]].iloc[:day + 1]
        future_exog = pd.DataFrame({"fng_lag1": [df["fng_value"].iloc[day]]})
        fit_x = SARIMAX(hist_endog, exog=hist_exog, order=(3, 0, 0)).fit(disp=False)
        arimax_preds.append(fit_x.forecast(steps=1, exog=future_exog).iloc[0])

        actuals.append(df["target"].iloc[day])

    results["arima"].append(score(actuals, arima_preds))
    results["arimax_fng"].append(score(actuals, arimax_preds))

print(f"{'Method':20s} {'avg MAE':>10s} {'avg Dir.Acc':>12s}")
for name, scores in results.items():
    maes, dir_accs = zip(*scores)
    print(f"{name:20s} {np.mean(maes):10.5f} {np.mean(dir_accs):11.1%}")
