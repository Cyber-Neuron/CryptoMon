import json
import logging
import os
import threading
import time
from collections import deque
from datetime import datetime

import bson
import requests
import websocket
from alert import TradingAlert
from colorama import Fore, Style, init

# 初始化 colorama
init(autoreset=True)

# 创建日志文件夹
os.makedirs("spot", exist_ok=True)
os.makedirs("futures", exist_ok=True)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# 只保留最近5秒的大单，便于匹配
spot_big_trades = deque(maxlen=100)
futures_big_trades = deque(maxlen=100)

# Open Interest 和 Order Book 缓存
oi_cache = []
orderbook_cache = {}
oi_lock = threading.Lock()
orderbook_lock = threading.Lock()

OI_WINDOW = 4  # OI对比窗口，秒
OI_UPDATE_INTERVAL = 2  # 每秒更新一次OI

SPOT_THRESHOLD = 5  # 现货大单阈值
FUTURES_THRESHOLD = 20  # 合约大单阈值
MATCH_INTERVAL = 4  # 匹配窗口，单位：秒
warning_alert = TradingAlert()


def ts2str(ts):
    # 毫秒转本地时间字符串
    return datetime.fromtimestamp(ts / 1000).strftime("%H:%M:%S.%f")[:-3]


def log_trade_to_file(trade_data, folder, timestamp):
    """将交易数据写入BSON文件"""
    filename = f"{folder}/{datetime.now().strftime('%Y%m%d')}.bson"
    try:
        # 添加接收时间戳
        trade_data["received_at"] = timestamp
        with open(filename, "ab") as f:  # 'ab' for append binary
            f.write(bson.dumps(trade_data))
    except Exception as e:
        logger.error(f"写入{trade_data}到{filename}失败: {e}")


