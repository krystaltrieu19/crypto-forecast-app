
## Model Exploration & Results

### Data

Daily BTC/USD closing prices from CoinGecko's free API (about a year of history), plus the daily Crypto Fear & Greed Index from alternative.me's free API. From the price history, I built a few features for each day: the return over the last 1, 2, and 3 days, and how volatile (choppy) the last 7 days had been.

### Methodology

Every model here is tested using walk-forward validation: 6 rolling 30-day windows, where each one trains on everything up to that point and tests on the following month, then moves forward and repeats.

I went with this after an early version of the project gave a misleading result. Under an 80/20 train/test split, linear regression appeared to outperform a naive baseline. This showed that a single split can give a misleading picture of a model's true performance, depending on which period of time happens to fall into the test set. Averaging across several windows gives a much more honest answer.

Two numbers are reported for each model, based on predicting tomorrow's return:

- **MAE (Mean Absolute Error)**: the average size of the prediction error. Lower is better.
- **Directional Accuracy**: the percentage of days the model correctly predicted the direction of movement (up or down). 50% is the accuracy expected from random guessing.

### Models tested

| Model | Description |
|---|---|
| Naive | Predicts that tomorrow's return will equal today's return |
| Mean baseline | Predicts that tomorrow's return will equal the average return observed during training |
| Linear regression | Predicts using recent lagged returns and recent volatility as inputs |
| Random Forest | Tested using a single train/test split only. Results suggested overfitting, so this model was not carried forward into the final walk-forward comparison. It is reported here for transparency. |
| ARIMA(3,0,0) | A classical time-series model that predicts future returns based on the statistical pattern of past returns |
| ARIMAX(3,0,0) + Fear & Greed | The same ARIMA model, with the previous day's Fear & Greed Index added as an additional input |

### Results (averaged across the 6 test windows)

| Method | Avg MAE | Avg Directional Acc |
|---|---|---|
| Naive | 0.02018 | 50.6% |
| Mean baseline | 0.01506 | 48.3% |
| Linear regression | 0.01534 | 46.7% |
| ARIMA(3,0,0) | 0.01510 | 43.3% |
| ARIMAX(3,0,0) + Fear & Greed | 0.01527 | 45.6% |

### Conclusion

None of the models tested including those using engineered features, classical time-series methods, and external sentiment data, consistently outperformed a simple average-based baseline in predicting next-day Bitcoin returns. The mean baseline achieved the lowest average error, while the naive baseline achieved the highest directional accuracy, only slightly above what random guessing would produce.

Adding the Fear & Greed Index did not meaningfully improve results. This is likely because a large portion of the index is derived from price-based measures, such as volatility, which the other models could already access in a different form.

This outcome is treated as a central finding of the project, not a shortcoming. It reflects the well-documented difficulty of forecasting short-term cryptocurrency price movements, and it shaped the design of the accompanying application, which presents forecasts transparently alongside their baseline comparisons rather than overstating their reliability.
