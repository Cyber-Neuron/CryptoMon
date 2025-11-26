#!/usr/bin/env python3
"""
命令行工具 - 数据补齐程序
"""

import argparse
import logging
import sys
from typing import Optional

from config import load_config
from data_completer import DataCompleter

logger = logging.getLogger(__name__)


def setup_logging(verbose: bool = False, debug: bool = False) -> None:
    """设置日志级别"""
    if debug:
        level = logging.DEBUG
    elif verbose:
        level = logging.INFO
    else:
        level = logging.WARNING

    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("data_completer.log", mode="a"),
        ],
    )


def check_incomplete_transactions(completer: DataCompleter) -> None:
    """检查不完整的交易数量"""
    incomplete_transactions = completer.get_incomplete_transactions()
    print(f"Found {len(incomplete_transactions)} transactions with missing wallet info")

    if incomplete_transactions:
        print("\nFirst 5 incomplete transactions:")
        for i, (tx_id, tx_hash) in enumerate(incomplete_transactions[:5]):
            print(f"  {i+1}. ID: {tx_id}, Hash: {tx_hash}")

        if len(incomplete_transactions) > 5:
            print(f"  ... and {len(incomplete_transactions) - 5} more")


def test_single_transaction(completer: DataCompleter, tx_hash: str) -> None:
    """测试处理单个交易"""
    print(f"Testing transaction: {tx_hash}")

    # 获取交易详情
    tx_details = completer.get_transaction_details(tx_hash)
    if not tx_details:
        print("❌ Failed to get transaction details")
        return

    print(f"✅ Transaction details retrieved:")
    print(f"  From: {tx_details.get('from', 'N/A')}")
    print(f"  To: {tx_details.get('to', 'N/A')}")
    print(f"  Block: {tx_details.get('block_number', 'N/A')}")

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
                print(f"  From wallet ID: {from_wallet_id}")

            if tx_details.get("to"):
                to_wallet_id = completer.process_wallet_address(tx_details["to"], conn)
                print(f"  To wallet ID: {to_wallet_id}")

            # 更新数据库中的交易记录
            if from_wallet_id is not None or to_wallet_id is not None:
                success = completer.update_transaction_by_hash(
                    tx_hash, from_wallet_id, to_wallet_id, conn
                )
                if success:
                    conn.commit()
                    print(f"✅ Successfully updated transaction in database")
                else:
                    conn.rollback()
                    print(f"❌ Failed to update transaction in database")
            else:
                print("⚠️  No wallet information to update")

        except Exception as e:
            conn.rollback()
            print(f"❌ Error processing transaction: {e}")


def update_transaction_by_hash(completer: DataCompleter, tx_hash: str) -> None:
    """根据交易哈希更新交易记录"""
    print(f"Updating transaction: {tx_hash}")

    # 获取交易详情
    tx_details = completer.get_transaction_details(tx_hash)
    if not tx_details:
        print("❌ Failed to get transaction details")
        return

    print(f"✅ Transaction details retrieved:")
    print(f"  From: {tx_details.get('from', 'N/A')}")
    print(f"  To: {tx_details.get('to', 'N/A')}")
    print(f"  Block: {tx_details.get('block_number', 'N/A')}")

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
                print(f"  From wallet ID: {from_wallet_id}")

            if tx_details.get("to"):
                to_wallet_id = completer.process_wallet_address(tx_details["to"], conn)
                print(f"  To wallet ID: {to_wallet_id}")

            # 更新数据库中的交易记录
            if from_wallet_id is not None or to_wallet_id is not None:
                success = completer.update_transaction_by_hash(
                    tx_hash, from_wallet_id, to_wallet_id, conn
                )
                if success:
                    conn.commit()
                    print(f"✅ Successfully updated transaction in database")
                else:
                    conn.rollback()
                    print(f"❌ Failed to update transaction in database")
            else:
                print("⚠️  No wallet information to update")

        except Exception as e:
            conn.rollback()
            print(f"❌ Error updating transaction: {e}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="数据补齐程序 - 补充数据库中缺失的钱包信息",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 检查不完整的交易
  python cli_completer.py --check
  
  # 运行数据补齐（默认批处理大小100）
  python cli_completer.py --run
  
  # 运行数据补齐（批处理大小50）
  python cli_completer.py --run --batch-size 50
  
  # 测试单个交易
  python cli_completer.py --test-tx 0x1234567890abcdef...
  
  # 根据交易哈希更新交易
  python cli_completer.py --update-tx 0x1234567890abcdef...
  
  # 详细日志
  python cli_completer.py --run --verbose
  
  # 调试模式
  python cli_completer.py --run --debug
        """,
    )

    # 添加参数
    parser.add_argument("--check", action="store_true", help="检查不完整的交易数量")

    parser.add_argument("--run", action="store_true", help="运行数据补齐程序")

    parser.add_argument("--test-tx", type=str, metavar="HASH", help="测试处理单个交易")

    parser.add_argument(
        "--update-tx", type=str, metavar="HASH", help="根据交易哈希更新交易记录"
    )

    parser.add_argument(
        "--batch-size", type=int, default=100, help="批处理大小 (默认: 100)"
    )

    parser.add_argument("--verbose", "-v", action="store_true", help="详细日志输出")

    parser.add_argument(
        "--debug", "-d", action="store_true", help="调试模式（最详细的日志）"
    )

    parser.add_argument(
        "--dry-run", action="store_true", help="试运行模式（不实际更新数据库）"
    )

    # 解析参数
    args = parser.parse_args()

    # 设置日志
    setup_logging(verbose=args.verbose, debug=args.debug)

    # 检查是否提供了任何操作
    if not any([args.check, args.run, args.test_tx, args.update_tx]):
        parser.print_help()
        return

    try:
        # 加载配置
        config = load_config()

        # 创建数据补齐器
        completer = DataCompleter(config)

        # 执行相应的操作
        if args.check:
            check_incomplete_transactions(completer)

        elif args.test_tx:
            test_single_transaction(completer, args.test_tx)

        elif args.update_tx:
            update_transaction_by_hash(completer, args.update_tx)

        elif args.run:
            if args.dry_run:
                print("🔍 DRY RUN MODE - 不会实际更新数据库")
                check_incomplete_transactions(completer)
            else:
                print("🚀 开始运行数据补齐程序...")
                completer.run(batch_size=args.batch_size)
                print("✅ 数据补齐程序运行完成")

    except KeyboardInterrupt:
        print("\n⚠️  用户中断操作")
        sys.exit(1)
    except Exception as e:
        logger.error(f"程序执行失败: {e}", exc_info=True)
        print(f"❌ 错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
