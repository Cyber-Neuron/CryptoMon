import datetime

import pandas as pd
import requests
import yaml
from binance.um_futures import UMFutures
from sqlalchemy import create_engine

import os
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/exmonitor")
engine = create_engine(DATABASE_URL)


def load_config():
    with open("config.yaml") as f:
        config = yaml.safe_load(f)
    return config


def get_funding_rate(symbol="ETHUSDT"):
    cfg = load_config()
    client = UMFutures(
        key=cfg["binance"]["api_key"], secret=cfg["binance"]["api_secret"]
    )
    rates = client.funding_rate(symbol=symbol, limit=10)
    return pd.DataFrame(rates)


def store_funding_rate(symbol="ETHUSDT"):
    df = get_funding_rate(symbol)
    now = datetime.datetime.utcnow()
    df["symbol"] = symbol
    df["funding_time"] = pd.to_datetime(df["fundingTime"], unit="ms")
    df["snapshot_time"] = now
    df["funding_rate"] = df["fundingRate"].astype(float)
    df = df[["symbol", "funding_time", "funding_rate", "snapshot_time"]]
    df.to_sql("futures_funding_rate", engine, if_exists="append", index=False)
    return df


def get_open_interest(symbol="ETHUSDT"):
    cfg = load_config()
    client = UMFutures(
        key=cfg["binance"]["api_key"], secret=cfg["binance"]["api_secret"]
    )
    oi = client.open_interest(symbol=symbol)
    return oi


def store_open_interest(symbol="ETHUSDT"):
    oi = get_open_interest(symbol)
    now = datetime.datetime.utcnow()
    df = pd.DataFrame(
        [
            {
                "symbol": symbol,
                "open_interest": float(oi["openInterest"]),
                "snapshot_time": now,
            }
        ]
    )
    df.to_sql("futures_open_interest", engine, if_exists="append", index=False)
    return df


def get_liquidations(symbol="ETHUSDT"):
    url = f"https://fapi.binance.com/futures/data/orderLiquidation"
    params = {"symbol": symbol, "limit": 100}
    resp = requests.get(url, params=params)
    df = pd.DataFrame(resp.json())
    return df


def store_liquidations(symbol="ETHUSDT"):
    df = get_liquidations(symbol)
    now = datetime.datetime.utcnow()
    if not df.empty:
        df["symbol"] = symbol
        df["snapshot_time"] = now
        df["time"] = pd.to_datetime(df["time"], unit="ms") if "time" in df else now
        df = df[["symbol", "orderId", "price", "qty", "side", "time", "snapshot_time"]]
        df.rename(columns={"orderId": "order_id", "qty": "quantity"}, inplace=True)
        df.to_sql("futures_liquidations", engine, if_exists="append", index=False)
    return df


if __name__ == "__main__":
    print("Storing Funding Rate...")
    print(store_funding_rate().head())
    print("Storing Open Interest...")
    print(store_open_interest().head())
    print("Storing Liquidations...")
    print(store_liquidations().head())
