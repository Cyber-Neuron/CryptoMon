"""
Main orchestration for wallet monitoring service.
"""

import logging
import time
from typing import Optional

from config import load_config
from db import store_flows, upsert_transactions
from db_utils import get_db_connection, get_hot_wallets
from extractor import extract_transactions
from fetcher import get_recent_blocks
from web3 import HTTPProvider, Web3

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def wei_to_eth(wei: int) -> float:
    """Convert WEI to ETH."""
    return wei / 1e18


def eth_to_wei(eth: float) -> int:
    """Convert ETH to WEI."""
    return int(eth * 1e18)


def get_watch_addresses(base: Optional[str] = None, all_addresses=False):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            rows = get_hot_wallets(cur, all_addresses)
            if base is None:
                # addresses = set(row[0].lower() for row in rows)
                addresses = {
                    row[0]: {"grp_name": row[1], "friendly_name": row[2]}
                    for row in rows
                }
            else:
                # addresses = set(row[0].lower() for row in rows if row[1] == base)
                addresses = {
                    row[0]: {"grp_name": row[1], "friendly_name": row[2]}
                    for row in rows
                    if row[1] == base
                }

            logger.info(
                f"Found {len(addresses)} hot wallet addresses for group '{base}'"
            )

            return addresses


def main():
    logger.info("Starting wallet monitoring service")
    config = load_config()
    w3 = Web3(HTTPProvider(str(config.PUBLICNODE_URL)))
    min_eth = config.MIN_ETH
    poll_interval = config.POLL_INTERVAL_SEC
    group_name = None  # "binance"  # Or make this configurable

    logger.info(
        f"Configuration: min_eth={min_eth} ETH, poll_interval={poll_interval}s, group={group_name}"
    )

    while True:
        try:
            logger.info("Starting monitoring cycle")

            # Get watch addresses
            watch_addresses = get_watch_addresses(group_name)
            full_addresses = get_watch_addresses(None, all_addresses=True)
            if not watch_addresses:
                logger.warning("No watch addresses found, skipping cycle")
                time.sleep(poll_interval)
                continue

            # Get recent blocks
            logger.info("Fetching recent blocks (last 10 minutes)")

            txs = extract_transactions(
                w3,
                minutes=10,
                watch_addresses=watch_addresses,
                min_eth=min_eth,
                full_addresses=full_addresses,
            )
            logger.info(f"Extracted {len(txs)} total transactions")

            logger.info(
                f"Monitoring cycle completed, sleeping for {poll_interval} seconds"
            )

        except Exception as e:
            logger.error(f"Error in monitor loop: {e}", exc_info=True)
        time.sleep(poll_interval)


if __name__ == "__main__":
    main()
