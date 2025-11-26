#!/usr/bin/env python3
"""
测试信号处理修复
验证在异步环境中信号处理是否正常工作
"""

import asyncio
import signal
import sys
import time

# 全局关闭事件
shutdown_event = asyncio.Event()


async def test_async_signal():
    """测试异步环境中的信号处理"""
    print("=== 异步信号处理测试 ===")
    print("这个测试模拟主程序的环境")
    print("按 Ctrl+C 来测试是否能正常退出")
    print()

    # 在异步环境中处理信号
    def signal_handler():
        print("\n收到关闭信号，正在退出...")
        shutdown_event.set()

    # 使用asyncio来处理信号
    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGINT, signal_handler)
    loop.add_signal_handler(signal.SIGTERM, signal_handler)

    # 模拟长时间运行的任务
    async def long_running_task():
        i = 0
        while not shutdown_event.is_set():
            print(f"任务运行中... {i}")
            try:
                await asyncio.wait_for(asyncio.sleep(1), timeout=1.0)
            except asyncio.TimeoutError:
                pass
            i += 1
        print("任务收到关闭信号，正在清理...")
        await asyncio.sleep(0.5)  # 模拟清理工作
        print("清理完成")

    try:
        await long_running_task()
    except Exception as e:
        print(f"任务异常: {e}")

    print("测试完成")


if __name__ == "__main__":
    print("开始异步信号处理测试...")
    print("按 Ctrl+C 来测试退出功能")
    print()

    try:
        asyncio.run(test_async_signal())
    except KeyboardInterrupt:
        print("\n测试完成：异步信号处理正常工作")
    except Exception as e:
        print(f"测试失败: {e}")
        sys.exit(1)
