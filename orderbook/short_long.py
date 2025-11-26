import json
import threading
import time

import requests
import websocket

# 全局缓存
trade_buffer = []
oi_last = None
result_buffer = []


def get_open_interest(symbol="ETHUSDT"):
    url = "https://fapi.binance.com/fapi/v1/openInterest"
    return float(requests.get(url, params={"symbol": symbol}).json()["openInterest"])


def on_trade(ws, message):
    data = json.loads(message)
    # 'm': True为卖单主动成交（taker卖/吃bid），False为买单主动成交（taker买/吃ask）
    trade_buffer.append(
        {
            "ts": int(time.time()),  # 秒级时间戳
            "price": float(data["p"]),
            "qty": float(data["q"]),
            "is_sell": data["m"],
        }
    )


def analyze_1s():
    global oi_last
    last_check_ts = int(time.time())
    oi_last = get_open_interest()
    print("启动中，等待1秒聚合...")

    while True:
        now = int(time.time())
        if now == last_check_ts:
            time.sleep(0.05)
            continue
        last_check_ts = now

        sec = now - 1
        # *** 仅统计数量大于50的大单 ***
        trades = [t for t in trade_buffer if t["ts"] == sec and t["qty"] > 5]
        trade_buffer[:] = [t for t in trade_buffer if t["ts"] >= sec]

        taker_buy = sum(t["qty"] for t in trades if not t["is_sell"])
        taker_sell = sum(t["qty"] for t in trades if t["is_sell"])
        total_qty = taker_buy + taker_sell

        oi_new = get_open_interest()
        delta_oi = oi_new - oi_last
        oi_last = oi_new

        # 判定方向
        if delta_oi > 0:
            if taker_buy > taker_sell:
                direction = "开多主导"
            elif taker_sell > taker_buy:
                direction = "开空主导"
            else:
                direction = "中性（多空均衡）"
        elif delta_oi < 0:
            if taker_buy > taker_sell:
                direction = "多方主动平仓"
            elif taker_sell > taker_buy:
                direction = "空方主动平仓"
            else:
                direction = "中性平仓"
        else:
            direction = "OI无变化/中性"
        if taker_buy > 0 or taker_sell > 0:
            result = {
                "time": time.strftime("%H:%M:%S", time.localtime(sec)),
                "大单主动买": taker_buy,
                "大单主动卖": taker_sell,
                "总大单成交量": total_qty,
                "OI变化": delta_oi,
                "判定": direction,
            }
            print(
                f"[{result['time']}] "
                f"主动买: {taker_buy:.2f}, 主动卖: {taker_sell:.2f}, OI变化: {delta_oi:+.2f} => {direction}"
            )


def analyze_1s_small():
    global oi_last
    last_check_ts = int(time.time())
    oi_last = get_open_interest()
    print("启动中，等待1秒聚合...")

    while True:
        now = int(time.time())
        if now == last_check_ts:
            time.sleep(0.05)
            continue
        last_check_ts = now

        # 聚合上一秒的数据
        sec = now - 1
        trades = [t for t in trade_buffer if t["ts"] == sec]
        # 清理缓存，防止溢出
        trade_buffer[:] = [t for t in trade_buffer if t["ts"] >= sec]

        taker_buy = sum(t["qty"] for t in trades if not t["is_sell"])
        taker_sell = sum(t["qty"] for t in trades if t["is_sell"])

        total_qty = taker_buy + taker_sell

        oi_new = get_open_interest()
        if taker_buy < 10 and taker_sell < 10:
            continue
        delta_oi = oi_new - oi_last
        oi_last = oi_new

        # 判定方向
        if delta_oi > 0:
            if taker_buy > taker_sell:
                direction = "开多主导"
            elif taker_sell > taker_buy:
                direction = "开空主导"
            else:
                direction = "中性（多空均衡）"
        elif delta_oi < 0:
            if taker_buy > taker_sell:
                direction = "多方主动平仓"
            elif taker_sell > taker_buy:
                direction = "空方主动平仓"
            else:
                direction = "中性平仓"
        else:
            direction = "OI无变化/中性"

        result = {
            "time": time.strftime("%H:%M:%S", time.localtime(sec)),
            "开多taker量": taker_buy,
            "开空taker量": taker_sell,
            "总成交量": total_qty,
            "OI变化": delta_oi,
            "判定": direction,
        }
        result_buffer.append(result)
        print(
            f"[{result['time']}] "
            f"主动买: {taker_buy:.2f}, 主动卖: {taker_sell:.2f}, OI变化: {delta_oi:+.2f} => {direction}"
        )


def start_ws():
    ws = websocket.WebSocketApp(
        "wss://fstream.binance.com/ws/ethusdt@trade", on_message=on_trade
    )
    ws.run_forever()


if __name__ == "__main__":
    threading.Thread(target=start_ws, daemon=True).start()
    analyze_1s()
