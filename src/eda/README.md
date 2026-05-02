**Exploratory Data Analysis (EDA) Summary**

This README reflects the current behavior of `src/eda/eda.py` and the plots saved under `eda_plots/`.

## Purpose

- Describe the SENSEX price dataset.
- Check distributions, outliers, and correlations.
- Visualize weekly and monthly trends.
- Compare `Open`, `High`, `Low`, and `Close` over time.

## Data Handling in `eda.py`

- Input file: `sensex_data/raw/sensex.csv`.
- `Volume` values equal to zero are replaced with random integers between the minimum and maximum observed volume.
- `Datetime` is converted to datetime and set as the index.
- The dataframe is sorted by time before plots are generated.

## Plot Output Folder

All plots are saved to `eda_plots/` at the project root. The helper in `eda.py` uses the exact path:

`eda_plots/{plot_name}.png`

## Plot Types Created

- `hist` for distribution shape
- `kde` for smoothed distribution density
- `box` for spread and outliers
- `bar` for aggregated value visualization
- `pairplot` for pairwise relationships
- combined time-series overlays for `Close`, `Open`, `Low`, and `High`
- rolling mean overlays for 10-period and 50-period windows
- weekly and monthly resampled trend plots

## Files in `eda_plots/`

### Daily distribution plots

- `close_bar.png`
- `close_box.png`
- `close_hist.png`
- `close_kde.png`
- `close_high_pairplot.png`
- `close_low_pairplot.png`
- `close_open_pairplot.png`
- `close_open_low_high.png`
- `close_open_low_high_ma10.png`
- `close_open_low_high_ma50.png`
- `high_bar.png`
- `high_box.png`
- `high_hist.png`
- `high_kde.png`
- `low_bar.png`
- `low_box.png`
- `low_hist.png`
- `low_kde.png`
- `low_high_pairplot.png`
- `open_bar.png`
- `open_box.png`
- `open_hist.png`
- `open_kde.png`
- `open_high_pairplot.png`
- `open_low_pairplot.png`

### Weekly and monthly trend plots

- `Close_weekly.png`
- `Close_monthly.png`
- `Open_weekly.png`
- `Open_monthly.png`
- `High_weekly.png`
- `High_monthly.png`
- `Low_weekly.png`
- `Low_monthly.png`

## Figures

The links below point to the current files under `eda_plots/`.

1. ![close_hist](../../eda_plots/close_hist.png)
2. ![close_kde](../../eda_plots/close_kde.png)
3. ![close_box](../../eda_plots/close_box.png)
4. ![close_bar](../../eda_plots/close_bar.png)
5. ![close_open_pairplot](../../eda_plots/close_open_pairplot.png)
6. ![close_high_pairplot](../../eda_plots/close_high_pairplot.png)
7. ![close_low_pairplot](../../eda_plots/close_low_pairplot.png)
8. ![close_open_low_high](../../eda_plots/close_open_low_high.png)
9. ![close_open_low_high_ma10](../../eda_plots/close_open_low_high_ma10.png)
10. ![close_open_low_high_ma50](../../eda_plots/close_open_low_high_ma50.png)
11. ![open_hist](../../eda_plots/open_hist.png)
12. ![open_kde](../../eda_plots/open_kde.png)
13. ![open_box](../../eda_plots/open_box.png)
14. ![open_bar](../../eda_plots/open_bar.png)
15. ![open_high_pairplot](../../eda_plots/open_high_pairplot.png)
16. ![open_low_pairplot](../../eda_plots/open_low_pairplot.png)
17. ![high_hist](../../eda_plots/high_hist.png)
18. ![high_kde](../../eda_plots/high_kde.png)
19. ![high_box](../../eda_plots/high_box.png)
20. ![high_bar](../../eda_plots/high_bar.png)
21. ![low_hist](../../eda_plots/low_hist.png)
22. ![low_kde](../../eda_plots/low_kde.png)
23. ![low_box](../../eda_plots/low_box.png)
24. ![low_bar](../../eda_plots/low_bar.png)
25. ![low_high_pairplot](../../eda_plots/low_high_pairplot.png)
26. ![Close_weekly](../../eda_plots/Close_weekly.png)
27. ![Close_monthly](../../eda_plots/Close_monthly.png)
28. ![Open_weekly](../../eda_plots/Open_weekly.png)
29. ![Open_monthly](../../eda_plots/Open_monthly.png)
30. ![High_weekly](../../eda_plots/High_weekly.png)
31. ![High_monthly](../../eda_plots/High_monthly.png)
32. ![Low_weekly](../../eda_plots/Low_weekly.png)
33. ![Low_monthly](../../eda_plots/Low_monthly.png)

## Main Findings

- Price series are strongly upward trending and non-stationary.
- Histograms and KDE plots are right-skewed and reflect long-run regime shifts.
- Boxplots show wide spreads and high-end outliers.
- Pairplots show strong linear relationships between `Open`, `High`, `Low`, and `Close`.
- Moving-average overlays smooth noise and confirm the long-term trend.
- Weekly and monthly resampling reduce noise and make regime changes easier to see.