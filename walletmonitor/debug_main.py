"""
Debug main entry point for wallet monitoring service.
This version provides maximum debug information for transaction monitoring.
"""

import logging
import time
from typing import Optional

from block_processor import BlockProcessor
from database import DatabaseManager
from debug_config import load_debug_config
from web3 import HTTPProvider, Web3

# Configure logging for maximum detail
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("debug.log", mode="w"),  # Also log to file
    ],
)
logger = logging.getLogger(__name__)


class DebugWalletMonitor:
    """Debug version of wallet monitoring service with maximum detail."""

    def __init__(self, config):
        self.config = config
        # Update logging level based on config
        logging.getLogger().setLevel(getattr(logging, config.LOG_LEVEL))
        logger.info("=" * 100)
        logger.info("DEBUG WALLET MONITOR STARTING")
        logger.info("=" * 100)
        logger.info(f"Logging level: {config.LOG_LEVEL}")
        logger.info(f"Debug mode: {config.DEBUG_MODE}")
        logger.info(f"Debug transaction details: {config.DEBUG_TRANSACTION_DETAILS}")
        logger.info(f"Debug wallet info: {config.DEBUG_WALLET_INFO}")
        logger.info(f"Minimum ETH threshold: {config.MIN_ETH}")
        logger.info(f"Poll interval: {config.POLL_INTERVAL_SEC} seconds")
        logger.info("=" * 100)

        self.web3 = Web3(HTTPProvider(str(config.PUBLICNODE_URL)))
        self.db_manager = DatabaseManager()
        self.block_processor = BlockProcessor(self.web3, self.db_manager, config)

    def get_watch_addresses(
        self, group_name: Optional[str] = None, all_addresses: bool = False
    ):
        """Get watch addresses from database with detailed logging."""
        try:
            logger.debug("=" * 60)
            logger.debug("FETCHING WATCH ADDRESSES")
            logger.debug("=" * 60)

            with self.db_manager.get_connection() as conn:
                wallets = self.db_manager.get_hot_wallets(conn, all_addresses)
                logger.debug(f"Retrieved {len(wallets)} total wallets from database")

                if group_name:
                    # Filter by group name
                    filtered_wallets = {
                        addr: wallet
                        for addr, wallet in wallets.items()
                        if wallet.grp_name == group_name
                    }
                    wallets = filtered_wallets
                    logger.debug(
                        f"Filtered to {len(wallets)} wallets for group '{group_name}'"
                    )

                # Always show watch addresses in debug mode
                logger.debug("WATCH ADDRESSES:")
                for addr, wallet in wallets.items():
                    logger.debug(
                        f"  {addr} -> {wallet.friendly_name} ({wallet.grp_name})"
                    )

                logger.info(
                    f"Found {len(wallets)} watch addresses for group '{group_name}'"
                )
                logger.debug("=" * 60)
                return wallets

        except Exception as e:
            logger.error(f"Error getting watch addresses: {e}", exc_info=True)
            return {}

    def run_monitoring_cycle(self, group_name: Optional[str] = None):
        """Run a single monitoring cycle with maximum debug detail."""
        try:
            logger.info("=" * 100)
            logger.info("STARTING MONITORING CYCLE")
            logger.info("=" * 100)

            # Step 1: Get watch addresses
            logger.debug("STEP 1: Getting watch addresses...")
            watch_addresses = self.get_watch_addresses(group_name)
            if not watch_addresses:
                logger.warning("No watch addresses found, skipping cycle")
                return

            # Step 2: Get recent blocks
            logger.debug("STEP 2: Fetching recent blocks...")
            blocks = self.block_processor.get_recent_blocks(minutes=10)
            if not blocks:
                logger.warning("No recent blocks found")
                return

            logger.debug(f"Found {len(blocks)} blocks to process")
            total_transactions = sum(len(block.transactions) for block in blocks)
            logger.debug(f"Total transactions to check: {total_transactions}")

            # Step 3: Process blocks and extract transactions
            logger.debug("STEP 3: Processing blocks and extracting transactions...")
            transactions = self.block_processor.process_blocks(
                blocks, self.config.MIN_ETH, watch_addresses
            )

            # Step 4: Store data in database
            if transactions:
                logger.debug("STEP 4: Storing data in database...")
                logger.info(f"Storing {len(transactions)} transactions")
                self.db_manager.store_all_data(transactions)
                logger.debug("Data storage completed")
            else:
                logger.info("No transactions to store")

            logger.info("Monitoring cycle completed successfully")
            logger.info("=" * 100)

        except Exception as e:
            logger.error(f"Error in monitoring cycle: {e}", exc_info=True)

    def run(self, group_name: Optional[str] = None):
        """Run the monitoring service continuously with debug information."""
        logger.info("Starting DEBUG wallet monitoring service")
        logger.info(
            f"Configuration: min_eth={self.config.MIN_ETH} ETH, "
            f"poll_interval={self.config.POLL_INTERVAL_SEC}s, group={group_name}"
        )

        cycle_count = 0
        while True:
            try:
                cycle_count += 1
                logger.info(f"Starting monitoring cycle #{cycle_count}")
                self.run_monitoring_cycle(group_name)
            except KeyboardInterrupt:
                logger.info("Received interrupt signal, shutting down")
                break
            except Exception as e:
                logger.error(
                    f"Unexpected error in cycle #{cycle_count}: {e}", exc_info=True
                )

            logger.debug(
                f"Waiting {self.config.POLL_INTERVAL_SEC} seconds before next cycle..."
            )
            time.sleep(self.config.POLL_INTERVAL_SEC)


def main():
    """Debug main entry point."""
    config = load_debug_config()
    monitor = DebugWalletMonitor(config)
    monitor.run()


if __name__ == "__main__":
    main()
