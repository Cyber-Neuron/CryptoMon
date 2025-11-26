"""
Refactored main orchestration for wallet monitoring service.
"""

import logging
import time
from typing import Optional

from block_processor import BlockProcessor
from config import load_config
from database import DatabaseManager
from web3 import HTTPProvider, Web3

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class WalletMonitor:
    """Main wallet monitoring service."""

    def __init__(self, config):
        self.config = config
        self.web3 = Web3(HTTPProvider(str(config.PUBLICNODE_URL)))
        self.db_manager = DatabaseManager()
        self.block_processor = BlockProcessor(self.web3, self.db_manager)

    def get_watch_addresses(
        self, group_name: Optional[str] = None, all_addresses: bool = False
    ):
        """Get watch addresses from database."""
        try:
            with self.db_manager.get_connection() as conn:
                wallets = self.db_manager.get_hot_wallets(conn, all_addresses)

                if group_name:
                    # Filter by group name
                    filtered_wallets = {
                        addr: wallet
                        for addr, wallet in wallets.items()
                        if wallet.grp_name == group_name
                    }
                    wallets = filtered_wallets

                logger.info(
                    f"Found {len(wallets)} watch addresses for group '{group_name}'"
                )
                return wallets

        except Exception as e:
            logger.error(f"Error getting watch addresses: {e}")
            return {}

    def run_monitoring_cycle(self, group_name: Optional[str] = None):
        """Run a single monitoring cycle."""
        try:
            logger.info("Starting monitoring cycle")

            # Get watch addresses
            watch_addresses = self.get_watch_addresses(group_name)
            if not watch_addresses:
                logger.warning("No watch addresses found, skipping cycle")
                return

            # Get recent blocks
            logger.info("Fetching recent blocks")
            blocks = self.block_processor.get_recent_blocks(minutes=10)
            if not blocks:
                logger.warning("No recent blocks found")
                return

            # Process blocks and extract transactions
            logger.info("Processing blocks and extracting transactions")
            transactions = self.block_processor.process_blocks(
                blocks, self.config.MIN_ETH, watch_addresses
            )

            # Store data in database
            if transactions:
                logger.info(f"Storing {len(transactions)} transactions")
                self.db_manager.store_all_data(transactions)
            else:
                logger.info("No transactions to store")

            logger.info("Monitoring cycle completed successfully")

        except Exception as e:
            logger.error(f"Error in monitoring cycle: {e}", exc_info=True)

    def run(self, group_name: Optional[str] = None):
        """Run the monitoring service continuously."""
        logger.info("Starting wallet monitoring service")
        logger.info(
            f"Configuration: min_eth={self.config.MIN_ETH} ETH, "
            f"poll_interval={self.config.POLL_INTERVAL_SEC}s, group={group_name}"
        )

        while True:
            try:
                self.run_monitoring_cycle(group_name)
            except KeyboardInterrupt:
                logger.info("Received interrupt signal, shutting down")
                break
            except Exception as e:
                logger.error(f"Unexpected error: {e}", exc_info=True)

            time.sleep(self.config.POLL_INTERVAL_SEC)


def main():
    """Main entry point."""
    config = load_config()
    monitor = WalletMonitor(config)
    monitor.run()


if __name__ == "__main__":
    main()
