"""
This file performs a comprehensive Exploratory Data Analysis (EDA) on the sensex.csv dataset.

The analysis focuses on understanding the structure and behavior of the data through the following aspects:

    Distribution - Examining how values are spread across each feature
    Correlation - Identifying relationships between variables
    Missing Values - Detecting and handling incomplete data
    Outliers - Identifying extreme or unusual values
    Patterns Over Time - Analyzing trends in time-series data
    Frequency Analysis - Understanding value occurrences and density
    Feature Comparisons - Comparing Open, Close, High, and Low prices
    Moving Averages - Computing and visualizing trends using 10-day and 50-day windows
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from pathlib import Path
ROOT_DIR = Path.cwd()

for parent in [ROOT_DIR] + list(ROOT_DIR.parents):
    if parent.name == 'SENSEX':
        ROOT_DIR = parent
        break

import sys
sys.path.append(str(ROOT_DIR))

import os
os.makedirs(os.path.join(ROOT_DIR, 'eda_plots'), exist_ok=True)

def saveimg(name,fig=None):
    filename = os.path.join(ROOT_DIR, 'eda_plots', f'{name}.png')

    if fig:
        fig.savefig(filename, bbox_inches='tight', dpi=300)
    else:
        plt.savefig(filename, bbox_inches='tight', dpi=300)

    plt.close()

if __name__ == '__main__':
    df = pd.read_csv(os.path.join(ROOT_DIR, 'sensex_data\\sensex.csv'))

    print(df.isna().sum())

    mask = df['Volume'] == 0
    df.loc[mask, 'Volume'] = np.random.randint(
        df['Volume'].min(),
        df['Volume'].max(),
        size=mask.sum()
    )

    df['Datetime'] = pd.to_datetime(df['Datetime'])
    df.set_index('Datetime', inplace=True)
    df.sort_index(inplace=True)

    print(df.corr())

    for col in ['Close', 'Open', 'Low', 'High']:
        plt.figure(figsize=(12,8))
        df[col].plot(kind='box')
        saveimg(f'{col.lower()}_box')

        plt.figure(figsize=(12,8))
        df[col].plot(kind='kde')
        saveimg(f'{col.lower()}_kde')

        plt.figure(figsize=(12,8))
        df[col].plot(kind='hist', bins=20)
        saveimg(f'{col.lower()}_hist')

        plt.figure(figsize=(12,8))
        df[col].plot(kind='bar')
        saveimg(f'{col.lower()}_bar')

    for col in ['Close', 'Open', 'Low', 'High']:
        df_weekly = df[col].resample('W').mean()
        df_weekly.plot(figsize=(12,6), title=f"Weekly {col} Trend")
        saveimg(f'{col}_weekly')
    
    for col in ['Close', 'Open', 'Low', 'High']:
        df_monthly = df[col].resample('M').mean()
        df_monthly.plot(figsize=(12,6), title=f"Monthly {col} Trend")
        saveimg(f'{col}_monthly')

    g = sns.pairplot(df[['Close', 'Open']], kind='kde')
    saveimg('close_open_pairplot', g.figure)
    g = sns.pairplot(df[['Close', 'Low']], kind='kde')
    saveimg('close_low_pairplot', g.figure)
    g = sns.pairplot(df[['Close', 'High']], kind='kde')
    saveimg('close_high_pairplot', g.figure)
    g = sns.pairplot(df[['Open', 'Low']], kind='kde')
    saveimg('open_low_pairplot', g.figure)
    g = sns.pairplot(df[['Open', 'High']], kind='kde')
    saveimg('open_high_pairplot', g.figure)
    g = sns.pairplot(df[['Low', 'High']], kind='kde')
    saveimg('low_high_pairplot', g.figure)

    df_reset = df.reset_index()

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    df_reset.plot(kind='scatter', x='Datetime', y='Close', ax=axes[0,0])
    df_reset.plot(kind='scatter', x='Datetime', y='Open',  ax=axes[0,1])
    df_reset.plot(kind='scatter', x='Datetime', y='High',  ax=axes[1,0])
    df_reset.plot(kind='scatter', x='Datetime', y='Low',   ax=axes[1,1])
    plt.tight_layout()
    saveimg('close_open_low_high')
    plt.show()

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    df['Close'].rolling(window=10).mean().plot(ax=axes[0,0])
    df['Open'].rolling(window=10).mean().plot(ax=axes[0,1])
    df['Low'].rolling(window=10).mean().plot(ax=axes[1,0])
    df['High'].rolling(window=10).mean().plot(ax=axes[1,1])
    plt.tight_layout()
    saveimg('close_open_low_high_ma10')
    plt.show()

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    df['Close'].rolling(window=50).mean().plot(ax=axes[0,0])
    df['Open'].rolling(window=50).mean().plot(ax=axes[0,1])
    df['Low'].rolling(window=50).mean().plot(ax=axes[1,0])
    df['High'].rolling(window=50).mean().plot(ax=axes[1,1])
    plt.tight_layout()
    saveimg('close_open_low_high_ma50')
    plt.show()