# Model Documentation

## Overview

This document describes the training pipeline implemented in `src/model/train.py`. The pipeline trains and evaluates classifier models on the engineered dataset (`sensex_data/processed/new_sensex.csv`), saves per-model classification metrics, creates precision–recall plots, and persists the chosen best model to disk.

## Input and Target

- Input file: `sensex_data/processed/new_sensex.csv` with `Datetime` as the index.
- Target: `Up_Down` (binary label added during feature engineering).

## Models

The pipeline trains these classifiers:

- `LGBMClassifier` (`lgb`) — LightGBM
- `XGBClassifier` (`xgb`) — XGBoost
- `RandomForestClassifier` (`rf`)
- `DecisionTreeClassifier` (`dt`)

Default model arguments and class weighting are set in the code; XGBoost uses a `scale_pos_weight` tuned for class imbalance.

## Evaluation and Metrics

Each model is evaluated on the test set and the following metrics are saved to `Metrics/{model}_metrics.json`:

- `accuracy`
- `precision`
- `recall`
- `f1`
- `roc_auc` (when probability/score is available)
- `directional_accuracy` (custom; compares signs on confident predictions)
- `sharpe_ratio` (strategy-style Sharpe using `Log_Return` and predicted positions)
- `coverage` (fraction of days with non-zero position)

Notes:

- Predictions use a probability threshold of **0.66** when `predict_proba` is available; otherwise the model's discrete `predict()` output is used.
- `directional_accuracy` and `sharpe_ratio` use a confidence threshold internally (default 0.0005) to focus on meaningful moves.

## Precision–Recall Plots

- Precision–recall curves are generated and saved to `model_plots/` for each trained classifier. Filenames follow `{model}_pr_curve.png`.
- Tuned models (from `tune_models()`) also have PR curves saved as `{model}_tuned_pr_curve.png`.

## Hyperparameter Tuning

- `tune_models()` runs `RandomizedSearchCV` with `TimeSeriesSplit(n_splits=3)` and `n_iter=20`.
- The tuning objective uses `f1_score` as the scorer via `make_scorer(f1_score)`.
- Best parameters and best scores are written to `Metrics/random_search_results.json`.

## Best Model Selection & Persistence

After tuning the pipeline:

1. Tuned estimators are collected and filtered to remove near-constant predictors.
2. The model with the highest tuning `best_score` is selected as the `best_model`.
3. The selected `best_model` is evaluated and its metrics are saved.
4. The chosen model is saved to disk in folder at project root:
	- `models/{best_name}_best_model.joblib`

## Outputs

- `Metrics/` — per-model metrics JSONs and `random_search_results.json`.
- `model_plots/` — precision–recall PNGs for baseline and tuned models.
- `models/` and `model/` — serialized `joblib` files containing the selected best estimator.
