from datetime import datetime, timezone

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytz
import yfinance as yf

# ========= 参数设置 =========
usdt_csv = "arkham_transactionsethereum_tether_202506150000_202506170000.csv"
usdc_csv = "arkham_transactionsethereum_usd-coin_202506150000_202506170000.csv"
eth_csv = "arkham_transactionsethereum_ethereum_202506150000_202506170000.csv"
threshold_sigma = 0.8
output_timezone = "America/Toronto"


# ========= 处理函数 =========
def prepare_hourly(df, asset_name, freq="1H"):
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    # 确保时间戳是UTC时间
    if df["timestamp"].dt.tz is None:
        df["timestamp"] = df["timestamp"].dt.tz_localize("UTC")
    df["hour"] = df["timestamp"].dt.floor(freq)
    inflow = df[df["type"] == "inflow"].groupby("hour")["usd_amount"].sum()
    outflow = -df[df["type"] == "outflow"].groupby("hour")["usd_amount"].sum()
    combined = pd.DataFrame(
        {f"inflow_{asset_name}": inflow, f"outflow_{asset_name}": outflow}
    )
    combined[f"net_{asset_name}"] = combined[f"inflow_{asset_name}"].fillna(
        0
    ) - combined[f"outflow_{asset_name}"].fillna(0)
    return combined


# ========= 主流程 =========
df_usdt = pd.read_csv(usdt_csv)
df_usdc = pd.read_csv(usdc_csv)
df_eth = pd.read_csv(eth_csv)

hourly = (
    prepare_hourly(df_usdt, "USDT")
    .join(prepare_hourly(df_usdc, "USDC"), how="outer")
    .join(prepare_hourly(df_eth, "ETH"), how="outer")
    .fillna(0)
)

hourly["net_stable"] = hourly["net_USDT"] + hourly["net_USDC"]
stable_mean, stable_std = hourly["net_stable"].mean(), hourly["net_stable"].std()
eth_mean, eth_std = hourly["net_ETH"].mean(), hourly["net_ETH"].std()
stable_threshold, eth_threshold = (
    threshold_sigma * stable_std,
    threshold_sigma * eth_std,
)


def early_signal(row):
    if (
        row["net_stable"] > stable_mean + stable_threshold
        and row["net_ETH"] < eth_mean - eth_threshold
    ):
        return "Pump"
    elif (
        row["net_stable"] < stable_mean - stable_threshold
        and row["net_ETH"] > eth_mean + eth_threshold
    ):
        return "Dump"
    return None


def check_live_alert(last_rows):
    r = last_rows.sum()
    sig = early_signal(r)
    if sig:
        timestamp = last_rows.index[-1].tz_convert(output_timezone)
        print(
            f"[{timestamp.strftime('%Y-%m-%d %H:%M')}] {sig} alert – "
            f"stable Δ ${r['net_stable']:,.0f}, ETH Δ ${r['net_ETH']:,.0f}"
        )


# 检查每小时内每10分钟区间的实时报警
print("\nChecking for alerts in each time window:")
for i in range(0, len(hourly), 6):
    window = hourly.iloc[i : i + 6]
    if not window.empty:
        check_live_alert(window)


def classify(row):
    if (
        row["net_stable"] > stable_mean + stable_threshold
        and row["net_ETH"] < eth_mean - eth_threshold
    ):
        return "Pump"
    elif (
        row["net_stable"] < stable_mean - stable_threshold
        and row["net_ETH"] > eth_mean + eth_threshold
    ):
        return "Dump"
    return ""


hourly["classification"] = hourly.apply(classify, axis=1)
hourly = hourly.reset_index()

print("\n[调试] hourly数据头部:\n", hourly.head())
print("[调试] hourly最早时间:", hourly["hour"].min())
print("[调试] hourly最晚时间:", hourly["hour"].max())

result = hourly[hourly["classification"] != ""][
    ["hour", "net_USDT", "net_USDC", "net_stable", "net_ETH", "classification"]
]

if not result.empty:
    print("[调试] 资金流事件区间:", result["hour"].min(), result["hour"].max())

# ========= ========== 滚动均值+标准差 10分钟报警模块 ========== ==========
print("\nRolling 10min window early warning (rolling mean/std, last 6h):")
agg10 = (
    prepare_hourly(df_usdt, "USDT", freq="10T")
    .join(prepare_hourly(df_usdc, "USDC", freq="10T"), how="outer")
    .join(prepare_hourly(df_eth, "ETH", freq="10T"), how="outer")
    .fillna(0)
)

agg10["net_stable"] = agg10["net_USDT"] + agg10["net_USDC"]
window = 36  # 6小时滚动窗口
agg10["mean_stable"] = agg10["net_stable"].rolling(window).mean()
agg10["std_stable"] = agg10["net_stable"].rolling(window).std()
agg10["mean_eth"] = agg10["net_ETH"].rolling(window).mean()
agg10["std_eth"] = agg10["net_ETH"].rolling(window).std()


