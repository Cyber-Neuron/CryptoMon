from datetime import timedelta

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytz
import yfinance as yf

# =============================================================
# CONFIGURATION
# =============================================================
WINDOW_HOURS = 1  # hourly pre‑alert rolling window (hours)
WINDOW_MIN = 5  # minute aggregation for fine‑grained alert
ROLLING_BINS = 72  # 36 × 10‑min = 6‑hour window for fine‑grained alert

# CSV paths (must exist in current directory)
usdt_path = "csv/arkham_transactionsethereum_tether_202506170000_202506172200.csv"
usdc_path = "csv/arkham_transactionsethereum_usd-coin_202506170000_202506172200.csv"
eth_path = "csv/arkham_transactionsethereum_ethereum_202506170000_202506172200.csv"

# =============================================================
# Helper functions
# =============================================================


def load_and_bucket(path: str, label: str, freq: str = "H") -> pd.Series:
    """Load Arkham CSV and resample `usd_amount` to the given frequency."""
    df = pd.read_csv(path, parse_dates=["timestamp"])
    df.set_index("timestamp", inplace=True)
    # Only localize if not already timezone-aware
    if df.index.tz is None:
        df.index = df.index.tz_localize("UTC")
    return df["usd_amount"].resample(freq).sum().rename(label)


def prepare(path: str, label: str, freq: str) -> pd.DataFrame:
    """Return DataFrame[net_{label}] for resampled freq (e.g. '10T')."""
    series = load_and_bucket(path, label, freq)
    return series.rename(f"net_{label}").to_frame()


# =============================================================
# HOURLY FLOW DATA (original logic)
# =============================================================
usdt_hour = load_and_bucket(usdt_path, "usdt")
usdc_hour = load_and_bucket(usdc_path, "usdc")
eth_hour = load_and_bucket(eth_path, "eth_usd")

flows = pd.concat([usdt_hour, usdc_hour, eth_hour], axis=1).fillna(0)
flows["stablecoin_net"] = flows["usdt"] + flows["usdc"]

# Detect pump / dump windows
p = 0.7
st_in = flows["stablecoin_net"].quantile(p)
st_out = flows["stablecoin_net"].quantile(1 - p)
eth_in = flows["eth_usd"].quantile(p)
eth_out = flows["eth_usd"].quantile(1 - p)

events = []
for ts, row in flows.iterrows():
    if row["stablecoin_net"] >= st_in and row["eth_usd"] <= eth_out:
        events.append(
            {
                "time": ts,
                "type": "拉盘 (pump)",
                "stablecoin_net_M": row["stablecoin_net"] / 1e6,
                "eth_net_M": row["eth_usd"] / 1e6,
            }
        )
    elif row["stablecoin_net"] <= st_out and row["eth_usd"] >= eth_in:
        events.append(
            {
                "time": ts,
                "type": "暴跌 (dump)",
                "stablecoin_net_M": row["stablecoin_net"] / 1e6,
                "eth_net_M": row["eth_usd"] / 1e6,
            }
        )

events_df = pd.DataFrame(events)

# =============================================================
# HOURLY DUMP‑RISK PRE‑ALERT
# =============================================================
dump_flags = []
for i, ts in enumerate(flows.index):
    if i < WINDOW_HOURS:
        dump_flags.append(False)
        continue
    window = flows.iloc[i - WINDOW_HOURS : i][["stablecoin_net", "eth_usd"]]
    avg_stable, std_stable = (
        window["stablecoin_net"].mean(),
        window["stablecoin_net"].std(),
    )
    avg_eth, std_eth = window["eth_usd"].mean(), window["eth_usd"].std()
    stable_th = avg_stable - 0.5 * std_stable
    eth_th = avg_eth + 0.5 * std_eth
    last_row = flows.iloc[i]
    dump_flags.append(
        last_row["stablecoin_net"] < stable_th and last_row["eth_usd"] > eth_th
    )

flows["dump_risk"] = dump_flags

# =============================================================
# 10‑MINUTE HIGH‑RESOLUTION WARNINGS
# =============================================================
raw_usdt_10 = prepare(usdt_path, "USDT", f"{WINDOW_MIN}T")
raw_usdc_10 = prepare(usdc_path, "USDC", f"{WINDOW_MIN}T")
raw_eth_10 = prepare(eth_path, "ETH", f"{WINDOW_MIN}T")

agg10 = (
    raw_usdt_10.join(raw_usdc_10, how="outer").join(raw_eth_10, how="outer").fillna(0)
)
agg10["net_stable"] = agg10["net_USDT"] + agg10["net_USDC"]

