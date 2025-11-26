"""
Configuration for wallet monitoring system.
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """Configuration class for wallet monitoring."""

    # Database configuration
    DATABASE_URL: str = (
        "postgresql://user:password@postgres:5432/walletmonitor"
    )

    # Ethereum node configuration
    PUBLICNODE_URL: str = (
        "https://ethereum-rpc.publicnode.com"  # Replace with your API key
    )

    # Monitoring configuration
    MIN_ETH: float = 100.0  # Minimum ETH amount to monitor
    POLL_INTERVAL_SEC: int = 120  # Polling interval in seconds

    # Arkham API configuration
    ARKHAM_API_KEY: Optional[str] = None  # Optional: Add your Arkham API key

    # Logging configuration
    LOG_LEVEL: str = "INFO"  # Changed to DEBUG for detailed logging
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Debug configuration
    DEBUG_MODE: bool = False  # Enable detailed debug information
    DEBUG_TRANSACTION_DETAILS: bool = False  # Show detailed transaction processing info
    DEBUG_WALLET_INFO: bool = False  # Show wallet information extraction details


def load_config() -> Config:
    """Load configuration from environment variables or use defaults."""
    return Config(
        DATABASE_URL=os.getenv("DATABASE_URL", Config.DATABASE_URL),
        PUBLICNODE_URL=os.getenv("PUBLICNODE_URL", Config.PUBLICNODE_URL),
        MIN_ETH=float(os.getenv("MIN_ETH", Config.MIN_ETH)),
        POLL_INTERVAL_SEC=int(os.getenv("POLL_INTERVAL_SEC", Config.POLL_INTERVAL_SEC)),
        ARKHAM_API_KEY=os.getenv("ARKHAM_API_KEY", Config.ARKHAM_API_KEY),
        LOG_LEVEL=os.getenv("LOG_LEVEL", Config.LOG_LEVEL),
        LOG_FORMAT=os.getenv("LOG_FORMAT", Config.LOG_FORMAT),
        DEBUG_MODE=os.getenv("DEBUG_MODE", "true").lower() == "true",
        DEBUG_TRANSACTION_DETAILS=os.getenv("DEBUG_TRANSACTION_DETAILS", "true").lower()
        == "true",
        DEBUG_WALLET_INFO=os.getenv("DEBUG_WALLET_INFO", "true").lower() == "true",
    )


# Export for backward compatibility
DATABASE_URL = Config.DATABASE_URL
