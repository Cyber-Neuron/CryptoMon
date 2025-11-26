from datetime import datetime, timedelta

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf

# ========= 参数设置 =========
usdt_csv = "arkham_transactionsethereum_tether_202506161200_202506171600.csv"
usdc_csv = "arkham_transactionsethereum_usd-coin_202506161200_202506171600.csv"
eth_csv = "arkham_transactionsethereum_ethereum_202506161200_202506171600.csv"
threshold_sigma = 0.5  # 阈值灵敏度
output_timezone = "America/Toronto"  # 统一使用 UTC，不再做任何时区转换


# ========= 处理函数 =========
def prepare(df: pd.DataFrame, asset: str, freq: str = "1H") -> pd.DataFrame:
    """按指定 freq 聚合 (inflow‑outflow) 并给出 net 值"""
    df["timestamp"] = pd.to_datetime(df["timestamp"])  # 默认即 UTC
    df["bucket"] = df["timestamp"].dt.floor(freq)
    inflow = df[df["type"] == "inflow"].groupby("bucket")["usd_amount"].sum()
    outflow = -df[df["type"] == "outflow"].groupby("bucket")["usd_amount"].sum()
    res = pd.DataFrame({f"in_{asset}": inflow, f"out_{asset}": outflow})
    res[f"net_{asset}"] = res[f"in_{asset}"].fillna(0) - res[f"out_{asset}"].fillna(0)
    return res


# ========= 读取 CSV =========
raw_usdt = pd.read_csv(usdt_csv)
raw_usdc = pd.read_csv(usdc_csv)
raw_eth = pd.read_csv(eth_csv)

hourly = (
    prepare(raw_usdt, "USDT")
    .join(prepare(raw_usdc, "USDC"), how="outer")
    .join(prepare(raw_eth, "ETH"), how="outer")
    .fillna(0)
)
# hourly.index = hourly.index.tz_localize("UTC").tz_convert(output_timezone)

# === Pump / Dump 判定 ===
hourly["net_stable"] = hourly["net_USDT"] + hourly["net_USDC"]
s_mean, s_std = hourly["net_stable"].mean(), hourly["net_stable"].std()
e_mean, e_std = hourly["net_ETH"].mean(), hourly["net_ETH"].std()
thr_stable, thr_eth = threshold_sigma * s_std, threshold_sigma * e_std


def classify(r):
    if r["net_stable"] > s_mean + thr_stable and r["net_ETH"] < e_mean - thr_eth:
        return "Pump"
    if r["net_stable"] < s_mean - thr_stable and r["net_ETH"] > e_mean + thr_eth:
        return "Dump"
    return ""


hourly["signal"] = hourly.apply(classify, axis=1)
events = hourly[hourly["signal"] != ""].copy()
print("Pump / Dump events (UTC):")
print(events[["net_stable", "net_ETH", "signal"]].head())

# === 10 分钟滚动预警 ===
agg10 = (
    prepare(raw_usdt, "USDT", "10T")
    .join(prepare(raw_usdc, "USDC", "10T"), how="outer")
    .join(prepare(raw_eth, "ETH", "10T"), how="outer")
    .fillna(0)
)

agg10["net_stable"] = agg10["net_USDT"] + agg10["net_USDC"]
window = 36  # 6 h 滚动窗口
agg10["ms"], agg10["ss"] = (
    agg10["net_stable"].rolling(window).mean(),
    agg10["net_stable"].rolling(window).std(),
)
agg10["me"], agg10["se"] = (
    agg10["net_ETH"].rolling(window).mean(),
    agg10["net_ETH"].rolling(window).std(),
)
# agg10.index = agg10.index.tz_localize("UTC").tz_convert(output_timezone)


def warn(r, s_sig=0.8, e_sig=0.8):
    if np.isnan(r["ms"]) or np.isnan(r["me"]):
        return ""
    if (
        r["net_stable"] > r["ms"] + s_sig * r["ss"]
        and r["net_ETH"] < r["me"] - e_sig * r["se"]
    ):
        return "Pump_warn"
    if (
        r["net_stable"] < r["ms"] - s_sig * r["ss"]
        and r["net_ETH"] > r["me"] + e_sig * r["se"]
    ):
        return "Dump_warn"
    return ""


agg10["warn"] = agg10.apply(warn, axis=1)
warnings = agg10[agg10["warn"] != ""]
print("\nEarly warnings (UTC):")
print(warnings[["net_stable", "net_ETH", "warn"]].head())

# === ETH 价格 (UTC index) ===
try:
    import yfinance as yf

    start_d = (hourly.index.min() - timedelta(days=0)).strftime("%Y-%m-%d")
    end_d = (hourly.index.max() + timedelta(days=1)).strftime("%Y-%m-%d")
    price = yf.download(
        "ETH-USD", interval="30m", start=start_d, end=end_d, progress=False
    )
    # if price.index.tz is None:
    # price.index = price.index.tz_convert(output_timezone)
except Exception as e:
    print("yfinance error", e)
    price = pd.DataFrame()
# print(price.index.tz)
# 1 / 0
# === 绘图 ===
plt.figure(figsize=(14, 7))
if not price.empty:
    plt.plot(
        price.index,
        price["Close"],
        color="black",
        linewidth=1.0,
        label="ETH Price (UTC)",
    )

for ts, sig in events["signal"].items():
    color = "green" if sig == "Pump" else "red"
    plt.axvline(
        x=ts,
        color=color,
        linestyle="--",
        linewidth=1.2,
        label=sig if sig not in plt.gca().get_legend_handles_labels()[1] else "",
    )

for ts, w in warnings["warn"].items():
    color = "lightgreen" if "Pump" in w else "salmon"
    plt.axvline(
        x=ts,
        color=color,
        linestyle=":",
        linewidth=1.0,
        alpha=0.5,
        label=w if w not in plt.gca().get_legend_handles_labels()[1] else "",
    )

plt.title("On‑Chain Pump / Dump Events & Early Warnings (UTC)")
plt.xlabel("UTC Time")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()
