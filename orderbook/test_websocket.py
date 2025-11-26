#!/usr/bin/env python3
"""
WebSocket连接测试脚本
用于测试Binance WebSocket连接是否正常
"""

import asyncio
import json
import logging
import time
from datetime import datetime

import websockets

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# 测试配置
WEBSOCKET_URLS = [
    "wss://fstream.binance.com/ws/ethusdt@aggTrade",
    "wss://fstream.binance.com/ws/ETHUSDT@aggTrade",
    "wss://fstream.binance.com/ws/btcusdt@aggTrade",
    "wss://fstream.binance.com/ws/BTCUSDT@aggTrade",
]


async def test_websocket_url(url: str, test_duration: int = 10):
    """测试单个WebSocket URL"""
    logger.info(f"=== 测试WebSocket连接: {url} ===")

    try:
        logger.info(f"正在连接: {url}")
        start_time = time.time()

        async with websockets.connect(
            url, ping_interval=20, ping_timeout=10
        ) as websocket:
            logger.info(f"✅ 连接成功，耗时: {time.time() - start_time:.2f}秒")

            message_count = 0
            last_message_time = time.time()

            async for message in websocket:
                message_count += 1
                current_time = time.time()

                try:
                    data = json.loads(message)
                    logger.info(
                        f"消息 #{message_count}: 交易对={data.get('s', 'N/A')}, "
                        f"价格={data.get('p', 'N/A')}, 数量={data.get('q', 'N/A')}"
                    )
                except json.JSONDecodeError:
                    logger.warning(
                        f"消息 #{message_count}: JSON解析失败 - {message[:100]}..."
                    )

                last_message_time = current_time

                # 如果超过测试时间或收到足够消息，停止测试
                if current_time - start_time > test_duration or message_count >= 10:
                    break

                # 如果超过5秒没有消息，可能连接有问题
                if current_time - last_message_time > 5:
                    logger.warning("5秒内未收到新消息")
                    break

            logger.info(f"测试完成: 共收到 {message_count} 条消息")
            return message_count > 0

    except websockets.exceptions.InvalidURI as e:
        logger.error(f"❌ URI无效: {e}")
        return False
    except websockets.exceptions.ConnectionClosed as e:
        logger.error(f"❌ 连接关闭: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ 连接失败: {e}")
        logger.error(f"错误类型: {type(e).__name__}")
        return False


async def test_all_urls():
    """测试所有WebSocket URL"""
    logger.info("=== WebSocket连接测试 ===")
    logger.info(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 50)

    results = {}

    for url in WEBSOCKET_URLS:
        success = await test_websocket_url(url, test_duration=10)
        results[url] = success
        logger.info(f"结果: {'✅ 成功' if success else '❌ 失败'}")
        logger.info("-" * 40)

        # 等待一下再测试下一个
        await asyncio.sleep(2)

    # 总结结果
    logger.info("=== 测试结果总结 ===")
    success_count = sum(results.values())
    total_count = len(results)

    for url, success in results.items():
        status = "✅ 成功" if success else "❌ 失败"
        logger.info(f"{url}: {status}")

    logger.info(
        f"成功率: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)"
    )

    if success_count > 0:
        logger.info("🎉 至少有一个连接成功，WebSocket服务正常")
    else:
        logger.error("❌ 所有连接都失败，请检查网络连接")


async def test_simple_connection():
    """简单的连接测试"""
    logger.info("=== 简单连接测试 ===")

    url = "wss://fstream.binance.com/ws/ethusdt@aggTrade"

    try:
        logger.info(f"尝试连接: {url}")
        async with websockets.connect(url) as websocket:
            logger.info("✅ 连接成功")

            # 等待一条消息
            logger.info("等待接收消息...")
            message = await asyncio.wait_for(websocket.recv(), timeout=10.0)
            logger.info(f"✅ 收到消息: {message[:100]}...")

            return True

    except asyncio.TimeoutError:
        logger.error("❌ 10秒内未收到消息")
        return False
    except Exception as e:
        logger.error(f"❌ 连接失败: {e}")
        return False


if __name__ == "__main__":
    try:
        # 先进行简单测试
        logger.info("开始简单连接测试...")
        if asyncio.run(test_simple_connection()):
            logger.info("简单测试成功，开始完整测试...")
            asyncio.run(test_all_urls())
        else:
            logger.error("简单测试失败，可能网络有问题")
    except KeyboardInterrupt:
        print("\n测试被中断")
    except Exception as e:
        print(f"测试异常: {e}")
