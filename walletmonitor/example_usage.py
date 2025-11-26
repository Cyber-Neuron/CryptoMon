"""
数据补齐程序使用示例
"""

import logging

from config import load_config
from data_completer import DataCompleter

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def example_basic_usage():
    """基本使用示例"""
    print("=== 基本使用示例 ===")

    try:
        # 加载配置
        config = load_config()

        # 创建数据补齐器
        completer = DataCompleter(config)

        # 检查不完整的交易
        incomplete_transactions = completer.get_incomplete_transactions()
        print(f"发现 {len(incomplete_transactions)} 个不完整的交易")

        if incomplete_transactions:
            # 处理前5个交易作为示例
            sample_transactions = incomplete_transactions[:5]
            print(f"处理前 {len(sample_transactions)} 个交易作为示例...")

            for tx_id, tx_hash in sample_transactions:
                print(f"\n处理交易 {tx_id}: {tx_hash}")

                # 获取交易详情
                tx_details = completer.get_transaction_details(tx_hash)
                if tx_details:
                    print(f"  发送方: {tx_details.get('from', 'N/A')}")
                    print(f"  接收方: {tx_details.get('to', 'N/A')}")

                    # 处理钱包地址
                    if tx_details.get("from"):
                        from_wallet_id = completer.process_wallet_address(
                            tx_details["from"]
                        )
                        print(f"  发送方钱包ID: {from_wallet_id}")

                    if tx_details.get("to"):
                        to_wallet_id = completer.process_wallet_address(
                            tx_details["to"]
                        )
                        print(f"  接收方钱包ID: {to_wallet_id}")
                else:
                    print("  无法获取交易详情")

        print("\n基本使用示例完成")

    except Exception as e:
        logger.error(f"基本使用示例失败: {e}")
        print(f"错误: {e}")


def example_batch_processing():
    """批量处理示例"""
    print("\n=== 批量处理示例 ===")

    try:
        # 加载配置
        config = load_config()

        # 创建数据补齐器
        completer = DataCompleter(config)

        # 运行批量处理（小批量用于演示）
        print("开始批量处理...")
        completer.run(batch_size=10)

        print("批量处理示例完成")

    except Exception as e:
        logger.error(f"批量处理示例失败: {e}")
        print(f"错误: {e}")


def example_single_transaction():
    """单个交易处理示例"""
    print("\n=== 单个交易处理示例 ===")

    # 示例交易哈希（需要替换为实际的交易哈希）
    example_tx_hash = (
        "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    )

    try:
        # 加载配置
        config = load_config()

        # 创建数据补齐器
        completer = DataCompleter(config)

        print(f"测试处理交易: {example_tx_hash}")

        # 获取交易详情
        tx_details = completer.get_transaction_details(example_tx_hash)
        if tx_details:
            print("交易详情:")
            print(f"  发送方: {tx_details.get('from', 'N/A')}")
            print(f"  接收方: {tx_details.get('to', 'N/A')}")
            print(f"  区块号: {tx_details.get('block_number', 'N/A')}")
            print(f"  交易哈希: {tx_details.get('hash', 'N/A')}")

            # 处理钱包地址
            if tx_details.get("from"):
                from_wallet_id = completer.process_wallet_address(tx_details["from"])
                print(f"  发送方钱包ID: {from_wallet_id}")

            if tx_details.get("to"):
                to_wallet_id = completer.process_wallet_address(tx_details["to"])
                print(f"  接收方钱包ID: {to_wallet_id}")
        else:
            print("无法获取交易详情（可能是无效的交易哈希）")

        print("单个交易处理示例完成")

    except Exception as e:
        logger.error(f"单个交易处理示例失败: {e}")
        print(f"错误: {e}")


def example_error_handling():
    """错误处理示例"""
    print("\n=== 错误处理示例 ===")

    try:
        # 加载配置
        config = load_config()

        # 创建数据补齐器
        completer = DataCompleter(config)

        # 测试无效的交易哈希
        invalid_tx_hash = "0xinvalid"
        print(f"测试无效交易哈希: {invalid_tx_hash}")

        tx_details = completer.get_transaction_details(invalid_tx_hash)
        if tx_details:
            print("意外：获取到了交易详情")
        else:
            print("正确：无法获取无效交易的详情")

        # 测试无效的钱包地址
        invalid_address = "0xinvalid"
        print(f"测试无效钱包地址: {invalid_address}")

        wallet_id = completer.process_wallet_address(invalid_address)
        print(f"钱包ID: {wallet_id}")

        print("错误处理示例完成")

    except Exception as e:
        logger.error(f"错误处理示例失败: {e}")
        print(f"错误: {e}")


def main():
    """主函数 - 运行所有示例"""
    print("数据补齐程序使用示例")
    print("=" * 50)

    # 运行各种示例
    example_basic_usage()
    example_batch_processing()
    example_single_transaction()
    example_error_handling()

    print("\n" + "=" * 50)
    print("所有示例运行完成")
    print("\n提示:")
    print("1. 使用 'python cli_completer.py --check' 检查不完整的交易")
    print("2. 使用 'python cli_completer.py --run' 运行完整的数据补齐")
    print("3. 使用 'python cli_completer.py --test-tx <hash>' 测试单个交易")
    print("4. 查看 README_data_completer.md 获取详细使用说明")


if __name__ == "__main__":
    main()
