import websocket
import threading
import json
import numpy as np
import matplotlib.pyplot as plt
import time

book_matrix = []
price_axis = None
base_price = None

def on_orderbook(ws, message):
    global base_price, price_axis
    data = json.loads(message)
    # 取前20档bids和前20档asks
    bids = sorted([(float(p), float(q)) for p, q in data['b']], reverse=True)[:20]
    asks = sorted([(float(p), float(q)) for p, q in data['a']])[:20]
    # 合并为从低到高的price list和quantity list
    full_book = bids[::-1] + asks
    prices = [p for p, q in full_book]
    qtys = [q for p, q in full_book]
    if not price_axis:
        price_axis = prices
        base_price = np.mean(prices)
    book_matrix.append(qtys)
    # 只保留最新300帧（可调，决定横坐标时间长度）
    if len(book_matrix) > 300:
        book_matrix.pop(0)

def ws_thread():
    ws = websocket.WebSocketApp(
        "wss://fstream.binance.com/ws/ethusdt@depth40@100ms", on_message=on_orderbook)
    ws.run_forever()

def plot_loop():
    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 5))
    while True:
        if len(book_matrix) < 10:  # 采样太少不画
            time.sleep(0.5)
            continue
        mat = np.array(book_matrix).T  # 转成价位 x 时间
        ax.clear()
        im = ax.imshow(
            np.log1p(mat),  # log变换，高挂单更显著
            aspect='auto',
            cmap='hot',
            origin='lower'
        )
        plt.colorbar(im, ax=ax, label="log(挂单数量+1)")
        # Y轴标价（只标头尾）
        ax.set_yticks([0, len(price_axis)//2, len(price_axis)-1])
        ax.set_yticklabels([
            f"{price_axis[0]:.2f}",
            f"{price_axis[len(price_axis)//2]:.2f}",
            f"{price_axis[-1]:.2f}"
        ])
        ax.set_xlabel("时间")
        ax.set_ylabel("价格档位")
        ax.set_title("ETHUSDT 盘口热力图（Binance 合约）")
        plt.pause(1)
    plt.ioff()

if __name__ == "__main__":
    threading.Thread(target=ws_thread, daemon=True).start()
    plot_loop()

