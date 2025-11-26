#!/usr/bin/env python3
"""
期货交易分析程序测试脚本
"""

import asyncio
import json
import time
from datetime import datetime

import aiohttp


async def test_local_api():
    """测试本地API连接"""
    print("=== 测试本地API连接 ===")

    try:
        async with aiohttp.ClientSession() as session:
            # 测试状态接口
            async with session.get("http://localhost:8000/status") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ 本地API连接成功: {data}")
                    return True
                else:
                    print(f"❌ 本地API状态检查失败: {response.status}")
                    return False
    except Exception as e:
        print(f"❌ 本地API连接测试失败: {e}")
        return False


async def test_quantity_api():
    """测试quantity API"""
    print("\n=== 测试Quantity API ===")

    try:
        async with aiohttp.ClientSession() as session:
            # 测试当前时间查询
            payload = {"price": 50000.0}
            async with session.post(
                "http://localhost:8000/quantity", json=payload
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ 当前时间查询成功: {data}")
                else:
                    print(f"❌ 当前时间查询失败: {response.status}")
                    return False

            # 测试历史时间查询
            current_time = int(time.time())
            payload = {"price": 50000.0, "timestamp": current_time - 10}
            async with session.post(
                "http://localhost:8000/quantity", json=payload
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ 历史时间查询成功: {data}")
                else:
                    print(f"❌ 历史时间查询失败: {response.status}")
                    return False

            return True
    except Exception as e:
        print(f"❌ Quantity API测试失败: {e}")
        return False


async def test_nearest_level_api():
    """测试最近档位API"""
    print("\n=== 测试最近档位API ===")

    try:
        async with aiohttp.ClientSession() as session:
            # 测试最近档位查询
            async with session.get(
                "http://localhost:8000/nearest-level/50000.0"
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ 最近档位查询成功: {data}")
                    return True
                else:
                    print(f"❌ 最近档位查询失败: {response.status}")
                    return False
    except Exception as e:
        print(f"❌ 最近档位API测试失败: {e}")
        return False


async def test_orderbook_api():
    """测试Order Book API"""
    print("\n=== 测试Order Book API ===")

    try:
        async with aiohttp.ClientSession() as session:
            # 测试Order Book查询
            async with session.get("http://localhost:8000/orderbook") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Order Book查询成功")
                    print(f"  Bids数量: {len(data.get('bids', {}))}")
                    print(f"  Asks数量: {len(data.get('asks', {}))}")
                    print(f"  最后更新ID: {data.get('last_update_id', 'N/A')}")
                    return True
                else:
                    print(f"❌ Order Book查询失败: {response.status}")
                    return False
    except Exception as e:
        print(f"❌ Order Book API测试失败: {e}")
        return False


def simulate_trade_data():
    """模拟交易数据"""
    current_time = int(time.time() * 1000)  # 毫秒时间戳

    return {
        "e": "aggTrade",
        "E": current_time,  # 事件时间
        "s": "ETHUSDT",
        "a": 12345,
        "p": "50000.00",
        "q": "1.5",
        "f": 100,
        "l": 105,
        "T": current_time - 3,  # 交易时间（稍早于事件时间）
        "m": False,  # 主动买入
    }


async def test_trade_analysis():
    """测试交易分析功能"""
    print("\n=== 测试交易分析功能 ===")

    # 模拟交易数据
    trade_data = simulate_trade_data()
    print(f"模拟交易数据: {json.dumps(trade_data, indent=2)}")

    try:
        async with aiohttp.ClientSession() as session:
            price = float(trade_data["p"])
            trade_time = trade_data["T"] // 1000  # 转换为秒

            # 获取交易前的数据
            payload = {"price": price, "timestamp": trade_time - 1}
            async with session.post(
                "http://localhost:8000/quantity", json=payload
            ) as response:
                if response.status == 200:
                    before_data = await response.json()
                    print(f"✅ 交易前数据获取成功: {before_data}")
                else:
                    print(f"❌ 交易前数据获取失败: {response.status}")
                    return False

            # 获取交易后的数据
            payload = {"price": price, "timestamp": trade_time + 1}
            async with session.post(
                "http://localhost:8000/quantity", json=payload
            ) as response:
                if response.status == 200:
                    after_data = await response.json()
                    print(f"✅ 交易后数据获取成功: {after_data}")
                else:
                    print(f"❌ 交易后数据获取失败: {response.status}")
                    return False

            # 分析变化
            before_qty = before_data.get("quantity", 0)
            after_qty = after_data.get("quantity", 0)
            qty_change = after_qty - before_qty

            print(f"\n📊 分析结果:")
            print(f"  交易前挂单量: {before_qty:.6f}")
            print(f"  交易后挂单量: {after_qty:.6f}")
            print(f"  变化量: {qty_change:+.6f}")

            if abs(qty_change) > 0.001:
                if qty_change > 0:
                    print("  📈 挂单增加: 可能有新订单进入")
                else:
                    print("  📉 挂单减少: 订单被消耗")
            else:
                print("  ➡️ 挂单无明显变化")

            return True
    except Exception as e:
        print(f"❌ 交易分析测试失败: {e}")
        return False


async def main():
    """主测试函数"""
    print("=== 期货交易分析程序测试 ===")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    # 测试本地API连接
    if not await test_local_api():
        print("\n❌ 本地API连接失败，请确保localorderbok.py正在运行")
        return

    # 测试各个API接口
    tests = [
        ("Quantity API", test_quantity_api),
        ("最近档位API", test_nearest_level_api),
        ("Order Book API", test_orderbook_api),
        ("交易分析功能", test_trade_analysis),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        try:
            if await test_func():
                passed += 1
                print(f"✅ {test_name} 测试通过")
            else:
                print(f"❌ {test_name} 测试失败")
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")

    print(f"\n=== 测试结果 ===")
    print(f"通过: {passed}/{total}")
    print(f"成功率: {passed/total*100:.1f}%")

    if passed == total:
        print("🎉 所有测试通过！程序可以正常运行。")
    else:
        print("⚠️ 部分测试失败，请检查配置和依赖。")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n测试被中断")
    except Exception as e:
        print(f"测试异常: {e}")
