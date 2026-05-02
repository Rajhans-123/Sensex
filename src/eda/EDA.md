**Exploratory Data Analysis (EDA) — Summary**

- **Purpose:** Describe the dataset, highlight distributional properties, detect outliers, and show relationships between price fields (`open`, `high`, `low`, `close`).
- **Data source:** Aggregated price data for the SENSEX timeframe(s) processed in this project.

**What’s included**

- The `eda_plots` folder contains visualizations used during EDA. Each image filename indicates the plotted field(s) and plot type. Key plot types:
  - **hist**: distribution histogram
  - **kde**: kernel density estimate of distribution
  - **box**: boxplot showing spread and outliers
  - **bar**: aggregated bar summaries
  - **pairplot**: pairwise relationships between columns
  - **open_low_high**, **close_open_low_high**: combined time-series overlays (moving averages noted in filenames)

**Files (in eda_plots)**

- close_bar.png — bar summary for `close`
- close_box.png — boxplot for `close`
- close_high_pairplot.png — pairwise comparisons focused on `close` and `high`
- close_hist.png — histogram for `close`
- close_kde.png — KDE for `close`
- close_low_pairplot.png — pairwise comparisons focused on `close` and `low`
- close_open_low_high.png — combined plot of `close`, `open`, `low`, `high`
- close_open_low_high_ma10.png — combined plot with 10-period moving average
- close_open_low_high_ma50.png — combined plot with 50-period moving average
- close_open_pairplot.png — pairwise comparisons of `close` and `open`
- high_bar.png — bar summary for `high`
- high_box.png — boxplot for `high`
- high_hist.png — histogram for `high`
- high_kde.png — KDE for `high`
- low_bar.png — bar summary for `low`
- low_box.png — boxplot for `low`
- low_high_pairplot.png — pairwise comparisons of `low` and `high`
- low_hist.png — histogram for `low`
- low_kde.png — KDE for `low`
- open_bar.png — bar summary for `open`
- open_box.png — boxplot for `open`
- open_high_pairplot.png — pairwise comparisons of `open` and `high`
- open_hist.png — histogram for `open`
- open_kde.png — KDE for `open`
- open_low_pairplot.png — pairwise comparisons of `open` and `low`

## Figures

Below are the EDA figures

1. ![Figure 1 — close_hist.png](../../eda_plots/close_hist.png)
   *Figure 1 — Histogram of `close` prices.*
2. ![Figure 2 — close_kde.png](../../eda_plots/close_kde.png)
   *Figure 2 — KDE of `close` prices.*
3. ![Figure 3 — close_box.png](../../eda_plots/close_box.png)
   *Figure 3 — Boxplot for `close` showing spread and outliers.*
4. ![Figure 4 — close_bar.png](../../eda_plots/close_bar.png)
   *Figure 4 — Binned/aggregated summary for `close`.*
5. ![Figure 5 — close_open_pairplot.png](../../eda_plots/close_open_pairplot.png)
   *Figure 5 — Pairwise plot: `close` vs `open`.*
6. ![Figure 6 — close_high_pairplot.png](../../eda_plots/close_high_pairplot.png)
   *Figure 6 — Pairwise plot: `close` vs `high`.*
7. ![Figure 7 — close_low_pairplot.png](../../eda_plots/close_low_pairplot.png)
   *Figure 7 — Pairwise plot: `close` vs `low`.*
8. ![Figure 8 — close_open_low_high.png](../../eda_plots/close_open_low_high.png)
   *Figure 8 — Overlay of `close`, `open`, `low`, `high`.*
9. ![Figure 9 — close_open_low_high_ma10.png](../../eda_plots/close_open_low_high_ma10.png)
   *Figure 9 — Same overlay with 10-period moving average.*
10. ![Figure 10 — close_open_low_high_ma50.png](../../eda_plots/close_open_low_high_ma50.png)
  *Figure 10 — Same overlay with 50-period moving average.*
11. ![Figure 11 — open_hist.png](../../eda_plots/open_hist.png)
  *Figure 11 — Histogram of `open` prices.*
12. ![Figure 12 — open_kde.png](../../eda_plots/open_kde.png)
  *Figure 12 — KDE of `open` prices.*
13. ![Figure 13 — open_box.png](../../eda_plots/open_box.png)
  *Figure 13 — Boxplot for `open`.*
14. ![Figure 14 — open_bar.png](../../eda_plots/open_bar.png)
  *Figure 14 — Binned/aggregated summary for `open`.*
15. ![Figure 15 — open_high_pairplot.png](../../eda_plots/open_high_pairplot.png)
  *Figure 15 — Pairwise plot: `open` vs `high`.*
16. ![Figure 16 — open_low_pairplot.png](../../eda_plots/open_low_pairplot.png)
  *Figure 16 — Pairwise plot: `open` vs `low`.*
17. ![Figure 17 — high_hist.png](../../eda_plots/high_hist.png)
  *Figure 17 — Histogram of `high` prices.*
18. ![Figure 18 — high_kde.png](../../eda_plots/high_kde.png)
  *Figure 18 — KDE of `high` prices.*
19. ![Figure 19 — high_box.png](../../eda_plots/high_box.png)
  *Figure 19 — Boxplot for `high`.*
20. ![Figure 20 — high_bar.png](../../eda_plots/high_bar.png)
  *Figure 20 — Binned/aggregated summary for `high`.*
