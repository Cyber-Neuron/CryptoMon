"""巨鲸交易检测和分析."""

import time
from datetime import datetime
from typing import Dict, List, Set, Tuple

from bitcoin.core import COutPoint, CTransaction, CTxIn, CTxOut
from bitcoin.core.script import CScript
from core.constants import LARGE_TX_THRESHOLD_BTC
from monitors.utxo_tracker import UTXOTracker
from utils.bitcoin_utils import get_address_from_script
from utils.logging_utils import setup_logging

logger = setup_logging()


class WhaleDetector:
    """检测和分析巨鲸交易."""

    def __init__(
        self, utxo_tracker: UTXOTracker, threshold: float = LARGE_TX_THRESHOLD_BTC
    ):
        self.utxo_tracker = utxo_tracker
        self.whale_addresses: Set[str] = set()
        self.threshold = threshold
        self.tx_history: Dict[str, List[Tuple[float, datetime]]] = {}  # 地址交易历史

    def format_amount(self, satoshis: int) -> str:
        """格式化金额显示."""
        btc = satoshis / 1e8
        if btc >= 1000:
            return f"{btc:,.2f} BTC (约 ${btc * 40000:,.2f})"  # 假设BTC价格为40000美元
        return f"{btc:,.8f} BTC"

    def analyze_input(self, vin: CTxIn) -> Tuple[str, int]:
        """分析交易输入."""
        prev_utxo = self.utxo_tracker.spend_utxo(vin.prevout.hash.hex(), vin.prevout.n)
        if prev_utxo:
            return prev_utxo.address or "未知地址", prev_utxo.value
        return "未知地址", 0

    def analyze_output(self, vout: CTxOut) -> Tuple[str, int]:
        """分析交易输出."""
        address = get_address_from_script(vout.scriptPubKey)
        return address or "未知地址", vout.nValue

    def update_tx_history(self, address: str, amount: float) -> None:
        """更新地址交易历史."""
        if address not in self.tx_history:
            self.tx_history[address] = []
        self.tx_history[address].append((amount, datetime.now()))

    def get_address_stats(self, address: str) -> str:
        """获取地址统计信息."""
        if address not in self.tx_history:
            return "无历史交易记录"

        history = self.tx_history[address]
        total_amount = sum(amount for amount, _ in history)
        avg_amount = total_amount / len(history)
        last_tx_time = history[-1][1]

        return (
            f"历史交易次数: {len(history)}\n"
            f"总交易金额: {self.format_amount(int(total_amount * 1e8))}\n"
            f"平均交易金额: {self.format_amount(int(avg_amount * 1e8))}\n"
            f"最近交易时间: {last_tx_time.strftime('%Y-%m-%d %H:%M:%S')}"
        )

    def analyze_transaction(self, tx: CTransaction) -> None:
        """分析交易中的巨鲸活动."""
        # 检查总输出金额
        total_output = sum(vout.nValue for vout in tx.vout) / 1e8
        if total_output >= self.threshold:
            tx_time = datetime.now()
            logger.info("=" * 80)
            logger.info(f"🐋 发现巨鲸交易")
            logger.info(f"交易ID: {tx.GetTxid()[::-1].hex(),tx.GetTxid()}")
            logger.info(f"交易时间: {tx_time.strftime('%Y-%m-%d %H:%M:%S')}")
            logger.info(f"交易总金额: {self.format_amount(int(total_output * 1e8))}")
            logger.info(f"交易大小: {len(tx.serialize())} 字节")
            # 计算交易费用
            total_input = sum(
                amount for _, amount in [self.analyze_input(vin) for vin in tx.vin]
            )
            fee = total_input - (total_output * 1e8)
            logger.info(
                f"交易费用: {self.format_amount(int(fee)) if fee > 0 else '未知'}"
            )

            # 分析输入
            logger.info("\n📥 交易输入:")
            total_input = 0
            input_addresses = []
            for i, vin in enumerate(tx.vin):
                address, amount = self.analyze_input(vin)
                total_input += amount
                input_addresses.append(address)
                logger.info(f"输入 {i+1}:")
                logger.info(f"  地址: {address}")
                logger.info(f"  金额: {self.format_amount(amount)}")
                logger.info(f"  前序交易: {vin.prevout.hash.hex()}:{vin.prevout.n}")

            # 分析输出
            logger.info("\n📤 交易输出:")
            for i, vout in enumerate(tx.vout):
                address, amount = self.analyze_output(vout)
                logger.info(f"输出 {i+1}:")
                logger.info(f"  地址: {address}")
                logger.info(f"  金额: {self.format_amount(amount)}")
                logger.info(f"  脚本类型: {vout.scriptPubKey.hex()[:50]}...")

            # 更新地址聚类
            if input_addresses:
                self.utxo_tracker.update_address_cluster(input_addresses)

                # 检查地址集群余额
                logger.info("\n👥 地址集群分析:")
                for addr in input_addresses:
                    cluster_balance = self.utxo_tracker.get_cluster_balance(addr) / 1e8
                    if cluster_balance >= self.threshold:
                        self.whale_addresses.add(addr)
                        logger.info(f"\n巨鲸地址: {addr}")
                        logger.info(
                            f"集群余额: {self.format_amount(int(cluster_balance * 1e8))}"
                        )
                        logger.info("地址统计:")
                        logger.info(self.get_address_stats(addr))

            # 交易摘要
            logger.info("\n📊 交易摘要:")
            logger.info(f"输入总额: {self.format_amount(total_input)}")
            logger.info(f"输出总额: {self.format_amount(int(total_output * 1e8))}")
            if total_input > 0:
                logger.info(f"交易费用: {self.format_amount(int(fee))}")
                logger.info(f"费用率: {fee/len(tx.serialize()):.1f} sat/byte")

            logger.info("=" * 80)
