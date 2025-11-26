# filename: option_pnl_analysis.py
import json
import fire
from collections import defaultdict
from typing import Dict, List

CONTRACT_MULTIPLIER = 1   # 一份合约对应的标的数量

def _load_series(data: Dict[str, list], key: str) -> List[float]:
    "读取 JSON 中可能缺失的字段，若不存在返回全 0 数组"
    return [float(x) for x in data.get(key, [0] * len(data["keyList"]))]

def intrinsic_payoff(S: float, K: float, call: bool) -> float:
    "单份期权在交割价 S 下的内在价值"
    return max(S - K, 0) if call else max(K - S, 0)

def calc_pnl(data: Dict[str, list], S: float) -> Dict[str, float]:
    strikes = [float(k) for k in data["keyList"]]
    call_oi      = _load_series(data, "callOiList")
    put_oi       = _load_series(data, "putOiList")
    mm_call_oi   = _load_series(data, "callMarketOiList")   # 做市商持仓
    mm_put_oi    = _load_series(data, "putMarketOiList")

    pnl = defaultdict(float)   # long_call, short_call, mm, ...

    for K, C_long, P_long, C_mm, P_mm in zip(
        strikes, call_oi, put_oi, mm_call_oi, mm_put_oi
    ):
        # 单份合约在价格 S 的内在价值
        call_iv = intrinsic_payoff(S, K, call=True)
        put_iv  = intrinsic_payoff(S, K, call=False)

        # ===== 多头 =====
        pnl["long_call"] += C_long * call_iv
        pnl["long_put"]  += P_long * put_iv

        # ===== 空头（市场其他所有卖方）=====
        pnl["short_call"] -= C_long * call_iv
        pnl["short_put"]  -= P_long * put_iv

        # ===== 做市商（假设是卖方仓位）=====
        pnl["mm"]        -= C_mm * call_iv
        pnl["mm"]        -= P_mm * put_iv

    # 乘以合约规模
    for k in pnl:
        pnl[k] *= CONTRACT_MULTIPLIER

    pnl["long_total"]  = pnl["long_call"]  + pnl["long_put"]
    pnl["short_total"] = pnl["short_call"] + pnl["short_put"]

    return pnl

def table(data: Dict[str, list], price_grid: List[float]) -> None:
    "打印价格-PnL 表"
    hdr = "Price  LongPnL  ShortPnL  MM_PnL"
    print(hdr)
    print("-" * len(hdr))
    for S in price_grid:
        pnl = calc_pnl(data, S)
        print(
            f"{S:>5.0f} {pnl['long_total']:>9.0f} {pnl['short_total']:>9.0f} {pnl['mm']:>9.0f}"
        )

def main(json_file: str, spot: float, step: float = 50, width: int = 5):
    """
    参数
    ----
    json_file : 期权 JSON（Binance API 格式）
    spot      : 当前或假设收盘价
    step      : 价格步长
    width     : 往上下各取 width 格价格，绘制价格-PnL 表
    """
    with open(json_file) as f:
        raw = json.load(f)["data"]

    # 1) 计算 max-pain
    strikes = [float(k) for k in raw["keyList"]]
    pains = [
        calc_pnl(raw, S)["short_total"]   # short_total = -long_total = 做市商赔付
        for S in strikes
    ]
    S_mp = strikes[pains.index(min(pains))]

    print(f"\n=== Max-Pain Strike: {S_mp} ===")

    # 2) 在给定 spot 价输出各方 PnL
    pnl_spot = calc_pnl(raw, spot)
    print(f"\n=== PnL @ S={spot} ===")
    print(
        f"Long  : {pnl_spot['long_total']:.0f}\n"
        f"Short : {pnl_spot['short_total']:.0f}\n"
        f"MM    : {pnl_spot['mm']:.0f}"
    )

    # 3) 打印一张附近价格栅格的 PnL 表
    grid = [spot + i * step for i in range(-width, width + 1)]
    print("\n=== Price-PnL Grid ===")
    table(raw, grid)

if __name__ == "__main__":
    fire.Fire(main)

