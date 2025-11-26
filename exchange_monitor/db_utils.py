import json
import logging
from typing import Optional

import psycopg2
from config import DATABASE_URL
from psycopg2.extras import DictCursor

logger = logging.getLogger(__name__)


def get_db_connection():
    """Get a database connection."""
    return psycopg2.connect(DATABASE_URL)


def get_hot_wallets(cur, base):
    """Get all hot wallets."""
    cur.execute(
        "SELECT address FROM wallets WHERE grp_type = 'Hot' AND grp_name = %s",
        (base,),
    )
    return cur.fetchall()


def get_or_create_wallet(
    cur,
    address: str,
    friendly_name: Optional[str] = None,
    grp_type: Optional[str] = None,
    grp_name: Optional[str] = None,
) -> Optional[int]:
    """Get or create a wallet record.

    Args:
        cur: Database cursor
        address: Wallet address

    Returns:
        Optional[int]: Wallet ID if successful, None otherwise
    """
    try:
        # Get wallet ID
        cur.execute(
            """
            INSERT INTO wallets (address, chain_id, friendly_name, grp_type, grp_name)
            VALUES (
                %s,
                (SELECT id FROM chains WHERE name = 'Ethereum'),
                %s,
                %s,
                %s
            )
            ON CONFLICT (address, chain_id) DO UPDATE
            SET friendly_name = EXCLUDED.friendly_name,
                grp_type = EXCLUDED.grp_type,
                grp_name = EXCLUDED.grp_name
            RETURNING id
            """,
            (
                address,
                (
                    f"Exchange Wallet {address[:8]}"
                    if friendly_name is None
                    else friendly_name
                ),
                grp_type if grp_type else "exchange",
                grp_name if grp_name else "Binance",
            ),
        )
        logger.info(
            f"Inserted wallet: {address}, {friendly_name}, {grp_type}, {grp_name}"
        )
        result = cur.fetchone()
        return result[0] if result else None
    except Exception as e:
        logger.error(f"Error in get_or_create_wallet: {e}")
        return None


def get_or_create_token(
    cur, symbol: str, chain_id: Optional[int] = None
) -> Optional[int]:
    """Get or create a token record.

    Args:
        cur: Database cursor
        symbol: Token symbol (e.g., 'ETH', 'USDT', 'ethereum', 'usd-coin','tether')

    Returns:
        Optional[int]: Token ID if successful, None otherwise
    """
    try:

        if "eth" in symbol.lower():
            decimals = 18
        elif "btc" in symbol.lower():
            decimals = 6
        else:
            decimals = 1
        if chain_id is None:
            chain_id = 7  # Unknown
        cur.execute(
            """
            INSERT INTO tokens (symbol, chain_id, decimals)
            VALUES (
                %s,
                %s,
                %s
            )
            ON CONFLICT (symbol, chain_id) DO UPDATE
            SET decimals = EXCLUDED.decimals
            RETURNING id
            """,
            (
                symbol,
                chain_id,
                decimals,
            ),
        )
        result = cur.fetchone()
        return result[0] if result else None
    except Exception as e:
        logger.error(f"Error in get_or_create_token: {e}")
        return None


def get_or_create_chain(cur, chain: str) -> Optional[int]:
    """Get or create a chain record.

    Args:
        cur: Database cursor

    Returns:
        Optional[int]: Chain ID if successful, None otherwise
    """
    # print(f"get_or_create_chain: {chain}")
    try:
        cur.execute(
            """
            INSERT INTO chains (name, native_sym)
            VALUES (%s, %s)
            ON CONFLICT (name) DO UPDATE
            SET native_sym = EXCLUDED.native_sym
            RETURNING id
            """,
            (chain, chain),
        )
        result = cur.fetchone()
        return result[0] if result else None
    except Exception as e:
        logger.error(f"Error in get_or_create_chain: {e}")
        return None


def get_wallets_to_update(cur):
    """Get all wallets that need Arkham label updates.

    Returns:
        List of tuples containing (wallet_id, address)
    """
    try:
        cur.execute(
            """
            SELECT id, address,friendly_name
            FROM wallets
            
            """
        )  # WHERE (friendly_name LIKE 'Exchange Wallet%' or friendly_name ='UNK')
        return cur.fetchall()
    except Exception as e:
        logger.error(f"Error in get_wallets_to_update: {e}")
        return []


def update_wallet_friendly_name(
    cur, wallet_id: int, friendly_name: str, grp_name: Optional[str] = None
):
    """Update wallet's friendly name.

    Args:
        cur: Database cursor
        wallet_id: ID of the wallet to update
        friendly_name: New friendly name
    """
    try:
        cur.execute(
            """
            UPDATE wallets 
            SET friendly_name = %s, grp_name = %s, updated = %s
            WHERE id = %s
            """,
            (
                friendly_name if friendly_name else "UNK",
                grp_name if grp_name else "UNK",
                True if friendly_name else False,  # a tempoary fix
                wallet_id,
            ),
        )
        logger.info(f"Updated wallet {wallet_id}, {friendly_name}")
    except Exception as e:
        logger.error(f"Error in update_wallet_friendly_name: {e}")


