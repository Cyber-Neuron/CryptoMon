import json
import logging
from datetime import datetime, timezone
from typing import Optional

import psycopg2
from config import DATABASE_URL

logger = logging.getLogger(__name__)


def get_db_connection():
    """Get a database connection."""
    return psycopg2.connect(DATABASE_URL)


def get_hot_wallets(cur, all_addresses=False):
    """Get all hot wallets."""
    if all_addresses:
        cur.execute("SELECT LOWER(address),grp_name,friendly_name FROM wallets")
    else:
        cur.execute(
            "SELECT LOWER(address),grp_name,friendly_name FROM wallets WHERE grp_type = 'Hot' and chain_id= '1'"
        )
    return cur.fetchall()


def get_wallet_friendly_name(cur, wallet_id: int):
    """Get wallet friendly name by ID."""
    cur.execute("SELECT friendly_name FROM wallets WHERE id = %s", (wallet_id,))
    result = cur.fetchone()

    return result[0] if result else None


def get_grp_name_by_address(cur, address: str):
    """Get grp name by address."""
    address = address.lower() if address else ""
    cur.execute("SELECT grp_name FROM wallets WHERE LOWER(address) = %s", (address,))
    result = cur.fetchone()
    return result[0] if result else None


def get_wallet_by_address(cur, address: str):
    """Get wallet ID by address."""
    address = address.lower() if address else ""
    cur.execute(
        "SELECT id,friendly_name FROM wallets WHERE LOWER(address) = %s",
        (address,),
    )
    result = cur.fetchone()
    if result:
        wallet_id = result[0]
        friendly_name = result[1]
        return wallet_id, friendly_name
    else:
        return None, None


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
        address = address.lower() if address else ""

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
                grp_type if grp_type else "UNK",
                grp_name if grp_name else "UNK",
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
            (chain.lower(), chain.lower()),
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
            WHERE friendly_name LIKE 'Exchange Wallet%'
            """
        )
        return cur.fetchall()
    except Exception as e:
        logger.error(f"Error in get_wallets_to_update: {e}")
        return []


def update_wallet_friendly_name(cur, wallet_id: int, friendly_name: str):
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
            SET friendly_name = %s, updated = %s
            WHERE id = %s
            """,
            (
                friendly_name if friendly_name else "Unknown",
                True if friendly_name else True,  # a tempoary fix
                wallet_id,
            ),
        )
        logger.info(f"Updated wallet {wallet_id}, {friendly_name}")
    except Exception as e:
        logger.error(f"Error in update_wallet_friendly_name: {e}")


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
        # print(transactions)
        for transaction in transactions:
            print(transaction.get("hash"))
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
                from_wallet_id, from_wallet_friendly_name = get_wallet_by_address(
                    cur, transaction["from"]
                )
                if not from_wallet_id:
                    from_wallet_id = get_or_create_wallet(
                        cur,
                        transaction["from"],
                        transaction["from_friendly_name"],
                        transaction["from_grp_type"],
                        transaction["from_grp_name"],
                    )
                    from_wallet_friendly_name = transaction["from_friendly_name"]
                to_wallet_id, to_wallet_friendly_name = get_wallet_by_address(
                    cur, transaction["to"]
                )
                if not to_wallet_id:
                    to_wallet_id = get_or_create_wallet(
                        cur,
                        transaction["to"],
                        transaction["to_friendly_name"],
                        transaction["to_grp_type"],
                        transaction["to_grp_name"],
                    )
                    to_wallet_friendly_name = transaction["to_friendly_name"]
                logger.info(
                    f"From: {from_wallet_friendly_name} To: {to_wallet_friendly_name}, with {transaction.get('amount')} ETH"
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
                        (
                            datetime.fromtimestamp(
                                transaction.get("timestamp"), tz=timezone.utc
                            ).strftime("%Y-%m-%d %H:%M:%S+00")
                            if transaction.get("timestamp")
                            else None
                        ),
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


def store_ex_flows(cur, txs):
    """Store ex flows in the database.

    Args:
        cur: Database cursor
        txs: List of transaction dictionaries

    """
    try:
        logger.info(f"Starting to store {len(txs)} ex flows")
        success_count = 0
        error_count = 0
        print(txs)
        for tx in txs:
            try:
                # Check if ex_flow already exists
                cur.execute(
                    "SELECT 1 FROM ex_flows WHERE tx_hash = %s",
                    (tx.get("hash"),),
                )
                if cur.fetchone():
                    logger.info(f"Ex flow {tx.get('hash')} already exists, skipping")
                    continue

                # Get or create token ID
                token_id = get_or_create_token(cur, tx.get("token", "ETH"))
                if not token_id:
                    logger.error(
                        f"Failed to get/create token for {tx.get('token', 'ETH')}"
                    )
                    error_count += 1
                    continue

                # Get or create chain ID
                chain_id = get_or_create_chain(cur, tx.get("chain", "Ethereum"))
                if not chain_id:
                    logger.error(
                        f"Failed to get/create chain for {tx.get('chain', 'Ethereum')}"
                    )
                    error_count += 1
                    continue

                # Extract group name from transaction data
                from_grp_name = tx.get("from_grp_name", "UNK")
                to_grp_name = tx.get("to_grp_name", "UNK")

                timestamp = tx.get("timestamp")

                # Insert ex_flow record
                cur.execute(
                    """
                    INSERT INTO ex_flows (
                        timestamp, token_id, chain_id, from_grp_name, to_grp_name, 
                        amount, usd_value, tx_hash
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        timestamp,
                        token_id,
                        chain_id,
                        from_grp_name,
                        to_grp_name,
                        tx.get("amount", 0),
                        tx.get("usd_value", 0),
                        tx.get("hash"),
                    ),
                )

                success_count += 1
                logger.info(
                    f"Successfully stored ex flow {tx.get('hash')} - "
                    f"Amount: {tx.get('amount')} {tx.get('token', 'ETH')}, "
                    f"From: {from_grp_name} To: {to_grp_name}"
                )

            except Exception as e:
                error_count += 1
                logger.error(f"Error processing ex flow {tx.get('hash')}: {e}")
                continue

        logger.info(
            f"Ex flow storage completed. Success: {success_count}, Errors: {error_count}"
        )

    except Exception as e:
        logger.error(f"Error storing ex flows: {e}")
        raise
