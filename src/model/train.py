import pandas as pd
import numpy as np

import tensorflow as tf
from lightgbm import LGBMClassifier as lgb
from xgboost import XGBClassifier as xgb
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, precision_recall_curve
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import TimeSeriesSplit, train_test_split
from sklearn.metrics import make_scorer

import os
from pathlib import Path
import sys

import json
import matplotlib.pyplot as plt
from joblib import dump

ROOT_DIR = Path.cwd()
for parent in [ROOT_DIR] + list(ROOT_DIR.parents):
    if parent.name == 'SENSEX':
        ROOT_DIR = parent
        break

sys.path.append(str(ROOT_DIR))

filepath = os.path.join(ROOT_DIR, 'sensex_data', 'processed', 'new_sensex.csv')

os.makedirs(os.path.join(ROOT_DIR, 'Metrics'), exist_ok=True)
os.makedirs(os.path.join(ROOT_DIR, 'model_plots'), exist_ok=True)
os.makedirs(os.path.join(ROOT_DIR, 'models'), exist_ok=True)

class MODEL:
    def __init__(self, df, X_train, X_test, y_train, y_test):
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        self.df = df        

    def sharpe_ratio(self, preds, threshold=0.0005):
        test_df = self.df.loc[self.X_test.index].copy()
        test_df['position'] = np.where(preds > threshold, 1, np.where(preds < -threshold, -1, 0))
        test_df['strategy_returns'] = test_df['position'].shift(1) * test_df['Log_Return']

        active = test_df[test_df['position'].shift(1) != 0]['strategy_returns']  # only traded periods
        
        if len(active) == 0 or active.std() == 0:
            return 0.0

        sharpe = (active.mean() / active.std()) * np.sqrt(252)
        return sharpe

    def directional_accuracy(self, y_true, y_pred, threshold=0.0005):
        y_true = np.asarray(y_true)
        y_pred = np.asarray(y_pred)
        
        # only evaluate on confident predictions
        confident = np.abs(y_pred) > threshold
        
        if confident.sum() == 0:
            return 0.0
        
        actual_direction = np.sign(y_true[confident])
        pred_direction = np.sign(y_pred[confident])
        return np.mean(actual_direction == pred_direction)

    def model(self):
        models = {
            'lgb' : lgb(
                n_estimators=500,
                learning_rate=0.05,
                num_leaves=31,
                max_depth=-1,
                min_child_samples=20,
                subsample=0.8,
                colsample_bytree=0.8,
                reg_alpha=0.1,
                reg_lambda=0.1,
                class_weight='balanced'
            ),
            'xgb' : xgb(
                n_estimators=500,
                learning_rate=0.05,
                max_depth=6,
                subsample=0.8,
                colsample_bytree=0.8,
                reg_alpha=0.1,
                reg_lambda=0.1,
                scale_pos_weight=5212/1837
            ),
            'rf' : RandomForestClassifier(
                n_estimators=300,
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                max_features="sqrt",
                bootstrap=True,
                class_weight='balanced'
            ),
            'dt' : DecisionTreeClassifier(
                max_depth=5,
                min_samples_split=10,
                min_samples_leaf=5,
                max_features=None,
                criterion="log_loss",
                class_weight='balanced'
            )
        }

        for name, model in models.items():
            self.train_evaluate(name, model)
        

    def plot_precision_recall(self, name, probs, y_true):
        """Generate and save precision-recall curve."""
        precision, recall, _ = precision_recall_curve(y_true, probs)
        
        plt.figure(figsize=(8, 6))
        plt.plot(recall, precision, marker='o', label=f'{name} PR Curve')
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.title(f'Precision-Recall Curve: {name}')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        plot_path = os.path.join(ROOT_DIR, 'model_plots', f'{name}_pr_curve.png')
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Saved PR curve to {plot_path}")

    def train_evaluate(self, name, model):
        print(f"Training {name}...")

        model.fit(self.X_train, self.y_train)
        
        # Get probabilities or scores
        probs = None
        if hasattr(model, "predict_proba"):
            try:
                probs = model.predict_proba(self.X_test)[:, 1]
            except Exception:
                probs = None
        elif hasattr(model, "decision_function"):
            try:
                probs = model.decision_function(self.X_test)
            except Exception:
                probs = None
        
        # Apply 0.66 threshold if probabilities available, otherwise use default predictions
        if probs is not None:
            preds = (probs > 0.66).astype(int)
        else:
            preds = model.predict(self.X_test)

        accuracy = accuracy_score(self.y_test, preds)
        precision = precision_score(self.y_test, preds, zero_division=0)
        recall = recall_score(self.y_test, preds, zero_division=0)
        f1 = f1_score(self.y_test, preds, zero_division=0)

        roc_auc = None
        if probs is not None and len(np.unique(self.y_test)) == 2:
            try:
                roc_auc = float(roc_auc_score(self.y_test, probs))
            except Exception:
                roc_auc = None

        dir_acc = self.directional_accuracy(self.y_test.values, preds)
        sharpe = self.sharpe_ratio(preds)

        threshold = 0.0005
        coverage = float(np.mean(np.abs(preds) > threshold))

        metrics = {
            "accuracy": float(accuracy),
            "precision": float(precision),
            "recall": float(recall),
            "f1": float(f1),
            "roc_auc": roc_auc,
            "directional_accuracy": float(dir_acc),
            "sharpe_ratio": float(sharpe),
            "coverage": coverage
        }

        with open(os.path.join(ROOT_DIR, 'Metrics', f'{name}_metrics.json'), "w") as f:
            json.dump(metrics, f, indent=4)

        # Generate and save precision-recall curve
        if probs is not None:
            self.plot_precision_recall(name, probs, self.y_test.values)

        print(f"Accuracy: {accuracy:.4f}, Precision: {precision:.4f}, Recall: {recall:.4f}, F1: {f1:.4f}")
        if roc_auc is not None:
            print(f"ROC AUC: {roc_auc:.4f}")
        print("Sharpe:", sharpe)
        print("Directional acc:", dir_acc)
        print(f"Coverage (% of days traded): {coverage:.2%}")


    def tune_models(self):
        models = {
            "rf": RandomForestClassifier(random_state=42),
            "dt": DecisionTreeClassifier(random_state=42),
            "xgb": xgb(random_state=42),
            "lgb": lgb(random_state=42)
        }

        param_grids = {
            "rf": {
                "n_estimators": [100, 200, 300, 500],
                "max_depth": [None, 5, 10, 20],
                "min_samples_split": [2, 5, 10],
                "min_samples_leaf": [1, 2, 4],
                "max_features": ["sqrt", "log2", None],
                "bootstrap": [True, False],
                "class_weight":["balanced"]
            },

            "dt": {
                "max_depth": [3, 5, 10, 20, None],
                "min_samples_split": [2, 5, 10, 20],
                "min_samples_leaf": [1, 2, 5, 10],
                "max_features": [None, "sqrt", "log2"],
                "criterion": ["log_loss", "entropy", "gini"],
                "class_weight":["balanced"]
            },

            "xgb": {
                "n_estimators": [100, 200, 300, 500],
                "learning_rate": [0.01, 0.05, 0.1, 0.2],
                "max_depth": [3, 5, 6, 10],
                "subsample": [0.6, 0.8, 1.0],
                "colsample_bytree": [0.6, 0.8, 1.0],
                "gamma": [0, 0.1, 0.3],
                "reg_alpha": [0, 0.1, 0.5],
                "reg_lambda": [0.5, 1, 2],
                "scale_pos_weight":[5212/1837]
            },

            "lgb": {
                "n_estimators": [100, 200, 300, 500],
                "learning_rate": [0.01, 0.05, 0.1, 0.2],
                "num_leaves": [15, 31, 63, 127],
                "max_depth": [-1, 5, 10, 20],
                "min_child_samples": [10, 20, 30, 50],
                "subsample": [0.6, 0.8, 1.0],
                "colsample_bytree": [0.6, 0.8, 1.0],
                "reg_alpha": [0, 0.1, 0.5],
                "reg_lambda": [0, 0.1, 0.5],
                "class_weight":["balanced"]
            }
        }

        results = {}
        best_model = dict()

        scorer = make_scorer(f1_score)

        for name in models.keys():

            print(f"Tuning {name}...")

            tscv = TimeSeriesSplit(n_splits=3)
            search = RandomizedSearchCV(
                estimator=models[name],
                param_distributions=param_grids[name],
                n_iter=20,
                cv=tscv,
                scoring=scorer,
                random_state=42,
                n_jobs=-1
            )

            search.fit(self.X_train, self.y_train)

            results[name] = {
                "name" : name,
                "best_params": search.best_params_,
                "best_score": abs(float(search.best_score_)),
            }

            best_model[name] = {
                'best_estimator' : search.best_estimator_,
                'best_score' : search.best_score_
            }

        with open(os.path.join(ROOT_DIR, 'Metrics', 'random_search_results.json'), "w") as f:
            json.dump(results, f, indent=4)

        return best_model


