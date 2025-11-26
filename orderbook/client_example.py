#!/usr/bin/env python3
"""
Order Book API客户端示例
演示如何使用REST API查询持仓量差值
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Optional

import aiohttp


class OrderBookClient:
    """Order Book API客户端"""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url

    async def get_status(self):
        """获取系统状态"""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/status") as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"状态查询失败: {response.status}")

    async def get_current_orderbook(self):
        """获取当前order book"""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/orderbook") as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Order book查询失败: {response.status}")

    async def get_quantity_difference(
        self, price: float, timestamp: Optional[int] = None
    ):
        """获取指定价格的持仓量差值"""
        payload = {"price": price}
        if timestamp is not None:
            payload["timestamp"] = timestamp

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/quantity", json=payload
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"持仓量查询失败: {response.status}")

    async def get_nearest_level(self, price: float):
        """获取离指定价格最近的一档"""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}/nearest-level/{price}"
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"最近档位查询失败: {response.status}")

    async def get_history_info(self):
        """获取历史数据信息"""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/history") as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"历史数据查询失败: {response.status}")


async def main():
    """主函数 - 演示API使用"""
    client = OrderBookClient()

    print("=== Order Book API客户端示例 ===")

    try:
        # 1. 检查系统状态
        print("\n1. 检查系统状态...")
        status = await client.get_status()
        print(f"   交易对: {status['symbol']}")
        print(f"   连接状态: {'已连接' if status['is_connected'] else '未连接'}")
        print(f"   最后更新ID: {status['last_update_id']}")
        print(f"   Bids数量: {status['bids_count']}")
        print(f"   Asks数量: {status['asks_count']}")
        print(f"   历史快照: {status['history_count']}")

        if not status["is_connected"]:
            print("   警告: 系统未连接到WebSocket，数据可能不准确")

        # 2. 获取当前order book
        print("\n2. 获取当前Order Book...")
        orderbook = await client.get_current_orderbook()
        print(f"   时间戳: {datetime.fromtimestamp(orderbook['timestamp'])}")
        print(f"   最后更新ID: {orderbook['last_update_id']}")

        # 显示前5个bid和ask
        if orderbook["bids"]:
            print("   前5个Bids:")
            sorted_bids = sorted(
                orderbook["bids"].items(), key=lambda x: x[0], reverse=True
            )[:5]
            for price, qty in sorted_bids:
                print(f"     {price}: {qty}")

        if orderbook["asks"]:
            print("   前5个Asks:")
            sorted_asks = sorted(orderbook["asks"].items(), key=lambda x: x[0])[:5]
            for price, qty in sorted_asks:
                print(f"     {price}: {qty}")

        # 3. 测试持仓量差值查询
        print("\n3. 测试持仓量差值查询...")

        # 选择一个存在的价格进行测试
        if orderbook["bids"]:
            test_price = list(orderbook["bids"].keys())[0]
            current_time = int(time.time())

            print(f"   测试价格: {test_price}")
            print(f"   当前时间: {datetime.fromtimestamp(current_time)}")

            # 测试1：不传入时间戳，获取最近档位
            print(f"   测试1：查询最近档位（不传入时间戳）")
            result = await client.get_quantity_difference(test_price)
            print(f"   结果:")
            print(f"     目标价格: {result['target_price']}")
            print(f"     实际价格: {result['actual_price']}")
            print(f"     持仓量: {result['quantity']:.6f}")
            print(f"     差值: {result['difference']:.6f}")
            print(f"     是否最近档位: {result['is_nearest_level']}")

            # 测试2：传入时间戳，获取历史数据
            print(f"   测试2：查询历史数据（传入时间戳）")
            result = await client.get_quantity_difference(test_price, current_time)
            print(f"   结果:")
            print(f"     目标价格: {result['target_price']}")
            print(f"     实际价格: {result['actual_price']}")
            print(f"     持仓量: {result['quantity']:.6f}")
            print(f"     差值: {result['difference']:.6f}")
            print(f"     是否最近档位: {result['is_nearest_level']}")

        # 4. 测试最近档位API
        print("\n4. 测试最近档位API...")
        if orderbook["bids"]:
            test_price = list(orderbook["bids"].keys())[0]

            # 测试一个不存在的价格
            non_existent_price = test_price + 100
            result = await client.get_nearest_level(non_existent_price)
            print(f"   查询价格 {non_existent_price} 的最近档位:")
            print(f"     目标价格: {result['target_price']}")
            print(f"     最近价格: {result['nearest_price']}")
            print(f"     价格差值: {result['price_difference']}")
            print(f"     持仓量: {result['quantity']:.6f}")

        # 5. 获取历史数据信息
        print("\n5. 获取历史数据信息...")
        history = await client.get_history_info()
        print(f"   历史快照数量: {history['history_count']}")
        if history["time_range"]["start"]:
            print(
                f"   开始时间: {datetime.fromtimestamp(history['time_range']['start'])}"
            )
        if history["time_range"]["end"]:
            print(
                f"   结束时间: {datetime.fromtimestamp(history['time_range']['end'])}"
            )

        # 6. 演示实时监控
        print("\n6. 演示实时监控（5秒）...")
        if orderbook["bids"]:
            test_price = list(orderbook["bids"].keys())[0]

            for i in range(5):
                await asyncio.sleep(1)
                result = await client.get_quantity_difference(test_price)
                print(
                    f"   {datetime.now().strftime('%H:%M:%S')} - "
                    f"价格 {test_price}: 实际价格={result['actual_price']}, "
                    f"持仓量={result['quantity']:.6f}, "
                    f"差值={result['difference']:.6f}"
                )

        print("\n=== 演示完成 ===")

    except Exception as e:
        print(f"错误: {e}")
        print("请确保Order Book系统正在运行 (python localorderbok.py)")


if __name__ == "__main__":
    asyncio.run(main())
