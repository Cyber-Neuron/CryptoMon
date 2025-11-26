import datetime

import pandas as pd
import yaml
from binance.client import Client
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert

import os
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/exmonitor")
engine = create_engine(DATABASE_URL)


def load_config():
    with open("config.yaml") as f:
        config = yaml.safe_load(f)
    return config


def get_order_book(symbol="ETHUSDT", limit=100):
    cfg = load_config()
    client = Client(cfg["binance"]["api_key"], cfg["binance"]["api_secret"])
    ob = client.get_order_book(symbol=symbol, limit=limit)
    bids = pd.DataFrame(ob["bids"], columns=["price", "quantity"]).astype(float)
    asks = pd.DataFrame(ob["asks"], columns=["price", "quantity"]).astype(float)
    return bids, asks


def store_order_book(symbol="ETHUSDT", limit=100):
    bids, asks = get_order_book(symbol, limit)
    now = datetime.datetime.utcnow()
    bids["symbol"] = symbol
    bids["side"] = "bid"
    bids["snapshot_time"] = now
    asks["symbol"] = symbol
    asks["side"] = "ask"
    asks["snapshot_time"] = now
    df = pd.concat([bids, asks], ignore_index=True)
    df.rename(columns={"price": "price", "quantity": "quantity"}, inplace=True)
    df = df[["symbol", "side", "price", "quantity", "snapshot_time"]]
    df.to_sql("spot_order_book", engine, if_exists="append", index=False)
    return df


def get_agg_trades(symbol="ETHUSDT", limit=100):
    cfg = load_config()
    client = Client(cfg["binance"]["api_key"], cfg["binance"]["api_secret"])
    trades = client.get_aggregate_trades(symbol=symbol, limit=limit)
    return pd.DataFrame(trades)


def store_agg_trades(symbol="ETHUSDT", limit=100):
    df = get_agg_trades(symbol, limit)
    now = datetime.datetime.utcnow()
    df["symbol"] = symbol
    df["snapshot_time"] = now
    df["trade_time"] = pd.to_datetime(df["T"], unit="ms")
    df["is_buyer_maker"] = df["m"]
    df.rename(
        columns={
            "a": "agg_trade_id",
            "p": "price",
            "q": "quantity",
            "f": "first_trade_id",
            "l": "last_trade_id",
        },
        inplace=True,
    )
    df = df[
        [
            "symbol",
            "agg_trade_id",
            "price",
            "quantity",
            "first_trade_id",
            "last_trade_id",
            "trade_time",
            "is_buyer_maker",
            "snapshot_time",
        ]
    ]
    df.to_sql("spot_agg_trades", engine, if_exists="append", index=False)
    return df


if __name__ == "__main__":
    print("Storing Order Book...")
    print(store_order_book().head())
    print("Storing Agg Trades...")
    print(store_agg_trades().head())
