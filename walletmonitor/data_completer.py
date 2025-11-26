"""
数据补齐程序 - 补充数据库中缺失的钱包信息
"""

import logging
from typing import List, Optional, Tuple

from block_processor import BlockProcessor
from config import Config, load_config
from database import DatabaseManager
from models import Wallet
from web3 import Web3

logger = logging.getLogger(__name__)


class DataCompleter:
    """数据补齐器，用于补充数据库中缺失的钱包信息"""

    def __init__(self, config: Config):
        self.config = config
        self.web3 = Web3(Web3.HTTPProvider(str(config.PUBLICNODE_URL)))
        self.db_manager = DatabaseManager()
        self.block_processor = BlockProcessor(self.web3, self.db_manager, config)

        if not self.web3.is_connected():
            raise ConnectionError(
                f"Failed to connect to Ethereum node: {config.PUBLICNODE_URL}"
            )

        logger.info("DataCompleter initialized successfully")

    def get_incomplete_transactions(self) -> List[Tuple[int, str]]:
        """
        获取数据库中缺失钱包信息的交易记录

        Returns:
            List[Tuple[int, str]]: 包含 (transaction_id, hash) 的列表
        """
        incomplete_transactions = []

        with self.db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, hash 
                    FROM transactions 
                    WHERE from_wallet_id IS NULL OR to_wallet_id IS NULL
                    ORDER BY id
                """
                )

                for row in cur.fetchall():
                    incomplete_transactions.append((row[0], row[1]))

        logger.info(
            f"Found {len(incomplete_transactions)} transactions with missing wallet info"
        )
        return incomplete_transactions

    def get_transaction_details(self, tx_hash: str) -> Optional[dict]:
        """
        通过 Web3 获取交易详细信息

        Args:
            tx_hash: 交易哈希

        Returns:
            Optional[dict]: 交易详情，包含 from 和 to 地址
        """
        try:
            # 直接使用字符串哈希，Web3会自动处理
            tx = self.web3.eth.get_transaction(tx_hash)  # type: ignore

            if tx:
                # 安全地访问交易数据
                tx_hash_hex = tx.get("hash")
                if tx_hash_hex and hasattr(tx_hash_hex, "hex"):
                    tx_hash_str = tx_hash_hex.hex()
                else:
                    tx_hash_str = str(tx_hash_hex) if tx_hash_hex else ""

                return {
                    "from": tx.get("from"),
                    "to": tx.get("to"),
                    "hash": tx_hash_str,
                    "block_number": tx.get("blockNumber"),
                    "value": tx.get("value"),
                }
            else:
                logger.warning(f"No transaction found for hash: {tx_hash}")
                return None

        except Exception as e:
            logger.error(f"Error getting transaction details for {tx_hash}: {e}")
            return None

    def process_wallet_address(self, address: str, conn) -> Optional[int]:
        """
        处理钱包地址，获取或创建钱包记录

        Args:
            address: 钱包地址
            conn: 数据库连接

        Returns:
            Optional[int]: 钱包ID，如果失败返回None
        """
        try:
            # 使用 extract_wallet_info 获取钱包信息
            address = address.lower() if address else ""
            wallets = self.db_manager.get_wallets_batch(conn, [address])
            # print(wallets, address, len(wallets), address in wallets)
            if wallets and len(wallets) > 0 and address in wallets:
                wallet = wallets[address]
                # print(wallet.id)
                return wallet.id
            else:
                # 1 / 0
                wallet = self.block_processor.extract_wallet_info(address)

                # 存储钱包到数据库（使用传入的连接）
                wallet_id = self.db_manager.get_or_create_wallet(conn, wallet)
                print(f"Processed wallet {address} -> ID: {wallet_id}")

                return wallet_id

        except Exception as e:
            logger.error(f"Error processing wallet address {address}: {e}")
            return None

    def update_transaction_by_hash(
        self,
        tx_hash: str,
        from_wallet_id: Optional[int],
        to_wallet_id: Optional[int],
        conn,
    ) -> bool:
        """
        根据交易哈希更新交易记录的钱包ID

        Args:
            tx_hash: 交易哈希
            from_wallet_id: 发送方钱包ID
            to_wallet_id: 接收方钱包ID
            conn: 数据库连接

        Returns:
            bool: 更新是否成功
        """
        try:
            with conn.cursor() as cur:
                # 构建更新语句
                update_parts = []
                params = []

                if from_wallet_id is not None:
                    update_parts.append("from_wallet_id = %s")
                    params.append(from_wallet_id)

                if to_wallet_id is not None:
                    update_parts.append("to_wallet_id = %s")
                    params.append(to_wallet_id)

                if not update_parts:
                    logger.warning(
                        f"No wallet IDs to update for transaction hash: {tx_hash}"
                    )
                    return False

                params.append(tx_hash)
                query = f"""
                    UPDATE transactions 
                    SET {', '.join(update_parts)}
                    WHERE hash = %s
                """

                cur.execute(query, params)
                # 不在这里提交，由外层管理事务

                logger.debug(
                    f"Updated transaction {tx_hash}: from_wallet_id={from_wallet_id}, to_wallet_id={to_wallet_id}"
                )
                return True

        except Exception as e:
            logger.error(f"Error updating transaction {tx_hash}: {e}")
            return False

    def update_transaction_wallets(
        self,
        tx_id: int,
        from_wallet_id: Optional[int],
        to_wallet_id: Optional[int],
        conn,
    ) -> bool:
        """
        更新交易记录的钱包ID（通过交易ID）

        Args:
            tx_id: 交易ID
            from_wallet_id: 发送方钱包ID
            to_wallet_id: 接收方钱包ID
            conn: 数据库连接

        Returns:
            bool: 更新是否成功
        """
        try:
            with conn.cursor() as cur:
                # 构建更新语句
                update_parts = []
                params = []

                if from_wallet_id is not None:
                    update_parts.append("from_wallet_id = %s")
                    params.append(from_wallet_id)

                if to_wallet_id is not None:
                    update_parts.append("to_wallet_id = %s")
                    params.append(to_wallet_id)

                if not update_parts:
                    logger.warning(f"No wallet IDs to update for transaction {tx_id}")
                    return False

                params.append(tx_id)
                query = f"""
                    UPDATE transactions 
                    SET {', '.join(update_parts)}
                    WHERE id = %s
                """

                cur.execute(query, params)
                # 不在这里提交，由外层管理事务

                logger.debug(
                    f"Updated transaction {tx_id}: from_wallet_id={from_wallet_id}, to_wallet_id={to_wallet_id}"
                )
                return True

        except Exception as e:
            logger.error(f"Error updating transaction {tx_id}: {e}")
            return False

    def process_transaction(self, tx_id: int, tx_hash: str) -> bool:
        """
        处理单个交易，补充缺失的钱包信息

        Args:
            tx_id: 交易ID
            tx_hash: 交易哈希

        Returns:
            bool: 处理是否成功
        """
        logger.info(f"Processing transaction {tx_id}: {tx_hash}")

        # 获取交易详情
        tx_details = self.get_transaction_details(tx_hash)
        if not tx_details:
            logger.warning(f"Failed to get transaction details for {tx_hash}")
            return False

        # 使用单个数据库连接处理整个事务
        with self.db_manager.get_connection() as conn:
            try:
                # 检查当前数据库中的钱包ID状态
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT from_wallet_id, to_wallet_id 
                        FROM transactions 
                        WHERE id = %s
                    """,
                        (tx_id,),
                    )
                    result = cur.fetchone()

                    if not result:
                        logger.error(f"Transaction {tx_id} not found in database")
                        return False

                    current_from_wallet_id, current_to_wallet_id = result

                # 处理缺失的发送方钱包
                from_wallet_id = current_from_wallet_id
                if current_from_wallet_id is None and tx_details.get("from"):
                    logger.debug(f"Processing from address: {tx_details['from']}")
                    from_wallet_id = self.process_wallet_address(
                        tx_details["from"], conn
                    )

                # 处理缺失的接收方钱包
                to_wallet_id = current_to_wallet_id
                if current_to_wallet_id is None and tx_details.get("to"):
                    logger.debug(f"Processing to address: {tx_details['to']}")
                    to_wallet_id = self.process_wallet_address(tx_details["to"], conn)

                # 更新数据库 - 使用交易哈希更新
                if (
                    from_wallet_id != current_from_wallet_id
                    or to_wallet_id != current_to_wallet_id
                ):
                    success = self.update_transaction_by_hash(
                        tx_hash, from_wallet_id, to_wallet_id, conn
                    )
                    if success:
                        # 提交整个事务
                        conn.commit()
                        logger.info(
                            f"Successfully updated transaction {tx_id} (hash: {tx_hash})"
                        )
                        return True
                    else:
                        # 回滚事务
                        conn.rollback()
                        logger.error(
                            f"Failed to update transaction {tx_id} (hash: {tx_hash})"
                        )
                        return False
                else:
                    logger.info(f"Transaction {tx_id} already has complete wallet info")
                    return True

            except Exception as e:
                # 发生错误时回滚事务
                conn.rollback()
                logger.error(f"Error processing transaction {tx_id}: {e}")
                return False

    def run(self, batch_size: int = 100) -> None:
        """
        运行数据补齐程序

        Args:
            batch_size: 批处理大小
        """
        logger.info("Starting data completion process...")

        # 获取所有不完整的交易
        incomplete_transactions = self.get_incomplete_transactions()

        if not incomplete_transactions:
            logger.info("No incomplete transactions found")
            return

        logger.info(
            f"Found {len(incomplete_transactions)} incomplete transactions to process"
        )

        # 分批处理
        success_count = 0
        error_count = 0

        for i in range(0, len(incomplete_transactions), batch_size):
            batch = incomplete_transactions[i : i + batch_size]
            logger.info(
                f"Processing batch {i//batch_size + 1}/{(len(incomplete_transactions) + batch_size - 1)//batch_size}"
            )

            for tx_id, tx_hash in batch:
                try:
                    if self.process_transaction(tx_id, tx_hash):
                        success_count += 1
                    else:
                        error_count += 1
                except Exception as e:
                    logger.error(f"Error processing transaction {tx_id}: {e}")
                    error_count += 1

        logger.info(f"Data completion process finished:")
        logger.info(f"  Successfully processed: {success_count}")
        logger.info(f"  Failed: {error_count}")
        logger.info(f"  Total: {len(incomplete_transactions)}")


def main():
    """主函数"""
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    try:
        # 加载配置
        config = load_config()

        # 创建数据补齐器
        completer = DataCompleter(config)

        # 运行数据补齐
        completer.run(batch_size=50)

    except Exception as e:
        logger.error(f"Data completion process failed: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
