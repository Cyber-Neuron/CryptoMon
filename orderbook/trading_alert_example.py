#!/usr/bin/env python3
"""
交易监控语音提醒系统示例
集成到你的交易监控程序中
"""

import random
import time
from datetime import datetime

from alert import TradingAlert


class TradingMonitor:
    def __init__(self):
        """初始化交易监控系统"""
        self.alert_system = TradingAlert(lang="zh-cn", slow=False)
        self.is_running = False

    def start_monitoring(self):
        """开始监控"""
        self.is_running = True
        print("🚀 开始交易监控...")

        while self.is_running:
            try:
                # 模拟检测到交易信号
                self.simulate_trading_signals()
                time.sleep(5)  # 每5秒检查一次

            except KeyboardInterrupt:
                print("\n⏹️ 停止监控")
                self.is_running = False
                break
            except Exception as e:
                print(f"监控错误: {e}")
                time.sleep(5)

    def simulate_trading_signals(self):
        """模拟交易信号检测"""
        # 模拟不同的交易场景
        scenarios = [
            # (概率, 交易类型, 金额, 币种)
            (0.1, "大额开空", "500万", "BTC"),
            (0.1, "大额开多", "300万", "ETH"),
            (0.15, "大额平仓", "200万", "BTC"),
            (0.2, "价格突破", "45000", "BTC"),
            (0.1, "异常交易", "1000万", "ETH"),
        ]

        for prob, action, amount, symbol in scenarios:
            if random.random() < prob:
                self.handle_trading_signal(action, amount, symbol)

    def handle_trading_signal(self, action, amount, symbol):
        """处理交易信号"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"\n📊 [{timestamp}] 检测到交易信号: {action} {symbol} {amount}")

        if "开空" in action:
            self.alert_system.trading_alert("开空", amount, symbol, wait_time=1)
        elif "开多" in action:
            self.alert_system.trading_alert("开多", amount, symbol, wait_time=1)
        elif "平仓" in action:
            self.alert_system.trading_alert("平仓", amount, symbol, wait_time=1)
        elif "价格突破" in action:
            self.alert_system.price_alert(symbol, amount, "突破", wait_time=1)
        elif "异常交易" in action:
            self.alert_system.custom_alert(
                f"检测到异常交易，{symbol}，金额{amount}", wait_time=1
            )

    def stop_monitoring(self):
        """停止监控"""
        self.is_running = False


def quick_test():
    """快速测试语音提醒"""
    alert = TradingAlert()

    print("🎤 快速测试语音提醒...")

    # 测试各种提醒
    alerts = [
        ("开空", "100万", "BTC"),
        ("开多", "50万", "ETH"),
        ("平仓", "200万", "BTC"),
        ("价格突破", "45000", "BTC"),
        ("异常交易", "1000万", "ETH"),
    ]

    for action, amount, symbol in alerts:
        print(f"测试: {action} {symbol} {amount}")
        if "开空" in action or "开多" in action or "平仓" in action:
            alert.trading_alert(action, amount, symbol, wait_time=1)
        elif "价格突破" in action:
            alert.price_alert(symbol, amount, "突破", wait_time=1)
        else:
            alert.custom_alert(f"检测到{action}，{symbol}，金额{amount}", wait_time=1)

        time.sleep(1)


def main():
    """主函数"""
    print("🎯 交易监控语音提醒系统")
    print("=" * 40)
    print("1. 快速测试语音提醒")
    print("2. 开始模拟监控")
    print("3. 退出")
    print("=" * 40)

    while True:
        try:
            choice = input("请选择 (1-3): ").strip()

            if choice == "1":
                quick_test()
            elif choice == "2":
                monitor = TradingMonitor()
                monitor.start_monitoring()
            elif choice == "3":
                print("👋 再见！")
                break
            else:
                print("❌ 无效选择，请重新输入")

        except KeyboardInterrupt:
            print("\n👋 再见！")
            break
        except Exception as e:
            print(f"❌ 错误: {e}")


if __name__ == "__main__":
    main()
