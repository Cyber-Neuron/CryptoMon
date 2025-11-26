import requests


def get_eth_usdt_price_at_unix(unix_ts: int) -> float:
    """
    使用 Binance K线接口获取指定 unix_ts（秒）时间点的 ETH/USDT 开盘价格。
    精度为 1 分钟，返回 float（价格）或 None。
    """
    ms = unix_ts * 1000  # Binance 使用毫秒单位
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": "ETHUSDT",
        "interval": "1m",
        "startTime": ms - 60_000,
        "endTime": ms,
    }

    try:
        resp = requests.get(url, params=params, timeout=5)
        data = resp.json()

        if isinstance(data, list) and len(data) > 0:
            open_price = float(data[0][1])  # [1] 是 open
            return open_price
        else:
            print("No data returned for that timestamp.")
            return None
    except Exception as e:
        print("Error:", e)
        return None


# # 例如：获取 2024-06-01 12:30:00 UTC 的 ETH/USDT 价格
# eth_price = get_eth_usdt_price_at_unix(1750466547)
# print("ETH/USDT at that time:", eth_price)
