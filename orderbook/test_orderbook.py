import asyncio
import json
import time
from datetime import datetime

import aiohttp


async def test_orderbook_api():
    """测试Order Book API"""
    base_url = "http://localhost:8000"

    async with aiohttp.ClientSession() as session:
        # 测试状态
        print("=== 测试API状态 ===")
        async with session.get(f"{base_url}/status") as response:
            if response.status == 200:
                status = await response.json()
                print(f"API状态: {json.dumps(status, indent=2, ensure_ascii=False)}")
            else:
                print(f"状态检查失败: {response.status}")

        # 等待一段时间让order book收集数据
        print("\n=== 等待数据收集 ===")
        await asyncio.sleep(10)

        # 获取当前order book
        print("\n=== 获取当前Order Book ===")
        orderbook = None
        async with session.get(f"{base_url}/orderbook") as response:
            if response.status == 200:
                orderbook = await response.json()
                print(f"当前Order Book:")
                print(f"  时间戳: {datetime.fromtimestamp(orderbook['timestamp'])}")
                print(f"  Last Update ID: {orderbook['last_update_id']}")
                print(f"  Bids数量: {len(orderbook['bids'])}")
                print(f"  Asks数量: {len(orderbook['asks'])}")

                # 显示前5个bid和ask
                if orderbook["bids"]:
                    print("  前5个Bids:")
                    sorted_bids = sorted(
                        orderbook["bids"].items(), key=lambda x: x[0], reverse=True
                    )[:5]
                    for price, qty in sorted_bids:
                        print(f"    {price}: {qty}")

                if orderbook["asks"]:
                    print("  前5个Asks:")
                    sorted_asks = sorted(orderbook["asks"].items(), key=lambda x: x[0])[
                        :5
                    ]
                    for price, qty in sorted_asks:
                        print(f"    {price}: {qty}")
            else:
                print(f"获取Order Book失败: {response.status}")
                return

        # 测试查询特定价格的持仓量
        print("\n=== 测试价格查询 ===")
        current_time = int(time.time())

        # 获取一个存在的价格进行测试
        if orderbook and orderbook["bids"]:
            test_price = list(orderbook["bids"].keys())[0]

            # 测试1：不传入时间戳，获取最近档位
            payload = {"price": test_price}
            print(f"测试1：查询价格 {test_price} 的最近档位（不传入时间戳）")

            async with session.post(f"{base_url}/quantity", json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    print(f"查询结果:")
                    print(f"  目标价格: {result['target_price']}")
                    print(f"  实际价格: {result['actual_price']}")
                    print(f"  时间戳: {datetime.fromtimestamp(result['timestamp'])}")
                    print(f"  持仓量: {result['quantity']}")
                    print(f"  差值: {result['difference']}")
                    print(f"  是否最近档位: {result['is_nearest_level']}")
                else:
                    print(f"查询失败: {response.status}")

            # 测试2：传入时间戳，获取历史数据
            payload = {"price": test_price, "timestamp": current_time}
            print(f"\n测试2：查询价格 {test_price} 的历史数据（传入时间戳）")

            async with session.post(f"{base_url}/quantity", json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    print(f"查询结果:")
                    print(f"  目标价格: {result['target_price']}")
                    print(f"  实际价格: {result['actual_price']}")
                    print(f"  时间戳: {datetime.fromtimestamp(result['timestamp'])}")
                    print(f"  持仓量: {result['quantity']}")
                    print(f"  差值: {result['difference']}")
                    print(f"  是否最近档位: {result['is_nearest_level']}")
                else:
                    print(f"查询失败: {response.status}")

        # 测试最近档位API
        print("\n=== 测试最近档位API ===")
        if orderbook and orderbook["bids"]:
            test_price = list(orderbook["bids"].keys())[0]

            async with session.get(
                f"{base_url}/nearest-level/{test_price}"
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    print(f"最近档位查询结果:")
                    print(f"  目标价格: {result['target_price']}")
                    print(f"  最近价格: {result['nearest_price']}")
                    print(f"  价格差值: {result['price_difference']}")
                    print(f"  持仓量: {result['quantity']}")
                    print(f"  时间戳: {datetime.fromtimestamp(result['timestamp'])}")
                else:
                    print(f"最近档位查询失败: {response.status}")


async def test_quantity_difference():
    """测试持仓量差值功能"""
    base_url = "http://localhost:8000"

    async with aiohttp.ClientSession() as session:
        # 等待数据收集
        await asyncio.sleep(5)

        # 获取当前order book
        async with session.get(f"{base_url}/orderbook") as response:
            if response.status != 200:
                print("无法获取order book")
                return

            orderbook = await response.json()

            # 选择一个价格进行测试
            if not orderbook["bids"]:
                print("没有bid数据")
                return

            test_price = list(orderbook["bids"].keys())[0]
            current_time = int(time.time())

            print(f"\n=== 测试价格 {test_price} 的持仓量变化 ===")

            # 查询多个时间点
            for i in range(5):
                timestamp = current_time - i
                payload = {"price": test_price, "timestamp": timestamp}

                async with session.post(
                    f"{base_url}/quantity", json=payload
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        print(
                            f"时间 {datetime.fromtimestamp(timestamp)}: "
                            f"持仓量={result['quantity']:.6f}, "
                            f"差值={result['difference']:.6f}"
                        )
                    else:
                        print(f"查询失败: {response.status}")


if __name__ == "__main__":
    print("开始测试Order Book API...")
    print("请确保主程序正在运行 (python localorderbok.py)")
    print("等待5秒后开始测试...")

    asyncio.run(test_quantity_difference())
