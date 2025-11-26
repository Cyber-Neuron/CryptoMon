#!/usr/bin/env python3
"""
Open Interest WebSocket 测试脚本
用于测试币安 Open Interest API 是否正常工作
"""

import json
import logging
import time

import websocket

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def on_message(ws, message):
    """处理接收到的消息"""
    logger.info(f"收到消息: {message}")
    try:
        data = json.loads(message)
        logger.info(f"解析后数据: {json.dumps(data, indent=2, ensure_ascii=False)}")

        # 检查是否有 openInterest 字段
        if "openInterest" in data:
            logger.info(f"✅ 找到 openInterest 字段: {data['openInterest']}")
        elif "o" in data:
            logger.info(f"✅ 找到 'o' 字段 (可能是 openInterest): {data['o']}")
        else:
            logger.warning(f"❌ 消息中没有 openInterest 或 'o' 字段")
            logger.info(f"可用字段: {list(data.keys())}")

    except json.JSONDecodeError as e:
        logger.error(f"JSON 解析失败: {e}")


def on_error(ws, error):
    """处理错误"""
    logger.error(f"WebSocket 错误: {error}")


def on_close(ws, close_status_code, close_msg):
    """处理连接关闭"""
    logger.warning(
        f"WebSocket 连接关闭 - 状态码: {close_status_code}, 消息: {close_msg}"
    )


def on_open(ws):
    """处理连接打开"""
    logger.info("✅ WebSocket 连接已建立")


def test_oi_websocket():
    """测试 Open Interest WebSocket"""
    logger.info("开始测试 Open Interest WebSocket...")

    # 测试不同的 URL
    urls = [
        "wss://fstream.binance.com/ws/ethusdt@openInterest",
        "wss://fstream.binance.com/ws/ethusdt@openInterest@1s",
        "wss://fstream.binance.com/ws/ethusdt@openInterest@1m",
    ]

    for i, url in enumerate(urls, 1):
        logger.info(f"\n=== 测试 URL {i}: {url} ===")

        try:
            ws = websocket.WebSocketApp(
                url,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close,
                on_open=on_open,
            )

            # 运行 10 秒
            logger.info(f"连接 {url}，运行 10 秒...")
            start_time = time.time()

            # 在单独的线程中运行 WebSocket
            import threading

            def run_ws():
                ws.run_forever()

            ws_thread = threading.Thread(target=run_ws, daemon=True)
            ws_thread.start()

            # 等待 10 秒
            while time.time() - start_time < 10:
                time.sleep(0.1)

            # 关闭连接
            ws.close()

        except Exception as e:
            logger.error(f"连接 {url} 失败: {e}")

        time.sleep(2)  # 等待 2 秒再测试下一个


def test_rest_api():
    """测试 REST API 作为备选方案"""
    logger.info("\n=== 测试 REST API ===")
    try:
        import requests

        # 测试 REST API
        url = "https://fapi.binance.com/fapi/v1/openInterest"
        params = {"symbol": "ETHUSDT"}

        logger.info(f"请求 REST API: {url}")
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            logger.info(
                f"✅ REST API 响应: {json.dumps(data, indent=2, ensure_ascii=False)}"
            )
        else:
            logger.error(f"❌ REST API 错误: {response.status_code} - {response.text}")

    except ImportError:
        logger.warning("requests 库未安装，跳过 REST API 测试")
    except Exception as e:
        logger.error(f"REST API 测试失败: {e}")


if __name__ == "__main__":
    logger.info("=== Open Interest API 测试开始 ===")

    # 测试 WebSocket
    test_oi_websocket()

    # 测试 REST API
    test_rest_api()

    logger.info("=== 测试完成 ===")
