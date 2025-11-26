#!/usr/bin/env python3
"""
期货交易数据分析程序
获取期货交易数据，分析交易前后的order book变化
"""

import asyncio
import json
import logging
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Union

import aiohttp
import websockets
from colorama import Fore, Style, init

# 导入配置
try:
    from trade_analyzer_config import *
except ImportError:
    # 默认配置
    LOCAL_API_BASE_URL = "http://localhost:8000"
    WEBSOCKET_URL = "wss://fstream.binance.com/ws/ethusdt@aggTrade"
    SYMBOL = "ETHUSDT"
    MIN_QUANTITY_THRESHOLD = 1.0
    ANALYSIS_WINDOW_SECONDS = 5
    PRICE_TOLERANCE = 0.1
    BUFFER_SIZE = 100
    ANALYSIS_INTERVAL = 1.0
    STATS_INTERVAL = 10
    LOG_LEVEL = "DEBUG"
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    LOG_DATE_FORMAT = "%H:%M:%S"
    RECONNECT_DELAY = 5
    CONNECTION_TIMEOUT = 30
    API_TIMEOUT = 5
    MAX_RETRIES = 3
    ENABLE_COLORS = True
    SHOW_DETAILED_ANALYSIS = True
    SHOW_STATISTICS = True

# 初始化 colorama
if ENABLE_COLORS:
    init(autoreset=True)

# 配置日志
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
    datefmt=LOG_DATE_FORMAT,
)
logger = logging.getLogger(__name__)

# 统计信息
total_trades = 0
analyzed_trades = 0
api_calls = 0
errors = 0


def ts2str(ts):
    """毫秒时间戳转本地时间字符串"""
    return datetime.fromtimestamp(ts / 1000).strftime("%H:%M:%S.%f")[:-3]


