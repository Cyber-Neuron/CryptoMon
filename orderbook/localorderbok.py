import asyncio
import json
import logging
import signal
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

import aiohttp
import uvicorn
import websockets
from config import *
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# 配置日志
logging.basicConfig(level=getattr(logging, LOG_LEVEL), format=LOG_FORMAT)
logger = logging.getLogger(__name__)

# 全局变量用于优雅关闭
shutdown_event = asyncio.Event()


@dataclass
class OrderBookEntry:
    """Order book条目"""

    price: float
    quantity: float
    timestamp: float


@dataclass
class OrderBookSnapshot:
    """Order book快照"""

    last_update_id: int
    bids: Dict[float, float]  # price -> quantity
    asks: Dict[float, float]  # price -> quantity
    timestamp: float


class OrderBookManager:
    """本地Order Book管理器"""

    def __init__(self, symbol: str = SYMBOL):
        self.symbol = symbol
        self.symbol_lower = symbol.lower()
        self.order_book = OrderBookSnapshot(
            last_update_id=0, bids={}, asks={}, timestamp=0
        )
        self.event_buffer = []  # 事件缓冲区
        self.last_event_u = 0  # 上一个事件的u值
        self.is_connected = False
        self.history = []  # 历史快照，用于查询

    async def get_depth_snapshot(self) -> OrderBookSnapshot:
        """获取深度快照"""
        async with aiohttp.ClientSession() as session:
            async with session.get(SNAPSHOT_URL) as response:
                if response.status != 200:
                    raise Exception(f"Failed to get depth snapshot: {response.status}")

                data = await response.json()

                # 解析快照数据
                bids = {float(price): float(qty) for price, qty in data["bids"]}
                asks = {float(price): float(qty) for price, qty in data["asks"]}

                snapshot = OrderBookSnapshot(
                    last_update_id=data["lastUpdateId"],
                    bids=bids,
                    asks=asks,
                    timestamp=time.time(),
                )

                logger.info(
                    f"Got depth snapshot with lastUpdateId: {snapshot.last_update_id}"
                )
                return snapshot

    def process_depth_event(self, event: dict):
        """处理深度事件"""
        u = event["u"]  # 最终更新ID
        U = event["U"]  # 第一个更新ID
        pu = event.get("pu", 0)  # 上一个最终更新ID

        # 检查事件序列
        if self.last_event_u != 0 and pu != self.last_event_u:
            logger.warning(
                f"Event sequence mismatch: pu={pu}, last_u={self.last_event_u}"
            )
            return False

        # 检查事件是否应该被处理
        if u < self.order_book.last_update_id:
            logger.info(
                f"Dropping event with u={u} < lastUpdateId={self.order_book.last_update_id}"
            )
            return True

        # 第一个事件应该满足条件
        if self.last_event_u == 0:
            if not (
                U <= self.order_book.last_update_id
                and u >= self.order_book.last_update_id
            ):
                logger.warning(
                    f"First event condition not met: U={U}, u={u}, lastUpdateId={self.order_book.last_update_id}"
                )
                return False

        # 更新order book
        for price, quantity in event["b"]:  # bids
            price = float(price)
            quantity = float(quantity)
            if quantity == 0:
                self.order_book.bids.pop(price, None)
            else:
                self.order_book.bids[price] = quantity

        for price, quantity in event["a"]:  # asks
            price = float(price)
            quantity = float(quantity)
            if quantity == 0:
                self.order_book.asks.pop(price, None)
            else:
                self.order_book.asks[price] = quantity

        self.order_book.last_update_id = u
        self.order_book.timestamp = time.time()
        self.last_event_u = u

        # 保存历史快照（每秒保存一次）
        current_time = int(time.time())
        if not self.history or current_time > self.history[-1]["timestamp"]:
            self.history.append(
                {
                    "timestamp": current_time,
                    "bids": self.order_book.bids.copy(),
                    "asks": self.order_book.asks.copy(),
                    "last_update_id": self.order_book.last_update_id,
                }
            )

            # 保留最近的历史数据
            if len(self.history) > MAX_HISTORY_SNAPSHOTS:
                self.history.pop(0)

        return True

    async def connect_websocket(self):
        """连接WebSocket并处理消息"""
        while not shutdown_event.is_set():
            try:
                async with websockets.connect(WEBSOCKET_URI) as websocket:
                    logger.info(f"Connected to WebSocket: {WEBSOCKET_URI}")
                    self.is_connected = True

                    # 获取初始快照
                    if self.order_book.last_update_id == 0:
                        self.order_book = await self.get_depth_snapshot()
                        self.history.append(
                            {
                                "timestamp": int(self.order_book.timestamp),
                                "bids": self.order_book.bids.copy(),
                                "asks": self.order_book.asks.copy(),
                                "last_update_id": self.order_book.last_update_id,
                            }
                        )

                    async for message in websocket:
                        # 检查是否需要关闭
                        if shutdown_event.is_set():
                            logger.info(
                                "Received shutdown signal, closing WebSocket..."
                            )
                            break

                        try:
                            data = json.loads(message)
                            if "data" in data:
                                event = data["data"]
                                success = self.process_depth_event(event)
                                if not success:
                                    # 重新初始化
                                    logger.info("Reinitializing order book...")
                                    self.order_book = await self.get_depth_snapshot()
                                    self.last_event_u = 0
                                    self.event_buffer.clear()

                        except json.JSONDecodeError as e:
                            logger.error(f"JSON decode error: {e}")
                        except Exception as e:
                            logger.error(f"Error processing message: {e}")

                    # 如果是因为关闭信号退出循环，直接返回
                    if shutdown_event.is_set():
                        logger.info(
                            "WebSocket connection closed due to shutdown signal"
                        )
                        return

            except Exception as e:
                if shutdown_event.is_set():
                    logger.info(
                        "WebSocket connection error during shutdown, exiting..."
                    )
                    return
                logger.error(f"WebSocket connection error: {e}")
                self.is_connected = False
                await asyncio.sleep(RECONNECT_DELAY)  # 重连延迟

    def get_quantity_at_price(
        self, price: float, timestamp: Optional[int] = None
    ) -> Tuple[float, float]:
        """获取指定时间点指定价格的持仓量，如果没有传入时间戳，返回离撮合价格最近的一档"""
        if timestamp is None:
            # 返回当前时间离撮合价格最近的一档
            return self.get_nearest_level_quantity(price)

        # 找到最接近指定时间的历史快照
        target_snapshot = None
        for snapshot in reversed(self.history):
            if snapshot["timestamp"] <= timestamp:
                target_snapshot = snapshot
                break

        if target_snapshot is None:
            return price, 0.0

        # 查找价格
        if price in target_snapshot["bids"]:
            return price, target_snapshot["bids"][price]
        elif price in target_snapshot["asks"]:
            return price, target_snapshot["asks"][price]
        else:
            return price, 0.0

    def get_nearest_level_quantity(self, target_price: float) -> Tuple[float, float]:
        """获取离目标价格最近的一档价格和数量"""
        if not self.order_book.bids and not self.order_book.asks:
            return target_price, 0.0

        nearest_price = target_price
        nearest_quantity = 0.0
        min_distance = float("inf")

        # 检查bids
        for price in self.order_book.bids.keys():
            distance = abs(price - target_price)
            if distance < min_distance:
                min_distance = distance
                nearest_price = price
                nearest_quantity = self.order_book.bids[price]

        # 检查asks
        for price in self.order_book.asks.keys():
            distance = abs(price - target_price)
            if distance < min_distance:
                min_distance = distance
                nearest_price = price
                nearest_quantity = self.order_book.asks[price]

        return nearest_price, nearest_quantity

    def get_quantity_difference(
        self, price: float, timestamp: Optional[int] = None
    ) -> Tuple[float, float, float]:
        """获取指定时间点和1秒前的持仓量差值，如果没有传入时间戳，返回当前最近档位的信息"""
        if timestamp is None:
            # 返回当前时间最近档位的信息
            nearest_price, nearest_quantity = self.get_nearest_level_quantity(price)
            return nearest_price, nearest_quantity, 0.0  # 当前时间没有差值

        # 获取指定时间点的数据
        current_price, current_qty = self.get_quantity_at_price(price, timestamp)
        one_second_ago_price, one_second_ago_qty = self.get_quantity_at_price(
            price, timestamp - 1
        )

        # 如果价格相同，计算差值
        if current_price == one_second_ago_price:
            difference = current_qty - one_second_ago_qty
        else:
            # 如果价格不同，返回当前价格和数量，差值为0
            difference = 0.0

        return current_price, current_qty, difference