def fetch_open_interest(symbol="ETHUSDT"):
    """从REST API获取Open Interest"""
    try:
        url = "https://fapi.binance.com/fapi/v1/openInterest"
        response = requests.get(url, params={"symbol": symbol}, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return float(data.get("openInterest", 0))
        else:
            logger.warning(f"[OI REST] API请求失败: {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"[OI REST] 获取OI失败: {e}")
        return None


def monitor_oi():
    """监控Open Interest的线程"""
    logger.debug("启动OI监控线程")
    while True:
        oi = fetch_open_interest()
        if oi is not None:
            ts = time.time()
            with oi_lock:
                oi_cache.append((ts, oi))
                # 只保留最近60秒
                oi_cache[:] = [x for x in oi_cache if ts - x[0] < 60]
            logger.debug(f"[OI] 更新持仓量: {oi:.2f}, 缓存长度: {len(oi_cache)}")
        time.sleep(OI_UPDATE_INTERVAL)


def on_orderbook(ws, message):
    """处理Order Book数据"""
    try:
        data = json.loads(message)
        with orderbook_lock:
            orderbook_cache["bids"] = [(float(p), float(q)) for p, q in data["b"][:5]]
            orderbook_cache["asks"] = [(float(p), float(q)) for p, q in data["a"][:5]]
        logger.debug(
            f"[OrderBook] 更新盘口 - 买一: {orderbook_cache['bids'][0] if orderbook_cache['bids'] else 'None'}, 卖一: {orderbook_cache['asks'][0] if orderbook_cache['asks'] else 'None'}"
        )
    except Exception as e:
        logger.error(f"[OrderBook] 处理消息失败: {e}")


def determine_position_action_improved(is_buyer_maker, ts):
    """改进的持仓动作判断逻辑"""
    with oi_lock:
        # 查找最近OI变动
        oi_before = [oi for t, oi in oi_cache if t <= ts - OI_WINDOW]
        oi_after = [oi for t, oi in oi_cache if abs(t - ts) <= OI_WINDOW]

    if oi_before and oi_after:
        delta_oi = oi_after[-1] - oi_before[-1]
        logger.debug(
            f"[OI分析] 时间窗口: {OI_WINDOW}秒, OI变化: {oi_before[-1]:.2f} → {oi_after[-1]:.2f} ({delta_oi:+.2f})"
        )

        # 经验判断逻辑
        if is_buyer_maker and delta_oi > 0:  # 主动卖出 + OI增加
            return "开空", delta_oi
        elif not is_buyer_maker and delta_oi > 0:  # 主动买入 + OI增加
            return "开多", delta_oi
        elif delta_oi < 0:  # OI减少
            if is_buyer_maker:
                return "平多", delta_oi
            else:
                return "平空", delta_oi
        else:  # OI无变化
            return "无明显判断", delta_oi
    else:
        logger.debug(f"[OI分析] 无法获取OI数据 - 缓存长度: {len(oi_cache)}")
        return "未知", None


def match_trades():
    logger.debug(f"启动匹配线程，匹配间隔: {MATCH_INTERVAL}秒")
    last_status_time = time.time()

    while True:
        now = time.time()

        # 每10秒显示一次状态
        if now - last_status_time >= 10:
            logger.debug(
                f"匹配状态 - 现货队列: {len(spot_big_trades)} 笔, 合约队列: {len(futures_big_trades)} 笔"
            )
            with oi_lock:
                logger.debug(f"OI缓存长度: {len(oi_cache)}")
            last_status_time = now

        # 遍历两边队列，寻找匹配
        match_count = 0
        matched_spots = set()
        matched_futures = set()

        # 统计同步大单的操作分布
        sync_operations = {"开多": 0, "开空": 0, "平多": 0, "平空": 0, "未知": 0}

        # 记录最后一次匹配的时间间隔
        last_dt = 0.0

        # 统计价格信息
        spot_prices = []
        futures_prices = []
        total_spot_qty = 0
        total_futures_qty = 0

        logger.debug(
            f"开始匹配检查 - 现货队列: {len(spot_big_trades)}, 合约队列: {len(futures_big_trades)}"
        )

        for s in list(spot_big_trades):
            for f in list(futures_big_trades):
                dt = abs(s["ts"] / 1000 - f["ts"] / 1000)
                logger.debug(
                    f"检查匹配: 现货时间={ts2str(s['ts'])}, 合约时间={ts2str(f['ts'])}, 时间差={dt:.3f}秒"
                )

                if dt <= MATCH_INTERVAL:
                    match_count += 1
                    last_dt = dt  # 记录最后一次匹配的时间间隔
                    logger.debug(f"发现匹配 #{match_count}: 时间差={dt:.3f}秒")
                    print(
                        Fore.YELLOW + Style.BRIGHT + f"\n=== [检测到疑似同步大单] ==="
                    )
                    print(
                        Fore.YELLOW
                        + f"[现货] {ts2str(s['ts'])} qty={s['qty']:.2f} price={s['price']} {'卖单' if s['isBuyerMaker'] else '买单'}"
                    )
                    print(
                        Fore.YELLOW
                        + f"[合约] {ts2str(f['ts'])} qty={f['qty']:.2f} price={f['price']} {f.get('positionAction', '未知')}"
                    )
                    print(Fore.YELLOW + f"时间间隔: {dt:.3f}秒" + Style.RESET_ALL)

                    # 统计操作类型
                    position_action = f.get("positionAction", "未知")
                    if "开多" in position_action:
                        sync_operations["开多"] += 1
                    elif "开空" in position_action:
                        sync_operations["开空"] += 1
                    elif "平多" in position_action:
                        sync_operations["平多"] += 1
                    elif "平空" in position_action:
                        sync_operations["平空"] += 1
                    else:
                        sync_operations["未知"] += 1

                    # 收集价格和数量信息
                    spot_prices.append(s["price"])
                    futures_prices.append(f["price"])
                    total_spot_qty += s["qty"]
                    total_futures_qty += f["qty"]

                    matched_spots.add(s["ts"])
                    matched_futures.add(f["ts"])

        # 匹配后移除已匹配的交易
        if matched_spots:
            # 分析操作分布并发出语音告警
            total_matches = sum(sync_operations.values())
            if total_matches > 0:
                # 找出占优势的操作
                dominant_operation = max(sync_operations.items(), key=lambda x: x[1])
                operation_name, operation_count = dominant_operation

                # 计算占比
                percentage = (operation_count / total_matches) * 100

                # 计算平均价格
                avg_spot_price = (
                    sum(spot_prices) / len(spot_prices) if spot_prices else 0
                )
                avg_futures_price = (
                    sum(futures_prices) / len(futures_prices) if futures_prices else 0
                )
                price_diff = avg_futures_price - avg_spot_price
                price_diff_percent = (
                    (price_diff / avg_spot_price * 100) if avg_spot_price > 0 else 0
                )

                # 生成统计信息
                stats_text = f"同步大单统计: 总计{total_matches}笔"
                for op, count in sync_operations.items():
                    if count > 0:
                        stats_text += f", {op}{count}笔"

                print(Fore.CYAN + f"\n📊 {stats_text}")
                print(
                    Fore.CYAN
                    + f"🎯 主要操作: {operation_name} ({percentage:.1f}%)"
                    + Style.RESET_ALL
                )

                # 显示价格统计
                print(Fore.GREEN + f"💰 价格统计:")
                print(Fore.GREEN + f"   现货平均价格: ${avg_spot_price:.2f}")
                print(Fore.GREEN + f"   合约平均价格: ${avg_futures_price:.2f}")
                print(
                    Fore.GREEN
                    + f"   价差: ${price_diff:+.2f} ({price_diff_percent:+.2f}%)"
                )
                print(Fore.GREEN + f"   现货总量: {total_spot_qty:.2f} ETH")
                print(
                    Fore.GREEN
                    + f"   合约总量: {total_futures_qty:.2f} ETH"
                    + Style.RESET_ALL
                )

                # 根据主要操作发出不同的语音告警
                if operation_name == "开多":
                    warning_alert.trading_alert("开多", f"{total_matches}笔", "ETH")
                elif operation_name == "开空":
                    warning_alert.trading_alert("开空", f"{total_matches}笔", "ETH")
                elif operation_name == "平多":
                    warning_alert.trading_alert("平多", f"{total_matches}笔", "ETH")
                elif operation_name == "平空":
                    warning_alert.trading_alert("平空", f"{total_matches}笔", "ETH")
                else:
                    # 如果主要是未知操作，发出一般性告警
                    warning_alert.custom_alert(
                        f"发现{total_matches}笔同步大单，操作类型未知"
                    )

                # 额外发出详细统计的语音提醒
                if total_matches >= 3:  # 如果同步大单较多，发出详细统计
                    detail_text = f"同步大单详情: {operation_name}占{percentage:.0f}%，共{total_matches}笔"
                    warning_alert.custom_alert(detail_text)

                # 播报价格信息
                price_alert_text = (
                    f"现货均价{avg_spot_price:.0f}，合约均价{avg_futures_price:.0f}"
                )
                if abs(price_diff_percent) > 0.5:  # 如果价差超过0.5%，播报价差
                    if price_diff > 0:
                        price_alert_text += f"，合约溢价{price_diff_percent:.1f}%"
                    else:
                        price_alert_text += f"，现货溢价{abs(price_diff_percent):.1f}%"
                warning_alert.custom_alert(price_alert_text)

            # warning_alert.custom_alert(
            #     f"发现疑似同步大单，现货时间间隔: {last_dt:.3f}秒"
            # )
            spot_big_trades_copy = list(spot_big_trades)
            removed_spots = 0
            for trade in spot_big_trades_copy:
                if trade["ts"] in matched_spots:
                    spot_big_trades.remove(trade)
                    removed_spots += 1
            logger.debug(f"移除已匹配的现货交易: {removed_spots} 笔")

        if matched_futures:
            futures_big_trades_copy = list(futures_big_trades)
            removed_futures = 0
            for trade in futures_big_trades_copy:
                if trade["ts"] in matched_futures:
                    futures_big_trades.remove(trade)
                    removed_futures += 1
            logger.debug(f"移除已匹配的合约交易: {removed_futures} 笔")

        if match_count > 0:
            logger.debug(f"本轮检测到 {match_count} 个匹配")
        time.sleep(0.5)


def spot_trade_ws():
    logger.debug("正在连接现货WebSocket...")
    url = "wss://stream.binance.com:9443/ws/ethusdt@trade"
    ws = websocket.WebSocketApp(
        url,
        on_message=on_spot_message,
        on_error=lambda ws, err: logger.error(f"[现货错误] {err}"),
        on_close=lambda ws, close_status_code, close_msg: logger.warning(
            f"[现货关闭] 状态码: {close_status_code}, 消息: {close_msg}"
        ),
        on_open=lambda ws: logger.info(
            "[现货] WebSocket连接已建立，开始接收交易数据..."
        ),
    )
    ws.run_forever()


def futures_trade_ws():
    logger.debug("正在连接合约WebSocket...")
    url = "wss://fstream.binance.com/ws/ethusdt@trade"
    ws = websocket.WebSocketApp(
        url,
        on_message=on_futures_message,
        on_error=lambda ws, err: logger.error(f"[合约错误] {err}"),
        on_close=lambda ws, close_status_code, close_msg: logger.warning(
            f"[合约关闭] 状态码: {close_status_code}, 消息: {close_msg}"
        ),
        on_open=lambda ws: logger.info(
            "[合约] WebSocket连接已建立，开始接收交易数据..."
        ),
    )
    ws.run_forever()


def orderbook_ws():
    """Order Book WebSocket连接"""
    logger.debug("正在连接Order Book WebSocket...")
    url = "wss://fstream.binance.com/ws/ethusdt@depth5@100ms"
    ws = websocket.WebSocketApp(
        url,
        on_message=on_orderbook,
        on_error=lambda ws, err: logger.error(f"[OrderBook错误] {err}"),
        on_close=lambda ws, close_status_code, close_msg: logger.warning(
            f"[OrderBook关闭] 状态码: {close_status_code}, 消息: {close_msg}"
        ),
        on_open=lambda ws: logger.info(
            "[OrderBook] WebSocket连接已建立，开始接收盘口数据..."
        ),
    )
    ws.run_forever()


def on_spot_message(ws, message):
    data = json.loads(message)
    qty = float(data["q"])
    price = float(data["p"])
    timestamp = data["T"]
    is_buyer_maker = data["m"]  # True为卖单（主动买单成交）
    action = "卖单" if is_buyer_maker else "买单"
    action_color = Fore.RED if is_buyer_maker else Fore.GREEN
    # print(f"收到现货交易: {data}")

    logger.debug(
        f"[现货] 收到交易: 数量={qty:.4f}, 价格=${price:.2f}, 主动方={'卖方' if is_buyer_maker else '买方'}"
    )

    # 记录所有交易（但只显示大单）
    if qty >= SPOT_THRESHOLD:
        trade = {
            "ts": timestamp,  # 毫秒时间戳
            "qty": qty,
            "price": price,
            "isBuyerMaker": is_buyer_maker,
        }
        spot_big_trades.append(trade)
        logger.debug(f"[现货] 添加大单到队列，当前队列长度: {len(spot_big_trades)}")
        print(
            Fore.BLUE
            + f"[现货大单] {ts2str(timestamp)} 数量: {qty:.2f} ETH, 价格: ${price:.2f} "
            + action_color
            + f"{action}"
            + Style.RESET_ALL
        )
    else:
        # 每100笔小单显示一次，避免日志过多
        if len(spot_big_trades) % 100 == 0:
            logger.debug(
                f"[现货] 收到交易 - 数量: {qty:.2f} ETH, 价格: ${price:.2f} ({action})"
            )

    # 记录所有原始数据到文件
    log_trade_to_file(data, "spot", time.time())


def on_futures_message(ws, message):
    data = json.loads(message)
    qty = float(data["q"])
    price = float(data["p"])
    timestamp = data["T"]
    is_buyer_maker = data["m"]  # true = 主动卖出，false = 主动买入

    logger.debug(
        f"[合约] 收到交易: 数量={qty:.4f}, 价格=${price:.2f}, 主动方={'卖方' if is_buyer_maker else '买方'}"
    )

    # 使用改进的持仓动作判断逻辑
    ts = time.time()
    position_action, delta_oi = determine_position_action_improved(is_buyer_maker, ts)

    logger.debug(
        f"[合约] 持仓动作分析: m={is_buyer_maker}, 判断结果={position_action}, OI变化={delta_oi}"
    )

    # 根据持仓动作确定颜色
    if "开多" in position_action or "平空" in position_action:
        action_color = Fore.GREEN  # 买入相关操作
    elif "开空" in position_action or "平多" in position_action:
        action_color = Fore.RED  # 卖出相关操作
    else:
        action_color = Fore.YELLOW  # 无明显判断
    if "买" not in position_action and "卖" not in position_action:
        position_action += " 卖方" if is_buyer_maker else " 买方"

    # 记录所有交易（但只显示大单）
    if qty >= FUTURES_THRESHOLD:
        trade = {
            "ts": timestamp,  # 毫秒时间戳
            "qty": qty,
            "price": price,
            "isBuyerMaker": is_buyer_maker,
            "positionAction": position_action,
            "deltaOI": delta_oi,
        }
        futures_big_trades.append(trade)
        logger.debug(f"[合约] 添加大单到队列，当前队列长度: {len(futures_big_trades)}")
        print(
            Fore.MAGENTA
            + f"[合约大单] {ts2str(timestamp)} 数量: {qty:.2f} ETH, 价格: ${price:.2f}, "
            + action_color
            + f"{position_action}"
            + Style.RESET_ALL
        )
        if delta_oi is not None:
            print(f"    OI变化: {delta_oi:+.2f}")
        else:
            print(f"    OI变化: 无法获取")

        # 显示当前盘口信息
        with orderbook_lock:
            bids = orderbook_cache.get("bids", [])
            asks = orderbook_cache.get("asks", [])
        if bids and asks:
            print(f"    盘口: 买一{bids[0]}, 卖一{asks[0]}")
    else:
        # 每100笔小单显示一次，避免日志过多
        if len(futures_big_trades) % 100 == 0:
            logger.debug(
                f"[合约] 收到交易 - 数量: {qty:.2f} ETH, 价格: ${price:.2f}, {position_action} (小单)"
            )

    # 记录所有原始数据到文件
    log_trade_to_file(data, "futures", time.time())


if __name__ == "__main__":
    logger.info("=== 币安大单监控程序启动 ===")
    logger.info(f"现货大单阈值: {SPOT_THRESHOLD} ETH")
    logger.info(f"合约大单阈值: {FUTURES_THRESHOLD} ETH")
    logger.info(f"匹配时间窗口: {MATCH_INTERVAL} 秒")
    logger.info(f"OI对比窗口: {OI_WINDOW} 秒")
    logger.info(f"OI更新间隔: {OI_UPDATE_INTERVAL} 秒")
    logger.info("=" * 40)

    # 启动四个线程
    threading.Thread(target=spot_trade_ws, daemon=True).start()
    threading.Thread(target=futures_trade_ws, daemon=True).start()
    threading.Thread(target=orderbook_ws, daemon=True).start()  # 启动Order Book线程
    threading.Thread(target=monitor_oi, daemon=True).start()  # 启动OI监控线程

    # 启动大单匹配线程
    match_trades()
