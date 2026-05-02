# Feature Engineering Documentation

## Overview

This document describes the feature engineering pipeline implemented in `src/feature_engineering/feature_engineering.py`. The pipeline reads `sensex_data/sensex.csv`, applies a set of transformations and engineered features, drops selected raw columns, removes rows with missing values, and saves the processed dataset to `sensex_data/new_sensex.csv`.

## Input setup

The function expects the input dataset to contain the following columns:

- `Datetime`
- `Open`
- `High`
- `Low`
- `Close`
- `Volume`

`Datetime` is converted to pandas datetime and set as the index so that rolling calculations and lag features are aligned correctly across time.

## Features created (implemented)

### 1. Log-transformed features

- `Close_log = log(Close)`
- `Open_log = log(Open)`
- `Low_log = log(Low)`
- `High_log = log(High)`
- `Volume_log = log1p(Volume)`

Log transforms reduce skewness and stabilize variance; `log1p` is used for volume to handle zeros safely.

### 2. Moving averages

- `MA_10` — 10-period simple moving average of `Close_log`
- `MA_50` — 50-period simple moving average of `Close_log`
- `ma_cross = MA_10 - MA_50`

These capture short- and long-term trend structure and the difference between them.

### 3. Exponential moving averages

- `EMA_10` — 10-period EMA of `Close_log`
- `EMA_50` — 50-period EMA of `Close_log`

EMAs weight recent observations more heavily than simple moving averages.

### 4. Log return

- `Log_Return = Close_log.diff()`

This is the period-to-period log return and is a stationary representation of price movement.

### 5. Volatility

- `Volatility_10` — rolling std of `Log_Return` over 10 periods
- `Volatility_50` — rolling std of `Log_Return` over 50 periods

Note: a 20-period volatility (`Volatility_20`) and a volatility ratio were present previously but are currently not enabled in the implementation.

### 6. Lagged returns

- `lag_2 = Log_Return.shift(2)`
- `lag_3 = Log_Return.shift(3)`

The code currently uses `lag_2` and `lag_3`; `lag_1` is commented out in the implementation.

### 7. Momentum

- `momentum = Log_Return.rolling(5).sum()`

This summarizes recent 5-period return behavior.

### 8. RSI

Relative Strength Index computed with a 14-period rolling window and normalized to approximately `[-1, 1]` using the transformation implemented in the code.

### 9. Bollinger Bands

Bollinger Bands are computed using a 20-period moving average and 2 standard deviations:

- `BB_Upper` — Upper band = MA(20) + (2 × std)
- `BB_Lower` — Lower band = MA(20) - (2 × std)
- `BB_Width` — Band width normalized by price: (Upper - Lower) / MA
- `BB_Position` — Relative position of close within bands: (Close - Lower) / (Upper - Lower)

These features capture volatility and overbought/oversold conditions.

### 10. MACD

Moving Average Convergence Divergence uses three exponential moving averages:

- `MACD` — Fast EMA (12) minus Slow EMA (26)
- `MACD_Signal` — 9-period EMA of MACD line
- `MACD_Histogram` — Difference between MACD and Signal

These capture momentum and trend changes.

### 11. Target and binary label

- `Expected_Pct = Log_Return.shift(-1)` is computed as the next-period log return (forward-shifted). In the current pipeline `Expected_Pct` is created but then dropped before saving the final CSV.
- `Up_Down` — a binary label added by the code: 1 when `((High - Close) / High) > 0.01`, else 0.

## Features intentionally not active in code

The following features are present in the original design or commented examples but are currently disabled (commented out) in `feature_engineering.py`:

- `Volatility_20` (20-period volatility)
- `vol_ratio` (Volatility_10 / Volatility_50)
- `lag_1`
- `return_5` (5-period mean return)
- `range_ratio` and `close_position` (intraday range-position features)
- `volume_change` and `volume_ma_ratio` (volume-based features)
- `lag_target_1` (lagged target)

These can be re-enabled easily by uncommenting the corresponding lines in `src/feature_engineering/feature_engineering.py`.

## Dropped columns

Before saving the processed dataset the pipeline drops the following raw, non-stationary columns:

- `Open`
- `High`
- `Low`
- `Close`
- `Volume`
- `Expected_Pct` (computed but removed from final output)

## Cleaning step

After feature creation the function calls `df.dropna()` to remove rows affected by rolling-window warm-up periods, differences, and shifts.

## Output

The final processed dataset (with engineered features listed above, excluding the dropped columns) is saved to `sensex_data/new_sensex.csv`.

## Notes

- The code currently returns a cleaned DataFrame of active features; review `src/feature_engineering/feature_engineering.py` to re-enable any commented features or adjust target creation.
- If you want the forward-looking `Expected_Pct` included in the output, the dropping of that column should be removed from the save step in the script.
