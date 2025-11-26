#!/usr/bin/env python3
"""
测试wallet_type功能的脚本
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from walletmonitor.database import DatabaseManager
from walletmonitor.models import Wallet


def test_wallet_type_functionality():
    """测试wallet_type功能"""
    db_manager = DatabaseManager()

    print("=== 测试wallet_type功能 ===")

    # 测试determine_wallet_type方法
    print("\n1. 测试determine_wallet_type方法:")
    test_cases = [
        ("Cold Storage Wallet", "cold"),
        ("Hot Trading Wallet", "hot"),
        ("Deposit Address", "deposit"),
        ("Internal Transfer", "internal"),
        ("Regular User Wallet", "regular"),
        ("Some Random Name", "regular"),
        (None, "regular"),
    ]

    for friendly_name, expected_type in test_cases:
        actual_type = db_manager.determine_wallet_type(friendly_name)
        status = "✓" if actual_type == expected_type else "✗"
        print(f"  {status} '{friendly_name}' -> {actual_type} (期望: {expected_type})")

    # 测试创建钱包
    print("\n2. 测试创建钱包:")
    test_wallets = [
        Wallet(
            address="0x1234567890123456789012345678901234567890",
            friendly_name="Cold Storage Wallet",
        ),
        Wallet(
            address="0x2345678901234567890123456789012345678901",
            friendly_name="Hot Trading Wallet",
        ),
        Wallet(
            address="0x3456789012345678901234567890123456789012",
            friendly_name="Deposit Address",
        ),
        Wallet(
            address="0x4567890123456789012345678901234567890123",
            friendly_name="Regular Wallet",
        ),
    ]

    try:
        with db_manager.get_connection() as conn:
            for wallet in test_wallets:
                wallet_id = db_manager.get_or_create_wallet(conn, wallet)
                print(
                    f"  ✓ 创建钱包: {wallet.address[:10]}... -> ID: {wallet_id}, Type: {wallet.wallet_type}"
                )

            # 测试批量获取钱包
            print("\n3. 测试批量获取钱包:")
            addresses = [w.address for w in test_wallets]
            wallets = db_manager.get_wallets_batch(conn, addresses)

            for addr, wallet in wallets.items():
                print(f"  ✓ 获取钱包: {addr[:10]}... -> Type: {wallet.wallet_type}")

            # 测试获取热钱包
            print("\n4. 测试获取热钱包:")
            hot_wallets = db_manager.get_hot_wallets(conn, all_addresses=True)
            print(f"  ✓ 获取到 {len(hot_wallets)} 个钱包")

            for addr, wallet in list(hot_wallets.items())[:3]:  # 只显示前3个
                print(f"    - {addr[:10]}... -> Type: {wallet.wallet_type}")

    except Exception as e:
        print(f"  ✗ 数据库操作失败: {e}")

    print("\n=== 测试完成 ===")


if __name__ == "__main__":
    test_wallet_type_functionality()