if __name__ == '__main__':
    df = pd.read_csv(filepath)
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    df = df.set_index('Datetime')

    y = df['Up_Down']
    X = df.drop('Up_Down', axis=1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    
    train_model = MODEL(df, X_train, X_test, y_train, y_test)
    train_model.model()
    models = train_model.tune_models()

    # Generate PR curves for all tuned models
    for name, model_dict in models.items():
        best_model = model_dict['best_estimator']
        probs = None
        if hasattr(best_model, "predict_proba"):
            try:
                probs = best_model.predict_proba(X_test)[:, 1]
            except Exception:
                pass
        elif hasattr(best_model, "decision_function"):
            try:
                probs = best_model.decision_function(X_test)
            except Exception:
                pass
        
        if probs is not None:
            train_model.plot_precision_recall(f'{name}_tuned', probs, y_test.values)

    valid_models = {
        name: m for name, m in models.items()
        if np.std(m['best_estimator'].predict(X_test)) > 1e-6
    }
    
    best_name = max(valid_models, key=lambda x: valid_models[x]['best_score']) 
    best_model = valid_models[best_name]['best_estimator']
    train_model.train_evaluate('best_model', best_model)
    
    # Save the selected best model to disk in both 'models/' and 'model/'
    model_path = os.path.join(ROOT_DIR, 'models', f'{best_name}_best_model.joblib')
    try:
        dump(best_model, model_path)
        print(f"Saved best model to {model_path}")
    except Exception as e:
        print(f"Failed to save best model: {e}")