class TradeAnalyzer:
    """交易分析器"""

    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self.trade_buffer: List[Dict] = []
        self.last_analysis_time = 0

    async def init_session(self):
        """初始化HTTP会话"""
        if self.session is None:
            self.session = aiohttp.ClientSession()

    async def close_session(self):
        """关闭HTTP会话"""
        if self.session:
            await self.session.close()
            self.session = None

    async def get_orderbook_at_time(
        self, price: float, timestamp: int
    ) -> Optional[Dict]:
        """获取指定时间点的order book数据"""
        global api_calls

        try:
            await self.init_session()

            # 确保session不为None
            if self.session is None:
                logger.error("HTTP会话初始化失败")
                return None

            # 调用本地API获取order book数据
            payload = {"price": price, "timestamp": timestamp}

            async with self.session.post(
                f"{LOCAL_API_BASE_URL}/quantity",
                json=payload,
                timeout=aiohttp.ClientTimeout(total=API_TIMEOUT),
            ) as response:
                api_calls += 1

                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    logger.warning(f"API调用失败: {response.status}")
                    return None

        except Exception as e:
            logger.error(f"获取order book数据失败: {e}")
            return None

    async def analyze_trade(self, trade_data: Dict):
        """分析单笔交易"""
        global analyzed_trades, errors

        try:
            # 解析交易数据
            event_time = trade_data["E"]  # 事件时间
            trade_time = trade_data["T"]  # 交易时间
            price = float(trade_data["p"])
            quantity = float(trade_data["q"])
            is_buyer_maker = trade_data["m"]

            # 检查交易数量是否达到阈值
            if quantity < MIN_QUANTITY_THRESHOLD:
                return

            # 转换为秒级时间戳
            event_time_sec = event_time // 1000
            trade_time_sec = trade_time // 1000

            logger.info(
                f"分析交易: 价格=${price:.2f}, 数量={quantity:.4f}, "
                f"事件时间={ts2str(event_time)}, 交易时间={ts2str(trade_time)}"
            )

            # 获取交易前的order book数据
            before_data = await self.get_orderbook_at_time(price, trade_time_sec - 1)

            # 获取交易后的order book数据
            after_data = await self.get_orderbook_at_time(price, trade_time_sec + 1)

            if before_data and after_data:
                if SHOW_DETAILED_ANALYSIS:
                    await self.print_analysis_result(
                        trade_data, before_data, after_data
                    )
                analyzed_trades += 1
            else:
                logger.warning("无法获取完整的order book数据")
                errors += 1

        except Exception as e:
            logger.error(f"分析交易失败: {e}")
            errors += 1

    async def print_analysis_result(
        self, trade_data: Dict, before_data: Dict, after_data: Dict
    ):
        """打印分析结果"""
        price = float(trade_data["p"])
        quantity = float(trade_data["q"])
        is_buyer_maker = trade_data["m"]
        event_time = trade_data["E"]
        trade_time = trade_data["T"]

        # 计算变化
        before_qty = before_data.get("quantity", 0)
        after_qty = after_data.get("quantity", 0)
        qty_change = after_qty - before_qty

        before_price = before_data.get("actual_price", price)
        after_price = after_data.get("actual_price", price)

        # 确定交易类型和颜色
        if is_buyer_maker:
            trade_type = "主动卖出"
            color = Fore.RED
        else:
            trade_type = "主动买入"
            color = Fore.GREEN

        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}交易分析结果")
        print(f"{Fore.CYAN}{'='*60}")

        print(f"{color}交易信息:")
        print(f"  时间: {ts2str(event_time)} (事件) / {ts2str(trade_time)} (交易)")
        print(f"  价格: ${price:.2f}")
        print(f"  数量: {quantity:.4f} {SYMBOL}")
        print(f"  类型: {trade_type}")

        print(f"\n{Fore.YELLOW}Order Book变化:")
        print(f"  交易前: 价格=${before_price:.2f}, 挂单量={before_qty:.6f}")
        print(f"  交易后: 价格=${after_price:.2f}, 挂单量={after_qty:.6f}")
        print(f"  变化量: {qty_change:+.6f}")

        # 分析挂单变化
        if abs(qty_change) > 0.001:  # 忽略微小变化
            if qty_change > 0:
                print(f"  {Fore.GREEN}挂单增加: 可能有新订单进入")
            else:
                print(f"  {Fore.RED}挂单减少: 订单被消耗")
        else:
            print(f"  {Fore.YELLOW}挂单无明显变化")

        # 价格变化分析
        price_change = after_price - before_price
        if abs(price_change) > price * PRICE_TOLERANCE / 100:
            print(f"  {Fore.MAGENTA}价格变化: {price_change:+.4f}")

        print(f"{Fore.CYAN}{'='*60}\n")

    async def process_trade_message(self, message: Union[str, bytes]):
        """处理交易消息"""
        global total_trades

        try:
            # 确保消息是字符串类型
            if isinstance(message, bytes):
                message = message.decode("utf-8")

            logger.debug(f"收到原始消息: {message[:200]}...")  # 只显示前200个字符

            data = json.loads(message)
            total_trades += 1

            logger.debug(
                f"解析交易数据: 价格={data.get('p', 'N/A')}, "
                f"数量={data.get('q', 'N/A')}, "
                f"事件时间={data.get('E', 'N/A')}, "
                f"交易时间={data.get('T', 'N/A')}, "
                f"交易对={data.get('s', 'N/A')}"
            )

            # 添加到缓冲区
            self.trade_buffer.append(data)

            # 限制缓冲区大小
            if len(self.trade_buffer) > BUFFER_SIZE:
                self.trade_buffer = self.trade_buffer[-BUFFER_SIZE:]

            logger.debug(f"缓冲区大小: {len(self.trade_buffer)}")

            # 定期分析缓冲区中的交易
            current_time = time.time()
            if current_time - self.last_analysis_time >= ANALYSIS_INTERVAL:
                logger.debug(f"开始分析缓冲区中的 {len(self.trade_buffer)} 笔交易")
                await self.analyze_buffer()
                self.last_analysis_time = current_time

        except json.JSONDecodeError as e:
            logger.error(f"JSON解析失败: {e}, 消息内容: {message[:100]}...")
        except Exception as e:
            logger.error(f"处理交易消息失败: {e}")
            logger.error(f"消息内容: {message[:100]}...")

    async def analyze_buffer(self):
        """分析缓冲区中的交易"""
        if not self.trade_buffer:
            return

        # 分析最近的交易
        recent_trades = self.trade_buffer[-10:]  # 分析最近10笔交易

        for trade in recent_trades:
            await self.analyze_trade(trade)

        # 清空缓冲区
        self.trade_buffer.clear()

    async def print_statistics(self):
        """打印统计信息"""
        while True:
            await asyncio.sleep(STATS_INTERVAL)
            if SHOW_STATISTICS:
                print(f"\n{Fore.BLUE}统计信息:")
                print(f"  总交易数: {total_trades}")
                print(f"  已分析交易: {analyzed_trades}")
                print(f"  API调用次数: {api_calls}")
                print(f"  错误次数: {errors}")
                print(f"  缓冲区大小: {len(self.trade_buffer)}")
                print(f"{Fore.BLUE}{'='*40}")


