#!/usr/bin/env python3
"""
最近档位功能演示脚本
展示如何使用新的最近档位查询功能
"""

import asyncio
import json
import time
from datetime import datetime

import aiohttp


async def demo_nearest_level():
    """演示最近档位功能"""
    base_url = "http://localhost:8000"

    print("=== 最近档位功能演示 ===")
    print("这个演示展示了如何查询离目标价格最近的一档价格和数量")
    print()

    async with aiohttp.ClientSession() as session:
        # 等待系统启动
        print("等待系统启动...")
        await asyncio.sleep(3)

        # 获取当前order book
        async with session.get(f"{base_url}/orderbook") as response:
            if response.status != 200:
                print("无法获取order book，请确保系统正在运行")
                return

            orderbook = await response.json()

            if not orderbook["bids"]:
                print("没有bid数据，请等待系统收集数据")
                return

            # 获取一些测试价格
            bids = list(orderbook["bids"].keys())
            asks = list(orderbook["asks"].keys())

            # 转换为浮点数
            bids_float = [float(price) for price in bids]
            asks_float = [float(price) for price in asks]

            print(f"当前Order Book状态:")
            print(f"  Bids数量: {len(bids)}")
            print(f"  Asks数量: {len(asks)}")
            print(f"  最高Bid: {max(bids_float)}")
            print(f"  最低Ask: {min(asks_float)}")
            print()

            # 演示1：查询存在的价格
            print("=== 演示1：查询存在的价格 ===")
            test_price = bids_float[0]  # 使用第一个bid价格

            # 使用quantity API（不传入时间戳）
            payload = {"price": test_price}
            async with session.post(f"{base_url}/quantity", json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    print(f"查询价格 {test_price}:")
                    print(f"  目标价格: {result['target_price']}")
                    print(f"  实际价格: {result['actual_price']}")
                    print(f"  持仓量: {result['quantity']}")
                    print(f"  是否最近档位: {result['is_nearest_level']}")
                    print()

            # 使用nearest-level API
            async with session.get(
                f"{base_url}/nearest-level/{test_price}"
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    print(f"最近档位API查询价格 {test_price}:")
                    print(f"  目标价格: {result['target_price']}")
                    print(f"  最近价格: {result['nearest_price']}")
                    print(f"  价格差值: {result['price_difference']}")
                    print(f"  持仓量: {result['quantity']}")
                    print()

            # 演示2：查询不存在的价格
            print("=== 演示2：查询不存在的价格 ===")
            # 计算一个不存在的价格（在两个bid之间）
            if len(bids_float) >= 2:
                non_existent_price = (bids_float[0] + bids_float[1]) / 2
            else:
                non_existent_price = bids_float[0] + 1

            print(f"查询不存在的价格 {non_existent_price}:")

            # 使用quantity API
            payload = {"price": non_existent_price}
            async with session.post(f"{base_url}/quantity", json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    print(f"  Quantity API结果:")
                    print(f"    目标价格: {result['target_price']}")
                    print(f"    实际价格: {result['actual_price']}")
                    print(f"    持仓量: {result['quantity']}")
                    print(f"    是否最近档位: {result['is_nearest_level']}")

            # 使用nearest-level API
            async with session.get(
                f"{base_url}/nearest-level/{non_existent_price}"
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    print(f"  Nearest-level API结果:")
                    print(f"    目标价格: {result['target_price']}")
                    print(f"    最近价格: {result['nearest_price']}")
                    print(f"    价格差值: {result['price_difference']}")
                    print(f"    持仓量: {result['quantity']}")
                    print()

            # 演示3：查询多个不同价格
            print("=== 演示3：查询多个不同价格 ===")
            test_prices = [
                bids_float[0],  # 最高bid
                min(asks_float),  # 最低ask
                (bids_float[0] + min(asks_float)) / 2,  # 中间价格
                bids_float[0] - 100,  # 低于最高bid
                min(asks_float) + 100,  # 高于最低ask
            ]

            for price in test_prices:
                async with session.get(f"{base_url}/nearest-level/{price}") as response:
                    if response.status == 200:
                        result = await response.json()
                        print(f"价格 {price}:")
                        print(f"  最近价格: {result['nearest_price']}")
                        print(f"  价格差值: {result['price_difference']}")
                        print(f"  持仓量: {result['quantity']}")
                        print()

            # 演示4：实时监控最近档位变化
            print("=== 演示4：实时监控最近档位变化（10秒） ===")
            monitor_price = bids_float[0]
            print(f"监控价格 {monitor_price} 的最近档位变化:")

            for i in range(10):
                await asyncio.sleep(1)
                async with session.get(
                    f"{base_url}/nearest-level/{monitor_price}"
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        print(
                            f"  {datetime.now().strftime('%H:%M:%S')} - "
                            f"最近价格: {result['nearest_price']}, "
                            f"持仓量: {result['quantity']:.6f}"
                        )

            print()
            print("=== 演示完成 ===")
            print("功能说明:")
            print("1. 当查询的价格不存在时，系统会返回离该价格最近的一档")
            print("2. 系统会在bids和asks中寻找距离最小的价格")
            print("3. 返回的价格差值表示最近档位与目标价格的距离")
            print("4. 这个功能对于寻找最佳交易价格很有用")


if __name__ == "__main__":
    print("最近档位功能演示")
    print("请确保Order Book系统正在运行 (python localorderbok.py)")
    print()

    asyncio.run(demo_nearest_level())
