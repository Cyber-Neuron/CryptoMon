import json
import threading
import time

import websocket

# 维护最近盘口快照，便于与成交tick对比
last_orderbook = {"bids": [], "asks": [], "time": None}  # [价格, 数量]
last_trade_id = None


def on_orderbook(ws, message):
    data = json.loads(message)
    last_orderbook["bids"] = [(float(p), float(q)) for p, q in data["b"][:5]]
    last_orderbook["asks"] = [(float(p), float(q)) for p, q in data["a"][:5]]
    last_orderbook["time"] = time.time()


def on_trade(ws, message):
    global last_trade_id
    data = json.loads(message)
    price = float(data["p"])
    qty = float(data["q"])
    is_sell = data["m"]  # True=主动卖单（吃bid），False=主动买单（吃ask）
    trade_id = data["t"]
    if qty < 5:
        return
    # 跳过重复
    if last_trade_id is not None and trade_id == last_trade_id:
        return
    last_trade_id = trade_id

    # 获取最近盘口
    bids = last_orderbook.get("bids", [])
    asks = last_orderbook.get("asks", [])

    # 找出tick成交发生在哪一档
    best_bid, bid_qty = bids[0] if bids else (None, None)
    best_ask, ask_qty = asks[0] if asks else (None, None)

    direction = "主动卖出（taker卖）" if is_sell else "主动买入（taker买）"
    remark = "（主动吃bid，价格向下）" if is_sell else "（主动吃ask，价格向上）"

    print("\n====== [Tick成交] ======")
    print(f"价格: {price}\t数量: {qty:.4f}\t方向: {direction}{remark}")
    print(f"盘口买1: {best_bid} {bid_qty} | 卖1: {best_ask} {ask_qty}")

    # 猜测多空归因
    # --- 这里只能判断主动买/主动卖，不能断定“开多/开空/平多/平空”
    # 可以输出行业经验公式，明确说明推断条件
    if price == best_ask:
        print("→ 该成交为主动买单吃掉卖一，买方更积极")
        guess = "主力多方主动进场（可能是开多或平空）"
    elif price == best_bid:
        print("→ 该成交为主动卖单吃掉买一，卖方更积极")
        guess = "主力空方主动进场（可能是开空或平多）"
    else:
        print("→ 该成交在盘口中间价位")
        guess = "中性/套利/非主力行为"
    # print(f"【仅凭盘口与成交，无法断定是开仓还是平仓！此归因仅供参考】")
    print(f"强信号猜测：{guess}")


def ws_thread(url, on_message):
    ws = websocket.WebSocketApp(url, on_message=on_message)
    ws.run_forever()


if __name__ == "__main__":
    threading.Thread(
        target=ws_thread,
        args=("wss://fstream.binance.com/ws/ethusdt@depth5@100ms", on_orderbook),
        daemon=True,
    ).start()
    ws_thread("wss://fstream.binance.com/ws/ethusdt@trade", on_trade)