def process_arkham_response(response_data: dict) -> tuple[Optional[str], Optional[str]]:
    """Process Arkham API response to extract friendly name.

    Args:
        response_data: JSON response from Arkham API

    Returns:
        Optional[str]: Combined friendly name if available, None otherwise
    """
    try:
        if not response_data or not isinstance(response_data, dict):
            return None, "UNK"

        names = []
        grp_name = "UNK"
        # Process all arkham-prefixed fields
        for key, value in response_data.items():
            # print(key, value)
            if key.lower().startswith("arkham") and isinstance(value, dict):
                name = value.get("name")
                grp_name = name if "entity" in key.lower() else name.split(" ")[0]
                if name:
                    names.append(name)
        # 1 / 0
        if not names:
            return None, grp_name

        return " ".join(names), grp_name
    except Exception as e:
        logger.error(f"Error in process_arkham_response: {e}")
        return None, "UNK"


def store_transactions(cur, transactions):
    """Store transactions in the database.

    Args:
        cur: Database cursor
        transactions: List of transaction dictionaries
    """
    try:
        logger.info(f"Starting to store {len(transactions)} transactions")
        success_count = 0
        error_count = 0
        filtered_transaction_hashs = []
        # Process each transaction
        for transaction in transactions:
            try:
                cur.execute(
                    "SELECT 1 FROM transactions WHERE tx_hash = %s",
                    (transaction.get("hash"),),
                )
                if cur.fetchone():
                    logger.info(
                        f"Transaction {transaction.get('hash')} already exists, skipping"
                    )
                    filtered_transaction_hashs.append(transaction.get("hash"))
                    continue

                # Get or create wallet IDs
                from_wallet_id = get_or_create_wallet(
                    cur,
                    transaction["from"],
                    friendly_name=transaction["from_label"],
                    grp_type=transaction["from_type"],
                    grp_name=transaction["from_entity"],
                )
                logger.info(
                    f"From wallet: {transaction['from']}, {transaction['from_label']}, {transaction['from_type']}, {transaction['from_entity']}"
                )
                to_wallet_id = get_or_create_wallet(
                    cur,
                    transaction["to"],
                    friendly_name=transaction["to_label"],
                    grp_type=transaction["to_type"],
                    grp_name=transaction["to_entity"],
                )
                logger.info(
                    f"To wallet: {transaction['to']}, {transaction['to_label']}, {transaction['to_type']}, {transaction['to_entity']}"
                )
                # Get or create chain ID
                # print(transaction)
                chain_id = get_or_create_chain(cur, transaction["chain"])
                # Get or create token ID
                token_id = get_or_create_token(cur, transaction["token"], chain_id)

                if not all([from_wallet_id, to_wallet_id, token_id, chain_id]):
                    logger.error(
                        f"Failed to get/create required records for transaction {transaction.get('hash')}, {[from_wallet_id, to_wallet_id, token_id, chain_id]}"
                    )
                    error_count += 1
                    continue

                # Store transaction
                cur.execute(
                    """
                    INSERT INTO transactions (
                        tx_hash, chain_id, block_height, from_wallet_id, to_wallet_id, 
                        token_id, amount, ts, raw_remark, usd_value
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (tx_hash) DO UPDATE SET
                        block_height = EXCLUDED.block_height,
                        from_wallet_id = EXCLUDED.from_wallet_id,
                        to_wallet_id = EXCLUDED.to_wallet_id,
                        token_id = EXCLUDED.token_id,
                        amount = EXCLUDED.amount,
                        ts = EXCLUDED.ts,
                        raw_remark = EXCLUDED.raw_remark,
                        usd_value = EXCLUDED.usd_value
                    """,
                    (
                        transaction["hash"],
                        chain_id,
                        transaction.get("block_number"),
                        from_wallet_id,
                        to_wallet_id,
                        token_id,
                        transaction.get("amount", 0),
                        transaction.get("timestamp"),
                        json.dumps(transaction),
                        transaction.get("usd_value", 0),
                    ),
                )
                success_count += 1
                logger.info(
                    f"Successfully stored transaction {transaction.get('hash')} - From: {transaction.get('from')[:8]} To: {transaction.get('to')[:8]} Amount: {transaction.get('amount')} {transaction.get('token')}"
                )

            except Exception as e:
                error_count += 1
                logger.error(
                    f"Error processing transaction {transaction.get('hash')}: {e}"
                )
                continue

        logger.info(
            f"Transaction storage completed. Success: {success_count}, Errors: {error_count}"
        )
        return filtered_transaction_hashs
    except Exception as e:
        logger.error(f"Error storing transactions: {e}")
        return {}
