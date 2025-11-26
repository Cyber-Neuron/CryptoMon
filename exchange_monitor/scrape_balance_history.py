import json
import logging
import os
import time
from datetime import UTC, datetime
from typing import Dict, Optional, Tuple

import httpx
from config import (
    BLOCKSCOUT_BASE_URL,
    MIN_ETH_DELTA,
    TOR_PROXY_HOST,
    TOR_PROXY_PORT,
)
from db_utils import (
    get_db_connection,
    get_or_create_chain,
    get_or_create_token,
    get_or_create_wallet,
    store_transactions,
)
from dotenv import load_dotenv
from psycopg2.extras import DictCursor, Json

from blockscout_client import Client
from blockscout_client.api.addresses import get_address_coin_balance_history
from blockscout_client.api.transactions import get_tx
from blockscout_client.models import (
    GetAddressCoinBalanceHistoryResponse200,
    Transaction,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize clients with Tor proxy
proxy_url = f"socks5h://{TOR_PROXY_HOST}:{TOR_PROXY_PORT}"
httpx_args = {"proxy": proxy_url}

# Initialize clients
blockscout = Client(base_url=BLOCKSCOUT_BASE_URL, httpx_args=httpx_args)


def check_delta(delta: str) -> bool:
    """Check if the delta value meets the minimum threshold.

    Args:
        delta: Delta value in wei

    Returns:
        bool: True if delta meets threshold, False otherwise
    """
    delta_wei = int(delta)
    delta_eth = delta_wei / 1e18
    return abs(delta_eth) >= MIN_ETH_DELTA


def process_transaction_wallets(
    cur, transaction_hash: str, tx_info: Transaction
) -> Tuple[Optional[int], Optional[int]]:
    """Process transaction-related wallets.

    Args:
        cur: Database cursor
        transaction_hash: Transaction hash
        tx_info: Transaction information

    Returns:
        Tuple[Optional[int], Optional[int]]: (from_wallet_id, to_wallet_id)
    """
    try:
        from_address = tx_info.from_.hash_
        to_address = tx_info.to.hash_

        if not from_address or not to_address:
            logger.error(f"Missing from/to addresses in transaction {transaction_hash}")
            return None, None

        from_wallet_id = get_or_create_wallet(cur, from_address)
        to_wallet_id = get_or_create_wallet(cur, to_address)

        return from_wallet_id, to_wallet_id
    except Exception as e:
        logger.error(
            f"Error processing transaction wallets for {transaction_hash}: {e}"
        )
        return None, None


def store_transaction_history(
    cur,
    address: str,
    history: GetAddressCoinBalanceHistoryResponse200,
) -> None:
    """Store transaction history.

    Args:
        cur: Database cursor
        address: Wallet address
        history: Balance history records
    """
    transactions_to_store = []

    for record in history.items:
        try:
            if not check_delta(record.delta):
                continue

            # Type checking for transaction hash
            if not isinstance(record.transaction_hash, str):
                logger.error(
                    f"Invalid transaction hash type for {record.transaction_hash}"
                )
                continue

            # Check if transaction exists
            cur.execute(
                "SELECT 1 FROM transactions WHERE tx_hash = %s",
                (record.transaction_hash,),
            )
            if cur.fetchone():
                logger.info(
                    f"Transaction {record.transaction_hash} already exists, skipping"
                )
                continue

            tx_details = get_tx.sync(
                client=blockscout,
                transaction_hash=record.transaction_hash,
            )
            if not tx_details:
                logger.error(
                    f"Failed to get transaction details for {record.transaction_hash}"
                )
                continue

            logger.info(
                f"Processing transaction {record.transaction_hash}, with value of {int(record.delta)/1e18} ETH"
            )

            usd_value = None
            if tx_details.exchange_rate:
                delta_eth = int(record.delta) / 1e18
                try:
                    usd_value = delta_eth * float(tx_details.exchange_rate)
                except (ValueError, TypeError) as e:
                    logger.error(f"Error calculating USD value: {e}")

            # Prepare transaction data
            transaction_data = {
                "hash": record.transaction_hash,
                "from": tx_details.from_.hash_,
                "to": tx_details.to.hash_,
                "token": "ETH",
                "block_number": record.block_number,
                "amount": record.delta,
                "timestamp": record.block_timestamp,
                "usd_value": usd_value,
                "raw_data": record.to_dict(),
            }

            transactions_to_store.append(transaction_data)

        except Exception as e:
            logger.error(f"Error processing transaction {record.transaction_hash}: {e}")
            continue

    # Store all transactions in batch
    if transactions_to_store:
        try:
            store_transactions(cur, transactions_to_store)
        except Exception as e:
            logger.error(f"Error storing transactions batch: {e}")


class BalanceHistoryScraper:
    def __init__(self, base_url, address, initial_block):
        self.base_url = base_url
        self.address = address
        self.current_block = initial_block
        self.client = httpx.Client(proxy=proxy_url)

    def fetch_page(self):
        url = f"{self.base_url}/addresses/{self.address}/coin-balance-history"
        params = {"block_number": self.current_block}
        logger.info(f"Fetching page {self.current_block} from {url}: {params}")
        try:
            response = self.client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            logger.error(f"Error fetching data: {e}")
            return None

    def scrape(self, max_pages=None):
        page_num = 1

        while True:
            logger.info(f"Fetching page {page_num} (block: {self.current_block})")
            data = self.fetch_page()

            if not data or "items" not in data:
                logger.info("No more data or error occurred")
                break

            # Convert the response to GetAddressCoinBalanceHistoryResponse200
            history = GetAddressCoinBalanceHistoryResponse200.from_dict(data)

            # Store data in database
            with get_db_connection() as conn:
                with conn.cursor(cursor_factory=DictCursor) as cur:
                    store_transaction_history(cur, self.address, history)
                    conn.commit()

            # Check if there's a next page
            if "next_page_params" not in data:
                logger.info("No more pages available")
                break

            # Update the block number for next request
            self.current_block = data["next_page_params"]["block_number"]

            # Check if we've reached the maximum number of pages
            if max_pages and page_num >= max_pages:
                logger.info(f"Reached maximum page limit ({max_pages})")
                break

            # Add delay between requests (2 seconds)
            time.sleep(2)
            page_num += 1


def main():
    # Configuration
    base_url = "https://eth.blockscout.com/api/v2"
    address = "0x28C6c06298d514Db089934071355E5743bf21d60"
    initial_block = 22693230

    # Create scraper instance
    scraper = BalanceHistoryScraper(base_url, address, initial_block)

    # Start scraping (set max_pages to None for unlimited pages)
    scraper.scrape(max_pages=10000)  # Start with 10 pages for testing


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Scraping stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise
