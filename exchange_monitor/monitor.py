import json
import logging
import time
from datetime import UTC, datetime
from typing import Dict, Optional, Tuple

from config import (
    BLOCKSCOUT_BASE_URL,
    ETH_ADDRESSES,
    MIN_ETH_DELTA,
    MONITOR_INTERVAL,
    TOR_PROXY_HOST,
    TOR_PROXY_PORT,
)
from db_utils import (
    get_db_connection,
    get_or_create_chain,
    get_or_create_token,
    get_or_create_wallet,
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

# # Validate required environment variables
# DATABASE_URL = os.getenv("DATABASE_URL")
# if not DATABASE_URL:
#     raise ValueError("DATABASE_URL must be set in .env file")

# # Exchange hot wallet addresses to monitor
# ETH_ADDRESSES: List[str] = [
#     "0x28C6c06298d514Db089934071355E5743bf21d60",  # Binance
#     "0x56Eddb7aa87536c09CCc2793473599fD21A8b17F",
#     # "0xdAC17F958D2ee523a2206206994597C13D831ec7",
# ]
# USDT_TOKEN = "0xdAC17F958D2ee523a2206206994597C13D831ec7"

# Initialize clients
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
    for record in history.items:
        try:
            if not check_delta(record.delta):
                continue

            wallet_id = get_or_create_wallet(cur, address)
            if not wallet_id:
                logger.error(f"Failed to get or create wallet for {address}")
                continue

            token_id = get_or_create_token(cur, "ETH")
            if not token_id:
                logger.error("Failed to get or create token for ETH")
                continue

            chain_id = get_or_create_chain(cur)
            if not chain_id:
                logger.error("Failed to get or create Ethereum chain")
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
            from_wallet_id, to_wallet_id = process_transaction_wallets(
                cur, record.transaction_hash, tx_details
            )
            if not from_wallet_id or not to_wallet_id:
                logger.error(
                    f"Skipping transaction {record.transaction_hash} due to missing wallet info"
                )
                continue

            usd_value = None
            if tx_details.exchange_rate:
                delta_eth = int(record.delta) / 1e18
                try:
                    usd_value = delta_eth * float(tx_details.exchange_rate)
                except (ValueError, TypeError) as e:
                    logger.error(f"Error calculating USD value: {e}")

            # Insert transaction record
            cur.execute(
                """
                INSERT INTO transactions (
                    tx_hash, chain_id, block_height, from_wallet_id, to_wallet_id, 
                    token_id, amount, ts, raw_remark, usd_value
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    record.transaction_hash,
                    chain_id,
                    record.block_number,
                    from_wallet_id,
                    to_wallet_id,
                    token_id,
                    record.delta,
                    record.block_timestamp,
                    json.dumps(record.to_dict()),
                    usd_value,
                ),
            )

            # Check if balance record exists
            cur.execute(
                """
                SELECT 1 FROM wallet_balances 
                WHERE wallet_id = %s AND token_id = %s AND block_height = %s
                """,
                (wallet_id, token_id, record.block_number),
            )
            if cur.fetchone():
                logger.debug(
                    f"Balance record for block {record.block_number} already exists, skipping"
                )
                continue

            # Insert balance record
            cur.execute(
                """
                INSERT INTO wallet_balances (
                    wallet_id, token_id, chain_id, amount, block_height, ts, raw_remark
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    wallet_id,
                    token_id,
                    chain_id,
                    int(record.value),
                    record.block_number,
                    record.block_timestamp,
                    json.dumps(record.to_dict()),
                ),
            )

        except Exception as e:
            logger.error(
                f"Error storing transaction history for {record.transaction_hash}: {e}"
            )
            raise


def fetch_eth_balance(address: str) -> Optional[Dict]:
    """Fetch ETH balance.

    Args:
        address: Wallet address

    Returns:
        Optional[Dict]: Balance information dictionary
    """
    try:
        history = get_address_coin_balance_history.sync(
            client=blockscout,
            address_hash=address,
        )

        if not history:
            logger.warning(f"No balance history found for address {address}")
            return {
                "timestamp": datetime.now(UTC).isoformat(),
                "address": address,
                "balance": 0,
                "type": "ETH",
                "last_transaction": None,
            }

        latest_record = history.items[0]
        current_balance = int(latest_record.value) / 1e18
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:

                store_transaction_history(cur, address, history)
                conn.commit()

                return {
                    "timestamp": datetime.now(UTC).isoformat(),
                    "address": address,
                    "balance": current_balance,
                    "type": "ETH",
                    "last_transaction": {
                        "hash": latest_record.transaction_hash,
                        "block_number": latest_record.block_number,
                        "block_timestamp": latest_record.block_timestamp,
                        "delta": int(latest_record.delta) / 1e18,
                    },
                }
    except Exception as e:
        logger.error(f"Error in calculate_balance_from_history: {e}")
        return None


def fetch_usdt_balance(address: str) -> dict:
    """Fetch USDT balance.

    Args:
        address: Wallet address

    Returns:
        dict: Balance information dictionary
    """
    # TODO: Implement proper USDT balance fetching using blockscout API
    # For now, return a placeholder
    return {
        "timestamp": datetime.now(UTC).isoformat(),
        "address": address,
        "balance": 0,
        "type": "USDT",
    }


def store_balance_data(data: dict) -> None:
    """Store balance data in database.

    Args:
        data: Balance data dictionary
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                wallet_id = get_or_create_wallet(cur, data["address"])
                if not wallet_id:
                    logger.error(
                        f"Failed to get or create wallet for {data['address']}"
                    )
                    return

                token_id = get_or_create_token(cur, data["type"])
                if not token_id:
                    logger.error(f"Failed to get or create token for {data['type']}")
                    return

                chain_id = get_or_create_chain(cur)
                if not chain_id:
                    logger.error("Failed to get or create Ethereum chain")
                    return

                cur.execute(
                    """
                    INSERT INTO wallet_balances 
                    (wallet_id, token_id, chain_id, amount, ts, raw_remark)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (wallet_id, token_id, block_height) DO NOTHING
                    """,
                    (
                        wallet_id,
                        token_id,
                        chain_id,
                        int(
                            data["balance"] * 1e18
                            if data["type"] == "ETH"
                            else data["balance"] * 1e6
                        ),
                        data["timestamp"],
                        Json({"raw_data": data}),
                    ),
                )
                conn.commit()
    except Exception as e:
        logger.error(f"Error storing balance data: {e}")


def monitor_loop(interval: int = MONITOR_INTERVAL) -> None:
    """Main monitoring loop.

    Args:
        interval: Monitoring interval in seconds
    """
    while True:
        try:
            for addr in ETH_ADDRESSES:
                try:
                    eth_balance = fetch_eth_balance(addr)
                    if eth_balance is not None:
                        store_balance_data(eth_balance)
                except Exception as e:
                    logger.error(f"Error processing address {addr}: {e}")
                    continue
        except Exception as e:
            logger.error(f"Error in monitor loop: {e}")
        time.sleep(interval)


if __name__ == "__main__":
    try:
        monitor_loop()
    except KeyboardInterrupt:
        logger.info("Monitoring stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise
