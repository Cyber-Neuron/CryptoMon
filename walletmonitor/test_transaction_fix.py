#!/usr/bin/env python3
"""
测试事务修复的脚本
"""

import logging

from config import load_config
from data_completer import DataCompleter

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def test_transaction_processing():
    """测试交易处理的事务管理"""
    try:
        # 加载配置
        config = load_config()

        # 创建数据补齐器
        completer = DataCompleter(config)

        # 获取一个不完整的交易进行测试
        incomplete_transactions = completer.get_incomplete_transactions()

        if not incomplete_transactions:
            print("没有找到不完整的交易进行测试")
            return

        # 测试第一个交易
        tx_id, tx_hash = incomplete_transactions[0]
        print(f"测试交易: ID={tx_id}, Hash={tx_hash}")

        # 处理交易
        success = completer.process_transaction(tx_id, tx_hash)

        if success:
            print("✅ 交易处理成功")
        else:
            print("❌ 交易处理失败")

    except Exception as e:
        logger.error(f"测试失败: {e}", exc_info=True)
        print(f"❌ 错误: {e}")


def test_single_transaction_update():
    """测试单个交易更新"""
    try:
        # 加载配置
        config = load_config()

        # 创建数据补齐器
        completer = DataCompleter(config)

        # 获取一个不完整的交易进行测试
        incomplete_transactions = completer.get_incomplete_transactions()

        if not incomplete_transactions:
            print("没有找到不完整的交易进行测试")
            return

        # 测试第一个交易
        tx_id, tx_hash = incomplete_transactions[0]
        print(f"测试单个交易更新: Hash={tx_hash}")

        # 获取交易详情
        tx_details = completer.get_transaction_details(tx_hash)
        if not tx_details:
            print("❌ 无法获取交易详情")
            return

        print(f"交易详情: From={tx_details.get('from')}, To={tx_details.get('to')}")

        # 使用单个数据库连接处理整个事务
        with completer.db_manager.get_connection() as conn:
            try:
                # 处理钱包地址
                from_wallet_id = None
                to_wallet_id = None

                if tx_details.get("from"):
                    from_wallet_id = completer.process_wallet_address(
                        tx_details["from"], conn
                    )
                    print(f"发送方钱包ID: {from_wallet_id}")

                if tx_details.get("to"):
                    to_wallet_id = completer.process_wallet_address(
                        tx_details["to"], conn
                    )
                    print(f"接收方钱包ID: {to_wallet_id}")

                # 更新数据库中的交易记录
                if from_wallet_id is not None or to_wallet_id is not None:
                    success = completer.update_transaction_by_hash(
                        tx_hash, from_wallet_id, to_wallet_id, conn
                    )
                    if success:
                        conn.commit()
                        print("✅ 成功更新交易记录")
                    else:
                        conn.rollback()
                        print("❌ 更新交易记录失败")
                else:
                    print("⚠️ 没有钱包信息需要更新")

            except Exception as e:
                conn.rollback()
                print(f"❌ 处理过程中发生错误: {e}")

    except Exception as e:
        logger.error(f"测试失败: {e}", exc_info=True)
        print(f"❌ 错误: {e}")


def main():
    """主函数"""
    print("测试事务修复")
    print("=" * 50)

    print("\n1. 测试交易处理:")
    test_transaction_processing()

    print("\n2. 测试单个交易更新:")
    test_single_transaction_update()

    print("\n" + "=" * 50)
    print("测试完成")


if __name__ == "__main__":
    main()
