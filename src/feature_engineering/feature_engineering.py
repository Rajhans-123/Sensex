"""
This files performs features engineering based on the key findings based on the
Exploratory Data Analysis done before.

Features which will be added to the the sensex.csv dataset are:
    log transformation - reduces skewness
    MA10 - Moving Average (window = 10) for model to learn better by removing noise and capturing short term trend
    MA50 - Moving Average (window = 50) for model to learn better by removing noise and 
    capturing long term trend   
    EMA - window 10, 50 for capturing trend more smoothly
    Volatility - windows - 10, 20, 50 for catching the market uncertainity
    Pct change - this is the Target we have to predict
"""

import numpy as np
import pandas as pd
import os

from pathlib import Path
ROOT_DIR = Path.cwd()

for parent in [ROOT_DIR] + list(ROOT_DIR.parents):
    if parent.name == 'SENSEX':
        ROOT_DIR = parent
        break

import sys
sys.path.append(str(ROOT_DIR))

def feature_engineering(df):
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    df.set_index('Datetime', inplace=True)

    # Log prices
    df['Close_log'] = np.log(df['Close'])
    df['Open_log'] = np.log(df['Open'])
    df['Low_log'] = np.log(df['Low'])
    df['High_log'] = np.log(df['High'])
    df['Volume_log'] = np.log1p(df['Volume'])

    # Moving averages
    df['MA_10'] = df['Close_log'].rolling(window=10).mean()
    df['MA_50'] = df['Close_log'].rolling(window=50).mean()
    df['ma_cross'] = df['MA_10'] - df['MA_50']

    # EMAs
    df['EMA_10'] = df['Close_log'].ewm(span=10, adjust=False).mean()
    df['EMA_50'] = df['Close_log'].ewm(span=50, adjust=False).mean()

    # Returns and log return
    df['Log_Return'] = df['Close_log'].diff()

    # Volatility
    df['Volatility_10'] = df['Log_Return'].rolling(window=10).std()
    # df['Volatility_20'] = df['Log_Return'].rolling(window=20).std()
    df['Volatility_50'] = df['Log_Return'].rolling(window=50).std()
    # df['vol_ratio'] = df['Volatility_10'] / df['Volatility_50']

    # Lagged returns (replacing raw price lags)
    # df['lag_1'] = df['Log_Return'].shift(1)
    df['lag_2'] = df['Log_Return'].shift(2)
    df['lag_3'] = df['Log_Return'].shift(3)

    # Momentum (return-based)
    df['momentum'] = df['Log_Return'].rolling(5).sum()
    # df['return_5'] = df['Log_Return'].rolling(5).mean()

    # RSI
    delta = df['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = (100 - (100 / (1 + rs)) - 50) / 50  # normalized to [-1, 1]

    # Bollinger Bands (20-period, 2 std)
    bb_period = 20
    bb_std = 2
    bb_ma = df['Close'].rolling(window=bb_period).mean()
    bb_std_dev = df['Close'].rolling(window=bb_period).std()
    df['BB_Upper'] = bb_ma + (bb_std * bb_std_dev)
    df['BB_Lower'] = bb_ma - (bb_std * bb_std_dev)
    df['BB_Width'] = (df['BB_Upper'] - df['BB_Lower']) / bb_ma
    df['BB_Position'] = (df['Close'] - df['BB_Lower']) / (df['BB_Upper'] - df['BB_Lower'])

    # MACD (12, 26, 9)
    ema_12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema_26 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = ema_12 - ema_26
    df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['MACD_Histogram'] = df['MACD'] - df['MACD_Signal']

    # Intraday features
    # df['range_ratio'] = (df['High'] - df['Low']) / df['High']
    # df['close_position'] = (df['Close'] - df['Low']) / (df['High'] - df['Low'])

    # Volume features
    # df['volume_change'] = df['Volume_log'].diff()
    # df['volume_ma_ratio'] = df['Volume_log'] / df['Volume_log'].rolling(10).mean()
    df['Expected_Pct'] = df['Log_Return'].shift(-1)

    # Target
    df['Up_Down'] = (((df['High'] - df['Close']) / df['High']) > 0.01).astype(int)

    # Lagged target
    # df['lag_target_1'] = df['Expected_Pct'].shift(1)

    # Drop non-stationary raw prices
    df.drop(['Open', 'High', 'Low', 'Close', 'Volume', 'Expected_Pct'], axis=1, inplace=True)

    df = df.dropna()
    return df

def save_data(df):
    df.to_csv(os.path.join(ROOT_DIR, 'sensex_data', 'processed', 'new_sensex.csv'), index=True)

if __name__ == '__main__':
    df = pd.read_csv(os.path.join(ROOT_DIR, 'sensex_data', 'raw', 'sensex.csv'))
    df = feature_engineering(df)
    save_data(df)
