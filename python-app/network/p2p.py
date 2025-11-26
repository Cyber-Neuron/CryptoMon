"""Bitcoin P2P network connection management."""

import io
import socket
import struct
import threading
import time
from typing import List, Optional, Tuple

import requests
from bitcoin.core import CTransaction
from core.constants import MAGIC_MAINNET, PROTOCOL_VERSION
from monitors.arbitrage import ArbitrageSignalGenerator
from monitors.utxo_tracker import UTXOTracker
from monitors.whale_detector import WhaleDetector
from network.tor import create_tor_socket
from utils.bitcoin_utils import make_message, sha256d
from utils.logging_utils import setup_logging

logger = setup_logging()


class P2PConnection:
    """Manages a single P2P connection to a Bitcoin node."""

    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        self.sock = None
        self.utxo_tracker = UTXOTracker()
        self.whale_detector = WhaleDetector(self.utxo_tracker)
        self.arbitrage_generator = ArbitrageSignalGenerator(self.utxo_tracker)
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 3
        self.reconnect_delay = 30  # 重连等待时间（秒）

    def connect(self) -> bool:
        """Establish connection to the node."""
        try:
            self.sock = create_tor_socket()
            self.sock.settimeout(30)  # 增加超时时间到30秒
            self.sock.connect((self.ip, self.port))
            logger.info(f"Connected to {self.ip}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            return False

    def reconnect(self) -> bool:
        """Attempt to reconnect to the node."""
        if self.reconnect_attempts >= self.max_reconnect_attempts:
            logger.warning(
                f"Max reconnection attempts reached for {self.ip}:{self.port}"
            )
            return False

        self.reconnect_attempts += 1
        logger.info(
            f"Attempting to reconnect to {self.ip}:{self.port} (attempt {self.reconnect_attempts})"
        )

        # 关闭旧连接
        self.close()

        # 等待一段时间后重试
        time.sleep(self.reconnect_delay)

        # 尝试重新连接
        if self.connect() and self.handshake():
            logger.info(f"Successfully reconnected to {self.ip}:{self.port}")
            self.reconnect_attempts = 0  # 重置重连计数
            return True

        return False

    def handshake(self) -> bool:
        """Perform Bitcoin P2P protocol handshake."""
        try:
            # Send version
            self.sock.sendall(self._build_version())
            logger.debug(f"Sent version to {self.ip}")

            # Wait for version and verack
            version_ok, verack_ok = False, False
            while not (version_ok and verack_ok):
                cmd, payload = self._read_msg()
                if not cmd:
                    logger.warning(f"Connection closed during handshake with {self.ip}")
                    return False

                if cmd == "version":
                    if payload:
                        logger.debug(f"Version payload: {payload.hex()[:64]}...")
                        self.sock.sendall(make_message("verack", b""))
                        logger.debug(f"Sent verack to {self.ip}")
                        version_ok = True
                elif cmd == "verack":
                    verack_ok = True

            logger.info(f"Handshake completed with {self.ip}")
            return True
        except Exception as e:
            logger.error(f"Handshake failed: {e}")
            return False

    def start_monitoring(self) -> None:
        """Start monitoring the connection for transactions."""
        while True:
            try:
                if not self.sock:
                    if not self.connect() or not self.handshake():
                        break

                # 发送初始消息
                if self.sock:
                    self.sock.sendall(self._build_getaddr())
                    self.sock.sendall(self._build_sendheaders())
                    self.sock.sendall(self._build_mempool())
                    self.sock.sendall(self._build_sendcmpct())
                    self.sock.sendall(self._build_feefilter())

                # 主消息循环
                while self.sock:
                    cmd, payload = self._read_msg()
                    if not cmd:
                        logger.warning(f"Connection closed with {self.ip}")
                        if not self.reconnect():
                            break
                        continue

                    logger.debug(f"Received {cmd} from {self.ip}")

                    if cmd == "inv":
                        if payload and self.sock:
                            txids = self._parse_inv(payload)
                            if txids:
                                self.sock.sendall(self._build_getdata(txids))
                                logger.debug(
                                    f"Requested {len(txids)} transactions from {self.ip}"
                                )
                    elif cmd == "tx":
                        if payload:
                            self._analyze_tx(payload)
                    elif cmd == "ping":
                        if payload and self.sock:
                            self.sock.sendall(make_message("pong", payload))
                            logger.debug(f"Sent pong to {self.ip}")

            except socket.timeout:
                logger.warning(f"Connection timeout with {self.ip}")
                if not self.reconnect():
                    break
            except Exception as e:
                logger.error(f"Monitoring error: {e}")
                if not self.reconnect():
                    break
            finally:
                self.close()

    def close(self) -> None:
        """Close the connection."""
        if self.sock:
            try:
                self.sock.close()
            except:
                pass
            self.sock = None

    def _read_msg(self) -> Tuple[Optional[str], Optional[bytes]]:
        """Read and parse a Bitcoin P2P message."""
        try:
            header = self.sock.recv(24)
            if len(header) < 24:
                return None, None

            magic, command, length, checksum = struct.unpack("<4s12sI4s", header)
            if magic != MAGIC_MAINNET:
                logger.warning(f"Invalid magic number: {magic.hex()}")
                return None, None

            command = command.rstrip(b"\x00").decode()
            payload = b""
            while len(payload) < length:
                chunk = self.sock.recv(length - len(payload))
                if not chunk:
                    return None, None
                payload += chunk

            if sha256d(payload)[:4] != checksum:
                logger.warning(f"Checksum mismatch for {command} message")
                return None, None

            logger.debug(f"Received {command} message: {payload.hex()[:64]}...")
            return command, payload
        except Exception as e:
            logger.error(f"Error reading message: {e}")
            return None, None

    def _build_version(self) -> bytes:
        """Build version message for handshake."""
        services = 0
        timestamp = int(time.time())
        addr_recv = b"\x00" * 26
        addr_from = b"\x00" * 26
        nonce = 0
        user_agent_bytes = b"\x00"
        start_height = 0
        relay = 1

        payload = struct.pack(
            "<iQQ26s26sQ",
            PROTOCOL_VERSION,
            services,
            timestamp,
            addr_recv,
            addr_from,
            nonce,
        )
        payload += user_agent_bytes
        payload += struct.pack("<i?", start_height, relay)

        return make_message("version", payload)

    def _build_getaddr(self) -> bytes:
        """Build getaddr message."""
        return make_message("getaddr", b"")

    def _build_sendheaders(self) -> bytes:
        """Build sendheaders message."""
        return make_message("sendheaders", b"")

    def _build_mempool(self) -> bytes:
        """Build mempool message."""
        return make_message("mempool", b"")

    def _build_sendcmpct(self) -> bytes:
        """Build sendcmpct message."""
        version = struct.pack("<Q", 1)
        mode = struct.pack("<B", 1)
        return make_message("sendcmpct", version + mode)

    def _build_feefilter(self) -> bytes:
        """Build feefilter message."""
        feerate = struct.pack("<Q", 0)  # 0 sat/byte
        return make_message("feefilter", feerate)

    def _parse_inv(self, payload: bytes) -> List[str]:
        """Parse inventory message."""
        count = payload[0]
        items = []
        offset = 1
        for _ in range(count):
            if offset + 36 > len(payload):
                break
            (typ,) = struct.unpack("<I", payload[offset : offset + 4])
            hash = payload[offset + 4 : offset + 36][::-1].hex()
            if typ == 1:  # MSG_TX
                items.append(hash)
                logger.debug(f"Found transaction hash: {hash}")
            offset += 36
        return items

    def _build_getdata(self, txids: List[str]) -> bytes:
        """Build getdata message for transactions."""
        count = struct.pack("B", len(txids))
        payload = count
        for txid in txids:
            payload += struct.pack("<I", 1)  # MSG_TX
            payload += bytes.fromhex(txid)[::-1]
        return make_message("getdata", payload)

    def _analyze_tx(self, payload: bytes) -> None:
        """Analyze transaction for large amounts and generate signals."""
        logger.debug(f"Analyzing transaction: {payload.hex()[:64]}...")
        tx = CTransaction.stream_deserialize(io.BytesIO(payload))

        # Process transaction with enhanced monitoring
        self.whale_detector.analyze_transaction(tx)

        # Check for arbitrage signals
        signal = self.arbitrage_generator.analyze_transaction(tx)
        if signal:
            logger.info(signal)