def rolling_signal(row, sigma_stable=0.8, sigma_eth=0.8):
    if np.isnan(row["mean_stable"]) or np.isnan(row["mean_eth"]):
        return ""
    if (
        row["net_stable"] > row["mean_stable"] + sigma_stable * row["std_stable"]
        and row["net_ETH"] < row["mean_eth"] - sigma_eth * row["std_eth"]
    ):
        return "Pump"
    if (
        row["net_stable"] < row["mean_stable"] - sigma_stable * row["std_stable"]
        and row["net_ETH"] > row["mean_eth"] + sigma_eth * row["std_eth"]
    ):
        return "Dump"
    return ""


agg10["rolling_signal"] = agg10.apply(rolling_signal, axis=1)
alerts = agg10[agg10["rolling_signal"] != ""]
alerts.index = alerts.index.tz_convert(output_timezone)

# 输出最新10条报警
print(
    alerts[
        [
            "net_stable",
            "net_ETH",
            "mean_stable",
            "std_stable",
            "mean_eth",
            "std_eth",
            "rolling_signal",
        ]
    ].tail(10)
)

if not agg10.empty:
    print("[调试] 10分钟agg10数据index起止:", agg10.index.min(), agg10.index.max())

# ========= 获取ETH价格并标注 =========
start_date = (
    hourly["hour"].dt.tz_convert("UTC").min().strftime("%Y-%m-%d")
    if not result.empty
    else hourly["hour"].min().strftime("%Y-%m-%d")
)

end_date = (
    (hourly["hour"].dt.tz_convert("UTC").max() + pd.Timedelta(days=1)).strftime(
        "%Y-%m-%d"
    )
    if not result.empty
    else (hourly["hour"].max() + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
)

print(f"Fetching ETH data from {start_date} to {end_date}")
eth = yf.download("ETH-USD", interval="30m", start=start_date, end=end_date)
# print(eth.index.tz, eth)
# 1 / 0
print("ETH data shape:", eth.shape if eth is not None else "None")

if eth is not None and not eth.empty:
    print("ETH原始数据index[0:5]:", eth.index[:5])
    print("ETH原始数据index tz:", eth.index.tz)

    # 确保ETH数据是UTC时间
    # if eth.index.tz is None:
    #     eth.index = eth.index.tz_localize("UTC")
    # eth.index = eth.index.tz_convert(output_timezone)

    print("ETH index after转换[0:5]:", eth.index[:5])
    print("ETH数据index起止:", eth.index.min(), eth.index.max())

    # 确保事件时间也是UTC时间
    event_times = pd.DatetimeIndex(result["hour"])
    if event_times.tz is None:
        event_times = event_times.tz_localize("UTC")
    event_times = event_times.tz_convert(output_timezone)

    print("事件event_times[0:5]:", event_times[:5])
    print("事件区间:", event_times.min(), event_times.max())
    # print(eth)
    # 1 / 0
    nearest_idx = []
    print("Finding nearest price points for events")
    for event_time in event_times:
        idx = eth.index.searchsorted(event_time)
        if idx >= len(eth):
            idx = len(eth) - 1
        nearest_idx.append(idx)
    print("Found nearest indices:", nearest_idx)
    plt.figure(figsize=(14, 6))
    print("Plotting ETH price line")
    plt.plot(eth.index, eth["Close"], label="ETH-USD Close", linewidth=1.5)
    print("Plotting event markers")
    print("Number of events:", len(result))
    print("Number of indices:", len(nearest_idx))
    for i, (_, row) in enumerate(result.iterrows()):
        print(f"Processing event {i}")
        if i < len(nearest_idx):
            x = eth.index[nearest_idx[i]]
            y = eth["Close"].iloc[nearest_idx[i]]
            label = row["classification"]
            color = "red" if label == "Dump" else "green"
            print(f"Plotting event {i}: time={x}, price={y}, type={label}")
            plt.axvline(
                x=x,
                color=color,
                alpha=0.5,
                linestyle="--",
                label=(
                    label
                    if label not in plt.gca().get_legend_handles_labels()[1]
                    else ""
                ),
            )
            plt.annotate(
                label,
                (x, y),
                xytext=(0, 10),
                textcoords="offset points",
                color=color,
                fontsize=12,
                ha="center",
                va="bottom",
                weight="bold",
                bbox=dict(facecolor="white", alpha=0.7, edgecolor="none", pad=2),
            )
    print("Setting up plot formatting")
    plt.title("ETH-USD 30min K-Line with On-Chain Pump/Dump Events (Eastern Time)")
    plt.xlabel("Time")
    plt.ylabel("Price (USD)")
    plt.gca().xaxis.set_major_formatter(
        mdates.DateFormatter("%Y-%m-%d %H:%M", tz=output_timezone)
    )
    plt.gcf().autofmt_xdate()
    plt.gca().xaxis.set_major_locator(
        mdates.HourLocator(interval=2, tz=output_timezone)
    )
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    print("Showing plot")
    plt.show()
    print("Plot shown")
else:
    print(
        "Warning: No ETH price data was downloaded. Please check the date range and internet connection."
    )
