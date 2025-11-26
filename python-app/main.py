"""Main entry point for the Bitcoin monitoring system."""

import argparse
import logging
import random
import threading
import time
from typing import Dict, List, Set, Tuple

import requests
from network.p2p import P2PConnection
from network.tor import configure_tor, test_tor_connection
from utils.logging_utils import setup_logging

logger = setup_logging()


class SimplePeerPool:
    """简单的节点池管理."""

    def __init__(self):
        self.bad_peers: Set[str] = set()  # 坏掉的节点
        self.lock = threading.Lock()

    def mark_bad(self, ip: str) -> None:
        """标记节点为坏节点."""
        with self.lock:
            self.bad_peers.add(ip)
            logger.warning(f"Marked {ip} as bad peer")

    def get_peers(
        self, all_peers: List[Tuple[str, int]], count: int
    ) -> List[Tuple[str, int]]:
        """随机获取指定数量的节点."""
        logger.debug(f"Getting {count} random peers from {len(all_peers)} total peers")
        try:
            # 直接随机选择节点
            selected = random.sample(all_peers, min(count, len(all_peers)))
            logger.debug(f"Selected {len(selected)} random peers")
            return selected
        except Exception as e:
            logger.error(f"Error in get_peers: {e}")
            return []


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Bitcoin monitoring system")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )
    parser.add_argument(
        "--peers",
        type=int,
        default=4,
        help="Number of peers to connect (default: 4)",
    )
    parser.add_argument(
        "--whale-threshold",
        type=float,
        default=100.0,
        help="Threshold for whale transaction detection in BTC (default: 100.0)",
    )
    return parser.parse_args()


def fetch_peers() -> List[Tuple[str, int]]:
    """获取比特币节点地址."""
    logger.info("Fetching peers from Bitnodes...")
    url = "https://bitnodes.io/api/v1/snapshots/latest/"
    try:
        response = requests.get(url, proxies=configure_tor(), timeout=10)
        if response.status_code != 200:
            logger.error(f"Failed to fetch peers: HTTP {response.status_code}")
            return []
        data = response.json()
        peers = list(data["nodes"].keys())
        logger.info(f"Found {len(peers)} peers")
    except Exception as e:
        logger.error(f"Error fetching peers: {e}")
        return []

    valid_peers = []
    for ip_port in peers:
        try:
            # 处理IPv6地址
            if "[" in ip_port and "]" in ip_port:
                # 提取IPv6地址和端口
                ip_end = ip_port.find("]")
                if ip_end == -1:
                    logger.warning(f"Invalid IPv6 format: {ip_port}")
                    continue
                ip = ip_port[1:ip_end]
                port = ip_port[ip_end + 2 :]  # 跳过]: 两个字符
            else:
                # 处理普通IPv4地址
                parts = ip_port.split(":")
                if len(parts) != 2:
                    logger.warning(f"Skipping invalid peer format: {ip_port}")
                    continue
                ip, port = parts

            # 只接受onion地址
            if ".onion" not in ip:
                logger.debug(f"Skipping non-onion address: {ip_port}")
                continue

            # 转换端口号，处理十六进制格式
            try:
                port = int(port)
            except ValueError:
                try:
                    port = int(port, 16)
                except ValueError:
                    logger.warning(f"Skipping peer with invalid port: {ip_port}")
                    continue

            # 验证端口范围
            if not (0 < port < 65536):
                logger.warning(f"Skipping peer with invalid port range: {ip_port}")
                continue

            valid_peers.append((ip, port))
            logger.debug(f"Added valid peer: {ip}:{port}")

        except Exception as e:
            logger.warning(f"Error processing peer {ip_port}: {e}")
            continue

    logger.info(f"Found {len(valid_peers)} valid peers")
    return valid_peers


def connect_to_peer(
    ip: str, port: int, whale_threshold: float, peer_pool: SimplePeerPool
) -> None:
    """连接到单个节点."""
    try:
        logger.debug(f"Attempting to connect to {ip}:{port}")
        conn = P2PConnection(ip, port)
        conn.whale_detector.threshold = whale_threshold
        if conn.connect() and conn.handshake():
            logger.info(f"Successfully connected to {ip}:{port}")
            conn.start_monitoring()
        else:
            logger.warning(f"Failed to connect to {ip}:{port}")
            peer_pool.mark_bad(ip)
    except Exception as e:
        logger.error(f"Error connecting to {ip}:{port}: {e}")
        peer_pool.mark_bad(ip)


def main() -> None:
    """Main entry point."""
    args = parse_args()

    # 设置日志级别
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled")

    # 等待Tor就绪
    logger.info("Waiting for Tor to be ready...")
    time.sleep(10)

    # 测试Tor连接
    if not test_tor_connection():
        logger.error("Tor connection test failed. Please check your Tor setup.")
        return

    # 获取所有可用节点
    all_peers = fetch_peers()
    if not all_peers:
        logger.error("No valid peers found")
        return

    logger.info(f"Starting with {len(all_peers)} total peers")

    # 创建节点池
    peer_pool = SimplePeerPool()
    workers = []

    try:
        while True:
            # 随机选择节点
            selected_peers = peer_pool.get_peers(all_peers, args.peers)
            if not selected_peers:
                logger.warning("No peers available, waiting...")
                time.sleep(60)
                continue

            # 清理已结束的线程
            workers = [w for w in workers if w.is_alive()]
            logger.debug(f"Active workers: {len(workers)}")

            # 启动新的连接
            for peer in selected_peers:
                if len(workers) >= args.peers:
                    logger.debug("Maximum number of workers reached")
                    break

                logger.info(f"Connecting to {peer[0]}:{peer[1]}")
                t = threading.Thread(
                    target=connect_to_peer,
                    args=(peer[0], peer[1], args.whale_threshold, peer_pool),
                    daemon=True,
                )
                workers.append(t)
                t.start()
                logger.debug(f"Started worker for {peer[0]}:{peer[1]}")

            # 等待一段时间
            time.sleep(10)

            # 显示当前状态
            active_count = sum(1 for w in workers if w.is_alive())
            logger.info(f"Currently connected to {active_count} peers")
            logger.debug(f"Bad peers count: {len(peer_pool.bad_peers)}")

    except KeyboardInterrupt:
        logger.info("Received shutdown signal")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        logger.info("Shutting down...")


if __name__ == "__main__":
    main()