agg10["ms"] = agg10["net_stable"].rolling(ROLLING_BINS).mean()
agg10["ss"] = agg10["net_stable"].rolling(ROLLING_BINS).std()
agg10["me"] = agg10["net_ETH"].rolling(ROLLING_BINS).mean()
agg10["se"] = agg10["net_ETH"].rolling(ROLLING_BINS).std()


def fine_warn(r, s_sig=0.6, e_sig=0.6):
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


agg10["warn"] = agg10.apply(fine_warn, axis=1)
warnings_df = agg10[agg10["warn"] != ""]

# =============================================================
# ETH PRICE DATA
# =============================================================
start_d = flows.index.min().strftime("%Y-%m-%d")
end_d = (flows.index.max() + timedelta(days=1)).strftime("%Y-%m-%d")
price = yf.download("ETH-USD", interval="5m", start=start_d, end=end_d, progress=False)

# TIMEZONE ALIGNMENT
toronto_tz = pytz.timezone("America/Toronto")
# Convert all indices to Toronto timezone
flows.index = flows.index.tz_convert(toronto_tz)
agg10.index = agg10.index.tz_convert(toronto_tz)

# Handle price data timezone and alignment
if isinstance(price, pd.DataFrame) and not price.empty:
    if price.index.tz is None:
        price.index = price.index.tz_localize("UTC")
    price.index = price.index.tz_convert(toronto_tz)
    price = price.loc[flows.index.min() : flows.index.max()]
else:
    price = pd.DataFrame(index=flows.index, columns=["Close"])
    price["Close"] = np.nan

# =============================================================
# PLOTTING
# =============================================================
fig, ax1 = plt.subplots(figsize=(14, 6))

# Hourly stablecoin net
ax1.plot(
    flows.index, flows["stablecoin_net"] / 1e6, label="Stablecoin net (USDT+USDC) [M$]"
)
ax1.set_ylabel("Stablecoin net flow (Million USD)")

# Hourly ETH net
ax2 = ax1.twinx()
ax2.plot(
    flows.index,
    flows["eth_usd"] / 1e6,
    label="ETH net [M$]",
    linestyle="-.",
    color="green",
)
ax2.set_ylabel("ETH net flow (Million USD)")

# ETH price
ax3 = ax1.twinx()
ax3.spines["right"].set_position(("outward", 60))
ax3.plot(price.index, price["Close"], color="red", linewidth=1.0, label="ETH Price")
ax3.set_ylabel("ETH Price (USD)")

# Mark pump/dump events
for _, ev in events_df.iterrows():
    color = "green" if ev["type"].startswith("拉盘") else "red"
    ax1.axvline(ev["time"], color=color, linestyle="--", alpha=0.6)

# Hourly dump‑risk predictions (purple triangles)
flag_times = flows.index[flows["dump_risk"]]
flag_prices = price["Close"].reindex(flag_times, method="ffill")
ax3.scatter(
    flag_times,
    flag_prices,
    marker="v",
    s=70,
    color="purple",
    label=f"Dump‑risk ({WINDOW_HOURS}h)",
)

# Fine‑grained 10‑min warnings (blue up‑arrow & orange X)
price_series = price["Close"]
for ts, row in warnings_df.iterrows():
    # Use last known price at or before ts
    if price_series.empty or ts < price_series.index[0]:
        continue
    y_price = price_series.reindex([ts], method="ffill").iloc[0]
    if isinstance(y_price, pd.Series):
        y_price = y_price.iloc[0]
    if pd.isna(y_price) or (isinstance(y_price, pd.Series) and y_price.empty):
        continue
    if row["warn"] == "Pump_warn":
        ax3.scatter(
            ts,
            y_price,
            marker="^",
            s=80,
            color="blue",
            label=(
                "Pump_warn"
                if "Pump_warn" not in ax3.get_legend_handles_labels()[1]
                else ""
            ),
        )
    elif row["warn"] == "Dump_warn":
        ax3.scatter(
            ts,
            y_price,
            marker="x",
            s=80,
            color="orange",
            label=(
                "Dump_warn"
                if "Dump_warn" not in ax3.get_legend_handles_labels()[1]
                else ""
            ),
        )

# -------------------------------------------------------------
ax1.set_title("Binance net flows with multi‑layer pump/dump alerts (hourly & 10‑min)")
ax1.legend(loc="upper left")
ax2.legend(loc="upper right")
ax3.legend(loc="lower right")
plt.tight_layout()
plt.show()
