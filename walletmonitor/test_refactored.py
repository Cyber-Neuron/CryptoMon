"""
Test script for refactored wallet monitoring system.
"""

import logging
from decimal import Decimal

from database import DatabaseManager
from models import ExFlow, Transaction, Wallet

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_models():
    """Test data models."""
    logger.info("Testing data models...")

    # Test Wallet model
    wallet = Wallet(
        address="0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6",
        friendly_name="Test Wallet",
        grp_type="Hot",
        grp_name="test_group",
    )
    logger.info(f"Created wallet: {wallet}")

    # Test Transaction model
    transaction = Transaction(
        hash="0x1234567890abcdef",
        block_number=12345,
        from_address="0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6",
        to_address="0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b7",
        amount=Decimal("10.5"),
        token="ETH",
        timestamp=1640995200,
        from_wallet=wallet,
        to_wallet=Wallet(address="0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b7"),
    )
    logger.info(f"Created transaction: {transaction}")

    # Test ExFlow model
    ex_flow = ExFlow.from_transaction(transaction)
    logger.info(f"Created ex_flow: {ex_flow}")

    # Test dictionary conversion
    wallet_dict = wallet.to_dict()
    transaction_dict = transaction.to_dict()
    ex_flow_dict = ex_flow.to_dict()

    logger.info(f"Wallet dict: {wallet_dict}")
    logger.info(f"Transaction dict: {transaction_dict}")
    logger.info(f"ExFlow dict: {ex_flow_dict}")

    logger.info("Data models test completed successfully!")


def test_database_manager():
    """Test database manager."""
    logger.info("Testing database manager...")

    try:
        db_manager = DatabaseManager()
        logger.info("Database manager created successfully")

        # Test connection
        with db_manager.get_connection() as conn:
            logger.info("Database connection successful")

            # Test getting hot wallets
            wallets = db_manager.get_hot_wallets(conn, all_addresses=True)
            logger.info(f"Found {len(wallets)} wallets in database")

    except Exception as e:
        logger.error(f"Database test failed: {e}")
        return False

    logger.info("Database manager test completed successfully!")
    return True


def test_model_conversions():
    """Test model conversions from dictionaries."""
    logger.info("Testing model conversions...")

    # Test Wallet from dict
    wallet_data = {
        "address": "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6",
        "friendly_name": "Test Wallet",
        "grp_type": "Hot",
        "grp_name": "test_group",
    }
    wallet = Wallet.from_dict(wallet_data)
    logger.info(f"Wallet from dict: {wallet}")

    # Test Transaction from dict
    transaction_data = {
        "hash": "0x1234567890abcdef",
        "block_number": 12345,
        "from": "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6",
        "to": "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b7",
        "amount": 10.5,
        "token": "ETH",
        "timestamp": 1640995200,
        "usd_value": 21000.0,
    }
    transaction = Transaction.from_dict(transaction_data)
    logger.info(f"Transaction from dict: {transaction}")

    # Test ExFlow from dict
    ex_flow_data = {
        "timestamp": 1640995200,
        "token": "ETH",
        "from_grp_name": "test_group",
        "to_grp_name": "another_group",
        "amount": 10.5,
        "usd_value": 21000.0,
        "tx_hash": "0x1234567890abcdef",
    }
    ex_flow = ExFlow.from_dict(ex_flow_data)
    logger.info(f"ExFlow from dict: {ex_flow}")

    logger.info("Model conversions test completed successfully!")


def main():
    """Run all tests."""
    logger.info("Starting refactored code tests...")

    # Test data models
    test_models()

    # Test model conversions
    test_model_conversions()

    # Test database manager (requires database connection)
    test_database_manager()

    logger.info("All tests completed!")


if __name__ == "__main__":
    main()