21. ![Figure 21 — low_hist.png](../../eda_plots/low_hist.png)
  *Figure 21 — Histogram of `low` prices.*
22. ![Figure 22 — low_kde.png](../../eda_plots/low_kde.png)
  *Figure 22 — KDE of `low` prices.*
23. ![Figure 23 — low_box.png](../../eda_plots/low_box.png)
  *Figure 23 — Boxplot for `low`.*
24. ![Figure 24 — low_bar.png](../../eda_plots/low_bar.png)
  *Figure 24 — Binned/aggregated summary for `low`.*
25. ![Figure 25 — low_high_pairplot.png](../../eda_plots/low_high_pairplot.png)
  *Figure 25 — Pairwise plot: `low` vs `high`.*
26. ![Figure 26 — open_low_pairplot.png](../../eda_plots/open_low_pairplot.png)
  *Figure 26 — Pairwise plot: `open` vs `low` (alternate view).* 

**Suggested reading order**

- Start with hist/KDE for each price field to understand distributions.
- Inspect boxplots to spot outliers and range differences across fields.
- Use pairplots to identify correlations and joint behaviors between fields.
- Review combined `open_low_high` / `close_open_low_high` plots (and MA overlays) for time-series patterns and trend smoothing.

## Aggregated trend figures

The following weekly and monthly aggregation plots reduce short-term noise and highlight medium- and long-term behavior:

- ![Close weekly trend](../../eda_plots/Close_weekly.png) — Weekly `close` series (smoother than daily, shows medium-term cycles).
- ![Close monthly trend](../../eda_plots/Close_monthly.png) — Monthly `close` series (very smooth; emphasizes long-term trend and regime changes).
- ![Open weekly trend](../../eda_plots/Open_weekly.png) — Weekly `open` series.
- ![Open monthly trend](../../eda_plots/Open_monthly.png) — Monthly `open` series.
- ![High weekly trend](../../eda_plots/High_weekly.png) — Weekly `high` series.
- ![High monthly trend](../../eda_plots/High_monthly.png) — Monthly `high` series.
- ![Low weekly trend](../../eda_plots/Low_weekly.png) — Weekly `low` series.
- ![Low monthly trend](../../eda_plots/Low_monthly.png) — Monthly `low` series.

## Findings

- **Aggregated views (weekly/monthly):** Weekly plots preserve medium-term cycles and volatility spikes while removing daily noise; monthly plots produce very smooth trends that clearly show regime shifts and long-term growth. These aggregated views make it easier to spot structural events and confirm that recent years (2020–2025) contain accelerated growth and elevated variability.
- **Volatility concentration in recent periods:** Weekly and monthly overlays emphasize that volatility and drawdowns concentrate in recent decades (notably 2008, 2020), with faster recoveries and higher peak values in the last 5–7 years.
- **No dominant simple seasonality visible:** Aggregated plots do not show an obvious stable monthly or yearly seasonal cycle in level (some recurring patterns may exist in returns; further decomposition required to confirm).
- **Strong upward, non-stationary trend:** All price series (`open`, `high`, `low`, `close`) show a clear long-term upward trend, with recent values substantially higher than historical ranges. The trend dominates the series and should be removed or accounted for when modeling stationarity-sensitive methods.
- **Right-skewed, multimodal distributions:** Histograms and KDEs for price fields are right-skewed and show multiple modes — a large mass at lower historical price ranges and smaller peaks at higher ranges — reflecting long-run growth and structural regime changes.
- **Large spread and outliers:** Boxplots indicate wide interquartile ranges and several high-value outliers near recent peaks. These are expected for index-level series but may affect models sensitive to extreme values or assumptions of normality.
- **High pairwise correlation:** Pairplots show near-linear relationships between `open`, `high`, `low`, and `close`. This multicollinearity suggests choosing features carefully or using regularized models when including multiple OHLC fields.
- **Smoothing and trend confirmation with moving averages:** The MA10 and MA50 overlays smooth short-term noise and confirm persistent uptrends; crossovers highlight periods of trend acceleration or deceleration.
- **Seasonal/structural events visible:** Major drawdowns and rebounds (for example around 2008 and 2020) are visible in overlays and aggregated plots; treat these as regime events when backtesting and risk-testing.
- **Aggregated views (weekly/monthly):** Weekly plots preserve medium-term cycles and volatility spikes while removing daily noise; monthly plots emphasize long-term trends and regime shifts, making structural changes easier to spot.
- **Volatility concentration in recent periods:** Aggregated views show higher volatility and more dramatic drawdowns in recent decades, with faster recoveries and larger peak values in the last 5–7 years.
- **No dominant simple seasonality visible:** There is no obvious stable monthly or yearly seasonal pattern in level series; seasonal signals (if any) may appear in returns and require decomposition to confirm.

## Recommendations

- Use aggregated (weekly/monthly) series for robust trend analysis and daily/1-min series for fine-grained volatility or intraday modeling.
- For time-series modeling, transform to returns or log-returns and difference/detrend to achieve stationarity; always test stationarity after transformation.
- Prefer `close` or `returns(close)` as primary targets; include rolling volatility, lagged returns, and moving-average features for predictive models.
- Address outliers or heavy tails via robust scaling, winsorization, or models that handle non-Gaussian errors.
- I can compute and save numeric diagnostics (mean, median, skewness, kurtosis), a correlation matrix heatmap, returns distributions, and rolling volatility plots into `eda_plots` — tell me which outputs to generate.