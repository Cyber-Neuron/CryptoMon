import os
from datetime import datetime

import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def load_data(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


def draw_kline(file_path: str, asset: str, interval: str = "1H"):
    df = load_data(file_path)
    df = df.sort_values("timestamp")
    df.set_index("timestamp", inplace=True)
    df = df.resample(interval).agg({"delta": "sum"})
    df["cum"] = df["delta"].cumsum()
    ohlc = df["cum"].resample(interval).ohlc()
    mpf.plot(ohlc, type="candle", style="charles", title=f"{asset} Flow Kline")
    plt.show()


if __name__ == "__main__":
    eth_path = os.path.join(DATA_DIR, "eth_history.csv")
    if os.path.exists(eth_path):
        draw_kline(eth_path, "ETH")
