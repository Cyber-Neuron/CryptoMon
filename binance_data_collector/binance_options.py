import datetime

import pandas as pd
import requests
from sqlalchemy import create_engine

import os
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/exmonitor")
engine = create_engine(DATABASE_URL)


def get_option_chain(symbol="ETHUSDT"):
    url = f"https://eapi.binance.com/eapi/v1/exchangeInfo"
    res = requests.get(url).json()
    symbols = [s["symbol"] for s in res["symbols"] if s["underlying"] == symbol]
    option_data = []
    for opt in symbols:
        ticker_url = f"https://eapi.binance.com/eapi/v1/ticker?symbol={opt}"
        tkr = requests.get(ticker_url).json()
        tkr["symbol"] = opt
        option_data.append(tkr)
    df = pd.DataFrame(option_data)
    return df


def store_option_chain(symbol="ETHUSDT"):
    df = get_option_chain(symbol)
    now = datetime.datetime.utcnow()
    if not df.empty:
        # 解析期权合约代码，提取标的、到期日、行权价、类型
        df["underlying"] = symbol
        df["snapshot_time"] = now

        # 假设合约代码格式: BTC-240628-50000-C
        def parse_option_code(code):
            parts = code.split("-")
            if len(parts) == 4:
                return (
                    parts[0],
                    parts[1],
                    float(parts[2]),
                    "CALL" if parts[3] == "C" else "PUT",
                )
            return symbol, None, None, None

        df[["underlying", "expiry_date", "strike", "option_type"]] = df["symbol"].apply(
            lambda x: pd.Series(parse_option_code(x))
        )
        df["expiry_date"] = pd.to_datetime(
            df["expiry_date"], format="%y%m%d", errors="coerce"
        )
        # 只保留主要字段
        for col in [
            "markPrice",
            "bidPrice",
            "askPrice",
            "vol",
            "openInterest",
            "impliedVolatility",
        ]:
            if col not in df:
                df[col] = None
        df = df[
            [
                "symbol",
                "underlying",
                "strike",
                "expiry_date",
                "option_type",
                "markPrice",
                "bidPrice",
                "askPrice",
                "impliedVolatility",
                "vol",
                "openInterest",
                "snapshot_time",
            ]
        ]
        df.rename(
            columns={
                "markPrice": "mark_price",
                "bidPrice": "bid_price",
                "askPrice": "ask_price",
                "impliedVolatility": "iv",
                "vol": "volume",
                "openInterest": "open_interest",
            },
            inplace=True,
        )
        df.to_sql("options_chain", engine, if_exists="append", index=False)
    return df


if __name__ == "__main__":
    print("Storing Option Chain...")
    print(store_option_chain().head())
