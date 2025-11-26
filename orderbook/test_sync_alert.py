#!/usr/bin/env python3
"""
测试同步大单统计和语音告警功能
"""

import time

from alert import TradingAlert


def test_sync_operations():
    """测试同步大单操作统计功能"""
    alert = TradingAlert()

    print("🎯 测试同步大单统计和语音告警功能")
    print("=" * 50)

    # 模拟不同的同步大单场景
    test_scenarios = [
        {
            "name": "开多占优势",
            "operations": {"开多": 3, "开空": 1, "平多": 0, "平空": 0, "未知": 0},
            "spot_prices": [2450.50, 2451.20, 2452.10, 2450.80],
            "futures_prices": [2450.75, 2451.50, 2452.30, 2451.00],
            "spot_qty": [15.5, 12.3, 18.7, 14.2],
            "futures_qty": [20.0, 16.8, 22.5, 18.9],
        },
        {
            "name": "开空占优势",
            "operations": {"开多": 1, "开空": 4, "平多": 1, "平空": 0, "未知": 0},
            "spot_prices": [2448.30, 2447.80, 2446.90, 2447.20, 2448.10, 2447.50],
            "futures_prices": [2448.60, 2448.10, 2447.20, 2447.50, 2448.40, 2447.80],
            "spot_qty": [13.2, 16.8, 19.5, 14.7, 17.3, 15.9],
            "futures_qty": [18.5, 22.1, 25.8, 20.2, 23.7, 21.4],
        },
        {
            "name": "大量同步大单",
            "operations": {"开多": 5, "开空": 3, "平多": 2, "平空": 1, "未知": 0},
            "spot_prices": [
                2455.20,
                2454.80,
                2455.50,
                2454.30,
                2455.90,
                2454.60,
                2455.10,
                2454.90,
                2455.30,
                2454.70,
                2455.40,
            ],
            "futures_prices": [
                2455.60,
                2455.20,
                2455.90,
                2454.70,
                2456.30,
                2455.00,
                2455.50,
                2455.30,
                2455.70,
                2455.10,
                2455.80,
            ],
            "spot_qty": [
                20.5,
                18.7,
                22.3,
                16.9,
                24.1,
                19.8,
                21.4,
                17.6,
                23.2,
                18.3,
                20.9,
            ],
            "futures_qty": [
                26.8,
                24.2,
                28.7,
                22.1,
                30.5,
                25.9,
                27.3,
                23.1,
                29.6,
                24.7,
                27.1,
            ],
        },
    ]

    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n📊 测试场景 {i}: {scenario['name']}")
        print(f"操作分布: {scenario['operations']}")

        # 计算统计信息
        total_matches = sum(scenario["operations"].values())
        dominant_operation = max(scenario["operations"].items(), key=lambda x: x[1])
        operation_name, operation_count = dominant_operation
        percentage = (operation_count / total_matches) * 100

        # 计算价格统计
        spot_prices = scenario["spot_prices"]
        futures_prices = scenario["futures_prices"]
        spot_qty = scenario["spot_qty"]
        futures_qty = scenario["futures_qty"]

        avg_spot_price = sum(spot_prices) / len(spot_prices)
        avg_futures_price = sum(futures_prices) / len(futures_prices)
        price_diff = avg_futures_price - avg_spot_price
        price_diff_percent = price_diff / avg_spot_price * 100
        total_spot_qty = sum(spot_qty)
        total_futures_qty = sum(futures_qty)

        # 生成统计信息
        stats_text = f"同步大单统计: 总计{total_matches}笔"
        for op, count in scenario["operations"].items():
            if count > 0:
                stats_text += f", {op}{count}笔"

        print(f"📊 {stats_text}")
        print(f"🎯 主要操作: {operation_name} ({percentage:.1f}%)")

        # 显示价格统计
        print(f"💰 价格统计:")
        print(f"   现货平均价格: ${avg_spot_price:.2f}")
        print(f"   合约平均价格: ${avg_futures_price:.2f}")
        print(f"   价差: ${price_diff:+.2f} ({price_diff_percent:+.2f}%)")
        print(f"   现货总量: {total_spot_qty:.2f} ETH")
        print(f"   合约总量: {total_futures_qty:.2f} ETH")

        # 模拟语音告警
        print("🔔 发出语音告警...")

        # 根据主要操作发出不同的语音告警
        if operation_name == "开多":
            alert.trading_alert("开多", f"{total_matches}笔同步", "ETH")
        elif operation_name == "开空":
            alert.trading_alert("开空", f"{total_matches}笔同步", "ETH")
        elif operation_name == "平多":
            alert.trading_alert("平多", f"{total_matches}笔同步", "ETH")
        elif operation_name == "平空":
            alert.trading_alert("平空", f"{total_matches}笔同步", "ETH")
        else:
            alert.custom_alert(f"发现{total_matches}笔同步大单，操作类型未知")

        # 额外发出详细统计的语音提醒
        if total_matches >= 3:
            detail_text = f"同步大单详情: {operation_name}占{percentage:.0f}%，共{total_matches}笔"
            alert.custom_alert(detail_text)

        # 播报价格信息
        price_alert_text = (
            f"现货均价{avg_spot_price:.0f}，合约均价{avg_futures_price:.0f}"
        )
        if abs(price_diff_percent) > 0.5:  # 如果价差超过0.5%，播报价差
            if price_diff > 0:
                price_alert_text += f"，合约溢价{price_diff_percent:.1f}%"
            else:
                price_alert_text += f"，现货溢价{abs(price_diff_percent):.1f}%"
        alert.custom_alert(price_alert_text)

        time.sleep(3)  # 等待语音播放完成

    print("\n✅ 测试完成！")


if __name__ == "__main__":
    test_sync_operations()