async def websocket_handler():
    """WebSocket连接处理"""
    analyzer = TradeAnalyzer()
    stats_task = None

    try:
        # 启动统计信息打印任务
        if SHOW_STATISTICS:
            stats_task = asyncio.create_task(analyzer.print_statistics())

        while True:
            try:
                logger.info(f"正在连接到WebSocket: {WEBSOCKET_URL}")
                logger.debug(f"WebSocket连接参数: ping_interval=20, ping_timeout=10")

                async with websockets.connect(
                    WEBSOCKET_URL, ping_interval=20, ping_timeout=10
                ) as websocket:
                    logger.info("✅ WebSocket连接已建立，开始接收交易数据...")
                    logger.debug(f"WebSocket连接状态: {websocket.state}")

                    message_count = 0
                    async for message in websocket:
                        message_count += 1
                        logger.debug(f"收到第 {message_count} 条消息")

                        await analyzer.process_trade_message(message)

                        # 每100条消息输出一次状态
                        if message_count % 100 == 0:
                            logger.info(f"已接收 {message_count} 条消息")

            except websockets.exceptions.ConnectionClosed as e:
                logger.warning(f"WebSocket连接断开: {e}")
                logger.warning("尝试重连...")
                await asyncio.sleep(RECONNECT_DELAY)
            except websockets.exceptions.InvalidURI as e:
                logger.error(f"WebSocket URI无效: {e}")
                logger.error(f"当前URI: {WEBSOCKET_URL}")
                await asyncio.sleep(RECONNECT_DELAY)
            except Exception as e:
                logger.error(f"WebSocket错误: {e}")
                logger.error(f"错误类型: {type(e).__name__}")
                await asyncio.sleep(RECONNECT_DELAY)

    except KeyboardInterrupt:
        logger.info("收到中断信号，正在关闭...")
    finally:
        await analyzer.close_session()
        if stats_task:
            stats_task.cancel()


async def test_websocket_connection():
    """测试WebSocket连接"""
    logger.info("=== 测试WebSocket连接 ===")

    try:
        logger.info(f"测试连接: {WEBSOCKET_URL}")

        async with websockets.connect(
            WEBSOCKET_URL, ping_interval=20, ping_timeout=10
        ) as websocket:
            logger.info("✅ WebSocket连接测试成功")

            # 等待几秒钟看是否能收到消息
            logger.info("等待接收消息...")
            message_count = 0
            start_time = time.time()

            async for message in websocket:
                message_count += 1
                logger.info(f"收到消息 #{message_count}: {message[:100]}...")

                if message_count >= 5:  # 只接收5条消息作为测试
                    break

                if time.time() - start_time > 10:  # 最多等待10秒
                    logger.warning("10秒内未收到足够消息，可能连接有问题")
                    break

            logger.info(f"测试完成，共收到 {message_count} 条消息")
            return message_count > 0

    except Exception as e:
        logger.error(f"WebSocket连接测试失败: {e}")
        return False


async def test_local_api():
    """测试本地API连接"""
    logger.info("测试本地API连接...")

    try:
        async with aiohttp.ClientSession() as session:
            # 测试状态接口
            async with session.get(
                f"{LOCAL_API_BASE_URL}/status",
                timeout=aiohttp.ClientTimeout(total=API_TIMEOUT),
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"本地API连接成功: {data}")
                    return True
                else:
                    logger.error(f"本地API状态检查失败: {response.status}")
                    return False
    except Exception as e:
        logger.error(f"本地API连接测试失败: {e}")
        return False


async def main():
    """主函数"""
    logger.info("=== 期货交易数据分析程序启动 ===")
    logger.info(f"本地API地址: {LOCAL_API_BASE_URL}")
    logger.info(f"WebSocket地址: {WEBSOCKET_URL}")
    logger.info(f"交易对: {SYMBOL}")
    logger.info(f"最小交易数量阈值: {MIN_QUANTITY_THRESHOLD}")
    logger.info(f"分析时间窗口: {ANALYSIS_WINDOW_SECONDS}秒")
    logger.info(f"缓冲区大小: {BUFFER_SIZE}")
    logger.info(f"分析间隔: {ANALYSIS_INTERVAL}秒")
    logger.info(f"日志级别: {LOG_LEVEL}")
    logger.info("=" * 50)

    # 测试本地API连接
    if not await test_local_api():
        logger.error("本地API连接失败，请确保localorderbok.py正在运行")
        return

    # 测试WebSocket连接
    logger.info("开始测试WebSocket连接...")
    if not await test_websocket_connection():
        logger.error("WebSocket连接测试失败，请检查网络连接和WebSocket地址")
        logger.error("可能的原因:")
        logger.error("1. 网络连接问题")
        logger.error("2. WebSocket地址错误")
        logger.error("3. Binance API服务不可用")
        logger.error("4. 防火墙阻止连接")
        return

    logger.info("所有测试通过，开始正式运行...")

    # 启动WebSocket处理
    await websocket_handler()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}程序已退出")
    except Exception as e:
        print(f"\n{Fore.RED}程序异常退出: {e}")
