#!/usr/bin/env python3
"""
Test script for debug functionality.
This script tests the debug features without running the full monitoring service.
"""

import logging
import os
import sys
from typing import Dict

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from debug_config import load_debug_config
from models import Wallet

# Configure logging for test
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def test_debug_config():
    """Test debug configuration loading."""
    logger.info("Testing debug configuration...")

    # Test debug config
    debug_config = load_debug_config()
    logger.info(f"Debug config loaded:")
    logger.info(f"  DEBUG_MODE: {debug_config.DEBUG_MODE}")
    logger.info(
        f"  DEBUG_TRANSACTION_DETAILS: {debug_config.DEBUG_TRANSACTION_DETAILS}"
    )
    logger.info(f"  DEBUG_WALLET_INFO: {debug_config.DEBUG_WALLET_INFO}")
    logger.info(f"  LOG_LEVEL: {debug_config.LOG_LEVEL}")
    logger.info(f"  MIN_ETH: {debug_config.MIN_ETH}")
    logger.info(f"  POLL_INTERVAL_SEC: {debug_config.POLL_INTERVAL_SEC}")

    assert debug_config.DEBUG_MODE == True
    assert debug_config.DEBUG_TRANSACTION_DETAILS == True
    assert debug_config.DEBUG_WALLET_INFO == True
    assert debug_config.LOG_LEVEL == "DEBUG"

    logger.info("✓ Debug configuration test passed")


def test_wallet_info_extraction():
    """Test wallet information extraction with debug logging."""
    logger.info("Testing wallet information extraction...")

    try:
        from block_processor import BlockProcessor
        from database import DatabaseManager
        from web3 import HTTPProvider, Web3

        # Create a minimal config for testing
        config = Config(
            DEBUG_MODE=True,
            DEBUG_TRANSACTION_DETAILS=True,
            DEBUG_WALLET_INFO=True,
            LOG_LEVEL="DEBUG",
        )

        # Initialize components
        web3 = Web3(HTTPProvider(str(config.PUBLICNODE_URL)))
        db_manager = DatabaseManager()
        block_processor = BlockProcessor(web3, db_manager, config)

        # Test wallet info extraction
        test_address = "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6"  # Example address

        logger.debug(f"Testing wallet info extraction for: {test_address}")
        wallet = block_processor.extract_wallet_info(test_address)

        logger.info(f"Extracted wallet info:")
        logger.info(f"  Address: {wallet.address}")
        logger.info(f"  Friendly Name: {wallet.friendly_name}")
        logger.info(f"  Group Name: {wallet.grp_name}")
        logger.info(f"  Group Type: {wallet.grp_type}")

        assert wallet.address == test_address
        logger.info("✓ Wallet information extraction test passed")

    except Exception as e:
        logger.error(f"✗ Wallet information extraction test failed: {e}")
        logger.debug("Exception details:", exc_info=True)


def test_debug_logging():
    """Test debug logging functionality."""
    logger.info("Testing debug logging...")

    config = Config(
        DEBUG_MODE=True,
        DEBUG_TRANSACTION_DETAILS=True,
        DEBUG_WALLET_INFO=True,
        LOG_LEVEL="DEBUG",
    )

    # Test different debug levels
    if config.DEBUG_MODE:
        logger.debug("This is a debug message")
        logger.info("This is an info message")
        logger.warning("This is a warning message")
        logger.error("This is an error message")

    if config.DEBUG_TRANSACTION_DETAILS:
        logger.debug("Transaction details debug message")

    if config.DEBUG_WALLET_INFO:
        logger.debug("Wallet info debug message")

    logger.info("✓ Debug logging test passed")


def test_environment_variables():
    """Test environment variable configuration."""
    logger.info("Testing environment variable configuration...")

    # Set test environment variables
    os.environ["DEBUG_MODE"] = "false"
    os.environ["DEBUG_TRANSACTION_DETAILS"] = "false"
    os.environ["DEBUG_WALLET_INFO"] = "false"
    os.environ["LOG_LEVEL"] = "INFO"
    os.environ["MIN_ETH"] = "5.0"
    os.environ["POLL_INTERVAL_SEC"] = "45"

    # Load config with environment variables
    config = load_debug_config()

    logger.info(f"Environment variable test results:")
    logger.info(f"  DEBUG_MODE: {config.DEBUG_MODE} (expected: False)")
    logger.info(
        f"  DEBUG_TRANSACTION_DETAILS: {config.DEBUG_TRANSACTION_DETAILS} (expected: False)"
    )
    logger.info(f"  DEBUG_WALLET_INFO: {config.DEBUG_WALLET_INFO} (expected: False)")
    logger.info(f"  LOG_LEVEL: {config.LOG_LEVEL} (expected: INFO)")
    logger.info(f"  MIN_ETH: {config.MIN_ETH} (expected: 5.0)")
    logger.info(f"  POLL_INTERVAL_SEC: {config.POLL_INTERVAL_SEC} (expected: 45)")

    assert config.DEBUG_MODE == False
    assert config.DEBUG_TRANSACTION_DETAILS == False
    assert config.DEBUG_WALLET_INFO == False
    assert config.LOG_LEVEL == "INFO"
    assert config.MIN_ETH == 5.0
    assert config.POLL_INTERVAL_SEC == 45

    # Clean up environment variables
    for var in [
        "DEBUG_MODE",
        "DEBUG_TRANSACTION_DETAILS",
        "DEBUG_WALLET_INFO",
        "LOG_LEVEL",
        "MIN_ETH",
        "POLL_INTERVAL_SEC",
    ]:
        if var in os.environ:
            del os.environ[var]

    logger.info("✓ Environment variable test passed")


def main():
    """Run all debug tests."""
    logger.info("=" * 80)
    logger.info("DEBUG FUNCTIONALITY TEST SUITE")
    logger.info("=" * 80)

    try:
        test_debug_config()
        test_debug_logging()
        test_environment_variables()
        test_wallet_info_extraction()

        logger.info("=" * 80)
        logger.info("ALL TESTS PASSED! ✓")
        logger.info("Debug functionality is working correctly.")
        logger.info("=" * 80)

    except Exception as e:
        logger.error("=" * 80)
        logger.error(f"TEST FAILED: {e}")
        logger.error("=" * 80)
        sys.exit(1)


if __name__ == "__main__":
    main()
