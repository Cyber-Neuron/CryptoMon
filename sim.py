import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def eth_hedge_sim(
    spot_eth=2.0,
    short_eth=1.0,
    price_series=None,
    funding_rate=0.0001,  # 资金费/8h（0.01%/8h）
    hours_per_step=8,
    plot=True,
):
    """
    ETH现货 + 币本位永续空单组合策略全路径模拟
    """
    # 默认一周，±10%随机波动牛市
    if price_series is None:
        np.random.seed(42)
        steps = 21
        base = 3700
        price_series = base * np.cumprod(1 + np.random.normal(0.001, 0.012, steps))

    price_series = np.array(price_series)
    n = len(price_series)
    steps = np.arange(n)

    # Directional (spot+short) P&L, Funding
    net_eth = spot_eth - short_eth
    price_pnl = net_eth * (price_series - price_series[0])
    funding_income = short_eth * price_series * funding_rate
    funding_cum = np.cumsum(funding_income)

    # 资产曲线
    equity = (
        spot_eth * price_series
        - short_eth * (price_series - price_series[0])
        + funding_cum
    )

    # 最大回撤
    dd = equity - np.maximum.accumulate(equity)
    mdd = np.min(dd)
    drawdown_pct = mdd / np.maximum.accumulate(equity).max()

    # 汇总
    result = pd.DataFrame(
        {
            "Price": price_series,
            "PricePnL": price_pnl,
            "FundingPnL": funding_cum,
            "TotalEquity": equity,
            "Drawdown": dd,
            "NetDelta": net_eth,
        }
    )

    summary = {
        "StartPrice": price_series[0],
        "EndPrice": price_series[-1],
        "TotalFunding": funding_cum[-1],
        "TotalPricePnL": price_pnl[-1],
        "FinalEquity": equity[-1],
        "MaxDrawdownUSD": mdd,
        "MaxDrawdownPct": drawdown_pct,
        "SpotETH": spot_eth,
        "ShortETH": short_eth,
        "NetDelta": net_eth,
    }

    if plot:
        plt.figure(figsize=(12, 5))
        plt.subplot(211)
        plt.plot(steps, price_series, label="ETH Price")
        plt.ylabel("ETH Price (USD)")
        plt.legend()
        plt.subplot(212)
        plt.plot(steps, equity, label="Total Equity")
        plt.plot(steps, funding_cum, label="Funding (Cumulative)")
        plt.plot(steps, price_pnl, label="Directional P&L")
        plt.xlabel("Step (8h)")
        plt.ylabel("Equity / P&L (USD)")
        plt.legend()
        plt.tight_layout()
        plt.show()

    return result, summary


# 示例运行
res, summ = eth_hedge_sim(
    spot_eth=2.0,
    short_eth=1.0,
    funding_rate=0.0001,
)
print(pd.DataFrame([summ]))
