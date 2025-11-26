#!/usr/bin/env python3
"""
测试信号处理功能
验证Ctrl+C是否能正常退出程序
"""

import asyncio
import signal
import sys
import time


async def test_shutdown():
    """测试关闭功能"""
    print("=== 信号处理测试 ===")
    print("这个测试会启动一个简单的异步任务")
    print("按 Ctrl+C 来测试是否能正常退出")
    print()

    # 模拟一个长时间运行的任务
    async def long_running_task():
        i = 0
        while True:
            print(f"任务运行中... {i}")
            await asyncio.sleep(1)
            i += 1

    try:
        await long_running_task()
    except KeyboardInterrupt:
        print("\n收到 Ctrl+C 信号，正在退出...")
        # 模拟清理工作
        await asyncio.sleep(0.5)
        print("清理完成，程序退出")


if __name__ == "__main__":
    print("开始信号处理测试...")
    print("按 Ctrl+C 来测试退出功能")
    print()

    try:
        asyncio.run(test_shutdown())
    except KeyboardInterrupt:
        print("\n测试完成：信号处理正常工作")
    except Exception as e:
        print(f"测试失败: {e}")
        sys.exit(1)
