"""
Main entry point for wallet monitoring service.
"""

import logging
import time
from typing import Optional

from block_processor import BlockProcessor
from config import Config, load_config
from database import DatabaseManager
from web3 import HTTPProvider, Web3

# Configure logging - will be updated with config values
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class WalletMonitor:
    """Main wallet monitoring service."""

    def __init__(self, config: Config):
        self.config = config
        # Update logging level based on config
        logging.getLogger().setLevel(getattr(logging, config.LOG_LEVEL))
        logger.info(f"Logging level set to: {config.LOG_LEVEL}")
        logger.info(f"Debug mode: {config.DEBUG_MODE}")
        self.web3 = Web3(HTTPProvider(str(config.PUBLICNODE_URL)))

        # self.web3 = Web3(
        #     HTTPProvider(
        #         str("https://ethereum.publicnode.com"),
        #         request_kwargs={
        #             "proxies": {
        #                 "http": "socks5h://tor:9050",
        #                 "https": "socks5h://tor:9050",
        #             }
        #         },
        #     )
        # )
        self.db_manager = DatabaseManager()
        self.block_processor = BlockProcessor(self.web3, self.db_manager, config)

    def get_watch_addresses(
        self, group_name: Optional[str] = None, all_addresses: bool = False
    ):
        """Get watch addresses from database."""
        try:
            logger.debug("Fetching watch addresses from database...")
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

                if self.config.DEBUG_MODE:
                    for addr, wallet in wallets.items():
                        logger.debug(
                            f"Watch address: {addr} -> {wallet.friendly_name} ({wallet.grp_name})"
                        )

                logger.info(
                    f"Found {len(wallets)} watch addresses for group '{group_name}'"
                )
                return wallets

        except Exception as e:
            logger.error(f"Error getting watch addresses: {e}", exc_info=True)
            return {}

    def run_monitoring_cycle(self, group_name: Optional[str] = None):
        """Run a single monitoring cycle."""
        try:
            logger.info("=" * 80)
            logger.info("Starting monitoring cycle")
            logger.info("=" * 80)

            # Get watch addresses
            logger.debug("Step 1: Getting watch addresses...")
            watch_addresses = self.get_watch_addresses(group_name)
            full_addresses = self.get_watch_addresses(
                group_name=None, all_addresses=True
            )
            if not watch_addresses:
                logger.warning("No watch addresses found, skipping cycle")
                return

            # Get recent blocks
            logger.debug("Step 2: Fetching recent blocks...")
            blocks = self.block_processor.get_recent_blocks(minutes=10)
            if not blocks:
                logger.warning("No recent blocks found")
                return

            logger.debug(f"Found {len(blocks)} blocks to process")
            for block in blocks:
                logger.debug(
                    f"  Block {block.number}: {len(block.transactions)} transactions"
                )

            # Process blocks and extract transactions
            logger.debug("Step 3: Processing blocks and extracting transactions...")
            transactions = self.block_processor.process_blocks(
                blocks, self.config.MIN_ETH, watch_addresses, full_addresses
            )

            # Store data in database
            if transactions:
                logger.debug("Step 4: Storing data in database...")
                logger.info(f"Storing {len(transactions)} transactions")
                self.db_manager.store_all_data(transactions)
                logger.debug("Data storage completed")
            else:
                logger.info("No transactions to store")

            logger.info("Monitoring cycle completed successfully")
            logger.info("=" * 80)

        except Exception as e:
            logger.error(f"Error in monitoring cycle: {e}", exc_info=True)

    def run(self, group_name: Optional[str] = None):
        """Run the monitoring service continuously."""
        logger.info("Starting wallet monitoring service")
        logger.info(
            f"Configuration: min_eth={self.config.MIN_ETH} ETH, "
            f"poll_interval={self.config.POLL_INTERVAL_SEC}s, group={group_name}"
        )
        logger.info(f"Debug mode: {self.config.DEBUG_MODE}")
        logger.info(
            f"Debug transaction details: {self.config.DEBUG_TRANSACTION_DETAILS}"
        )
        logger.info(f"Debug wallet info: {self.config.DEBUG_WALLET_INFO}")

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
    """Main entry point."""
    config = load_config()
    monitor = WalletMonitor(config)
    monitor.run()


if __name__ == "__main__":
    main()