# FastAPI模型
class QuantityRequest(BaseModel):
    price: float
    timestamp: Optional[int] = None


class QuantityResponse(BaseModel):
    target_price: float  # 查询的目标价格
    actual_price: float  # 实际返回的价格（可能是最近档位）
    timestamp: int
    quantity: float
    difference: float
    is_nearest_level: bool  # 是否返回的是最近档位


# 全局order book管理器
order_book_manager = OrderBookManager()

# FastAPI应用
app = FastAPI(title="Order Book API", description="本地Order Book查询API")


@app.get("/")
async def root():
    return {"message": "Order Book API is running"}


@app.get("/status")
async def get_status():
    return {
        "symbol": order_book_manager.symbol,
        "is_connected": order_book_manager.is_connected,
        "last_update_id": order_book_manager.order_book.last_update_id,
        "bids_count": len(order_book_manager.order_book.bids),
        "asks_count": len(order_book_manager.order_book.asks),
        "history_count": len(order_book_manager.history),
    }


@app.post("/quantity", response_model=QuantityResponse)
async def get_quantity(request: QuantityRequest):
    """获取指定价格和时间点的持仓量及差值"""
    try:
        current_time = int(time.time())

        if request.timestamp is None:
            # 没有传入时间戳，返回当前时间最近档位
            actual_price, quantity = order_book_manager.get_quantity_at_price(
                request.price
            )
            return QuantityResponse(
                target_price=request.price,
                actual_price=actual_price,
                timestamp=current_time,
                quantity=quantity,
                difference=0.0,
                is_nearest_level=True,
            )
        else:
            # 传入时间戳，返回历史数据
            actual_price, quantity, difference = (
                order_book_manager.get_quantity_difference(
                    request.price, request.timestamp
                )
            )
            return QuantityResponse(
                target_price=request.price,
                actual_price=actual_price,
                timestamp=request.timestamp,
                quantity=quantity,
                difference=difference,
                is_nearest_level=False,
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/nearest-level/{price}")
async def get_nearest_level(price: float):
    """获取离指定价格最近的一档价格和数量"""
    try:
        actual_price, quantity = order_book_manager.get_nearest_level_quantity(price)
        return {
            "target_price": price,
            "nearest_price": actual_price,
            "quantity": quantity,
            "timestamp": int(time.time()),
            "price_difference": actual_price - price,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/orderbook")
async def get_current_orderbook():
    """获取当前order book"""
    return {
        "symbol": order_book_manager.symbol,
        "timestamp": order_book_manager.order_book.timestamp,
        "last_update_id": order_book_manager.order_book.last_update_id,
        "bids": order_book_manager.order_book.bids,
        "asks": order_book_manager.order_book.asks,
    }


@app.get("/history")
async def get_history_info():
    """获取历史数据信息"""
    return {
        "history_count": len(order_book_manager.history),
        "time_range": {
            "start": (
                order_book_manager.history[0]["timestamp"]
                if order_book_manager.history
                else None
            ),
            "end": (
                order_book_manager.history[-1]["timestamp"]
                if order_book_manager.history
                else None
            ),
        },
    }


async def main():
    """主函数"""
    websocket_task = None

    # 在异步环境中处理信号
    def signal_handler():
        logger.info("Received shutdown signal, initiating graceful shutdown...")
        shutdown_event.set()

    # 使用asyncio来处理信号
    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGINT, signal_handler)
    loop.add_signal_handler(signal.SIGTERM, signal_handler)

    try:
        # 启动WebSocket连接
        websocket_task = asyncio.create_task(order_book_manager.connect_websocket())

        # 启动FastAPI服务器
        config = uvicorn.Config(app, host=API_HOST, port=API_PORT, log_level="info")
        server = uvicorn.Server(config)

        # 并发运行
        await asyncio.gather(server.serve(), websocket_task, return_exceptions=True)
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received, shutting down...")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        # 优雅关闭
        logger.info("Shutting down gracefully...")
        shutdown_event.set()

        # 等待任务完成
        if websocket_task:
            try:
                await asyncio.wait_for(websocket_task, timeout=5.0)
            except asyncio.TimeoutError:
                logger.warning("WebSocket task did not complete within timeout")

        logger.info("Shutdown complete")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n程序已退出")
    except Exception as e:
        print(f"程序异常退出: {e}")
        sys.exit(1)
