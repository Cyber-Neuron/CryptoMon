"""
测试数据补齐程序的功能
"""

import logging

from config import load_config
from data_completer import DataCompleter

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def test_data_completer():
    """测试数据补齐程序"""
    try:
        # 加载配置
        config = load_config()

        # 创建数据补齐器
        completer = DataCompleter(config)

        # 测试获取不完整交易
        incomplete_transactions = completer.get_incomplete_transactions()
        logger.info(f"Found {len(incomplete_transactions)} incomplete transactions")

        if incomplete_transactions:
            # 测试处理第一个交易
            tx_id, tx_hash = incomplete_transactions[0]
            logger.info(f"Testing with transaction {tx_id}: {tx_hash}")

            # 测试获取交易详情
            tx_details = completer.get_transaction_details(tx_hash)
            if tx_details:
                logger.info(f"Transaction details: {tx_details}")

                # 测试处理钱包地址
                if tx_details.get("from"):
                    from_wallet_id = completer.process_wallet_address(
                        tx_details["from"]
                    )
                    logger.info(f"From wallet ID: {from_wallet_id}")

                if tx_details.get("to"):
                    to_wallet_id = completer.process_wallet_address(tx_details["to"])
                    logger.info(f"To wallet ID: {to_wallet_id}")
            else:
                logger.warning("Failed to get transaction details")

        logger.info("Data completer test completed successfully")

    except Exception as e:
        logger.error(f"Data completer test failed: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    test_data_completer()
