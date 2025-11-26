"""
Debug configuration for wallet monitoring system.
This file contains settings optimized for detailed debugging and transaction monitoring.
"""

import os

from config import Config


class DebugConfig(Config):
    """Debug configuration with all debug options enabled."""

    # Debug configuration - all enabled for maximum detail
    DEBUG_MODE: bool = True
    DEBUG_TRANSACTION_DETAILS: bool = True
    DEBUG_WALLET_INFO: bool = True

    # Logging configuration - set to DEBUG level
    LOG_LEVEL: str = "DEBUG"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Monitoring configuration - reduced for faster testing
    MIN_ETH: float = 1.0  # Lower threshold to see more transactions
    POLL_INTERVAL_SEC: int = 30  # Shorter interval for faster feedback


def load_debug_config() -> DebugConfig:
    """Load debug configuration with environment variable overrides."""
    return DebugConfig(
        DATABASE_URL=os.getenv("DATABASE_URL", DebugConfig.DATABASE_URL),
        PUBLICNODE_URL=os.getenv("PUBLICNODE_URL", DebugConfig.PUBLICNODE_URL),
        MIN_ETH=float(os.getenv("MIN_ETH", DebugConfig.MIN_ETH)),
        POLL_INTERVAL_SEC=int(
            os.getenv("POLL_INTERVAL_SEC", DebugConfig.POLL_INTERVAL_SEC)
        ),
        ARKHAM_API_KEY=os.getenv("ARKHAM_API_KEY", DebugConfig.ARKHAM_API_KEY),
        LOG_LEVEL=os.getenv("LOG_LEVEL", DebugConfig.LOG_LEVEL),
        LOG_FORMAT=os.getenv("LOG_FORMAT", DebugConfig.LOG_FORMAT),
        DEBUG_MODE=os.getenv("DEBUG_MODE", "true").lower() == "true",
        DEBUG_TRANSACTION_DETAILS=os.getenv("DEBUG_TRANSACTION_DETAILS", "true").lower()
        == "true",
        DEBUG_WALLET_INFO=os.getenv("DEBUG_WALLET_INFO", "true").lower() == "true",
    )
