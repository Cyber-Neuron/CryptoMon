"""
Optimized database operations for wallet monitoring system.
"""

import logging
from contextlib import contextmanager
from decimal import Decimal
from typing import Dict, List, Optional

import psycopg2
from config import DATABASE_URL
from models import Transaction, Wallet
from psycopg2.extras import execute_batch

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Optimized database manager with batch operations and caching."""

    def __init__(self):
        self._wallet_cache: Dict[str, Wallet] = {}
        self._token_cache: Dict[str, int] = {}
        self._chain_cache: Dict[str, int] = {}
        self._wallet_type_cache: Dict[str, int] = {}

    @contextmanager
    def get_connection(self):
        """Get database connection with context manager."""
        conn = psycopg2.connect(DATABASE_URL)
        try:
            yield conn
        finally:
            conn.close()

    def clear_cache(self):
        """Clear all caches."""
        self._wallet_cache.clear()
        self._token_cache.clear()
        self._chain_cache.clear()
        self._wallet_type_cache.clear()

    def get_or_create_chain(self, conn, chain_name: str) -> int:
        """Get or create chain with caching."""
        if chain_name in self._chain_cache:
            return self._chain_cache[chain_name]

        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO chains (name, native_sym)
                VALUES (%s, %s)
                ON CONFLICT (name) DO NOTHING
                RETURNING id
                """,
                (chain_name.lower(), chain_name.lower()),
            )
            result = cur.fetchone()
            if result is None:
                # If no new record was inserted, get the existing one
                cur.execute(
                    "SELECT id FROM chains WHERE name = %s",
                    (chain_name.lower(),),
                )
                result = cur.fetchone()
                if result is None:
                    raise ValueError(f"Failed to get chain: {chain_name}")

            chain_id = result[0]
            if chain_id is None:
                raise ValueError(f"Chain ID is None for chain: {chain_name}")
            self._chain_cache[chain_name] = chain_id
            return chain_id

    def get_or_create_token(self, conn, symbol: str, chain_id: int) -> int:
        """Get or create token with caching."""
        cache_key = f"{symbol}_{chain_id}"
        if cache_key in self._token_cache:
            return self._token_cache[cache_key]

        with conn.cursor() as cur:
            # Determine decimals based on token
            if "eth" in symbol.lower():
                decimals = 18
            elif symbol.lower() in ["usdt", "usdc"]:
                decimals = 6
            else:
                decimals = 18

            cur.execute(
                """
                INSERT INTO tokens (symbol, chain_id, decimals)
                VALUES (%s, %s, %s)
                ON CONFLICT (symbol, chain_id) DO NOTHING
                RETURNING id
                """,
                (symbol, chain_id, decimals),
            )
            result = cur.fetchone()
            if result is None:
                # If no new record was inserted, get the existing one
                cur.execute(
                    "SELECT id FROM tokens WHERE symbol = %s AND chain_id = %s",
                    (symbol, chain_id),
                )
                result = cur.fetchone()
                if result is None:
                    raise ValueError(
                        f"Failed to get token: {symbol} on chain {chain_id}"
                    )

            token_id = result[0]
            self._token_cache[cache_key] = token_id
            return token_id

    def get_or_create_wallet_type(self, conn, wallet_type_name: str) -> int:
        """Get or create wallet type with caching."""
        if wallet_type_name in self._wallet_type_cache:
            return self._wallet_type_cache[wallet_type_name]

        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO wallet_types (name)
                VALUES (%s)
                ON CONFLICT (name) DO NOTHING
                RETURNING id
                """,
                (wallet_type_name.lower(),),
            )
            result = cur.fetchone()
            if result is None:
                # If no new record was inserted, get the existing one
                cur.execute(
                    "SELECT id FROM wallet_types WHERE name = %s",
                    (wallet_type_name.lower(),),
                )
                result = cur.fetchone()
                if result is None:
                    raise ValueError(f"Failed to get wallet type: {wallet_type_name}")

            wallet_type_id = result[0]
            self._wallet_type_cache[wallet_type_name] = wallet_type_id
            return wallet_type_id

    def determine_wallet_type(self, friendly_name: Optional[str]) -> str:
        """根据friendly_name确定wallet_type"""
        if not friendly_name:
            return "regular"

        friendly_name_lower = friendly_name.lower()

        # 检查是否包含cold关键字
        if "cold" in friendly_name_lower:
            return "cold"
        # 检查是否包含hot关键字
        elif "hot" in friendly_name_lower:
            return "hot"
        # 检查是否包含deposit关键字
        elif "deposit" in friendly_name_lower:
            return "deposit"
        # 检查是否包含internal关键字
        elif "internal" in friendly_name_lower:
            return "internal"
        # 默认为regular
        else:
            return "regular"

    def get_or_create_wallet(self, conn, wallet: Wallet) -> int:
        """Get or create wallet with caching."""
        # 确保address为小写
        wallet.address = wallet.address.lower() if wallet.address else ""

        if wallet.address in self._wallet_cache:
            cached_wallet = self._wallet_cache[wallet.address]
            if cached_wallet.id is not None:
                wallet.id = cached_wallet.id
                return cached_wallet.id
            # If cached wallet has no ID, we need to create it in the database

        # 确定wallet_type
        if wallet.wallet_type is None:
            wallet.wallet_type = self.determine_wallet_type(wallet.friendly_name)

        # 获取或创建wallet_type_id
        wallet_type_id = self.get_or_create_wallet_type(conn, wallet.wallet_type)
        if wallet_type_id == 2:
            wallet.grp_type = "Hot"
        # if (
        #     wallet.address.lower()
        #     == "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48".lower()
        # ) or True:
        #     print("1111111111111:", wallet)
        # 1 / 0
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO wallets (address, chain_id, friendly_name, grp_type, grp_name, wallet_type_id)
                VALUES (
                    %s,
                    (SELECT id FROM chains WHERE name = %s),
                    %s,
                    %s,
                    %s,
                    %s
                )
                ON CONFLICT (address, chain_id) DO NOTHING
                RETURNING id
                """,
                (
                    wallet.address.lower(),
                    wallet.chain_id,
                    wallet.friendly_name or f"Wallet {wallet.address[:8]}",
                    wallet.grp_type or "UNK",
                    wallet.grp_name or "UNK",
                    wallet_type_id,
                ),
            )
            result = cur.fetchone()
            if result is None:
                # If no new record was inserted, get the existing one
                cur.execute(
                    """
                    SELECT id FROM wallets  
                    WHERE lower(address) = %s AND chain_id = (SELECT id FROM chains WHERE name = %s)
                    """,
                    (wallet.address, wallet.chain_id),
                )
                result = cur.fetchone()
                if result is None:
                    raise ValueError(f"Failed to get wallet: {wallet.address}")

            wallet_id = result[0]
            if wallet_id is None:
                raise ValueError(f"Wallet ID is None for wallet: {wallet.address}")
            wallet.id = wallet_id
            self._wallet_cache[wallet.address] = wallet
            return wallet_id

    def get_wallets_batch(self, conn, addresses: List[str]) -> Dict[str, Wallet]:
        """Get multiple wallets in batch."""
        if not addresses:
            return {}

        # 确保所有addresses都是小写
        addresses = [addr.lower() if addr else "" for addr in addresses]

        # Check cache first
        result = {}
        uncached_addresses = []

        for addr in addresses:
            if addr in self._wallet_cache:
                result[addr] = self._wallet_cache[addr]
            else:
                uncached_addresses.append(addr)

        if not uncached_addresses:
            return result

        # Query database for uncached addresses
        with conn.cursor() as cur:
            placeholders = ",".join(["%s"] * len(uncached_addresses))
            cur.execute(
                f"""
                SELECT w.id, w.address, w.chain_id, w.friendly_name, w.grp_type, w.grp_name, wt.name as wallet_type
                FROM wallets w
                LEFT JOIN wallet_types wt ON w.wallet_type_id = wt.id
                WHERE LOWER(w.address) IN ({placeholders})
                """,
                uncached_addresses,
            )

            for row in cur.fetchall():
                wallet = Wallet(
                    id=row[0],
                    address=row[1],
                    chain_id=row[2],
                    friendly_name=row[3],
                    grp_type=row[4],
                    grp_name=row[5],
                    wallet_type=row[6],
                )
                result[wallet.address] = wallet
                self._wallet_cache[wallet.address] = wallet

        return result

    def store_transactions_batch(self, conn, transactions: List[Transaction]) -> None:
        """Store transactions in batch with optimized queries."""
        if not transactions:
            return

        # First, ensure all wallet objects from transactions are stored in the database
        all_wallets = (
            []
        )  # Use list instead of set since Wallet objects are not hashable
        for tx in transactions:
            if tx.from_wallet and tx.from_wallet not in all_wallets:
                all_wallets.append(tx.from_wallet)
            if tx.to_wallet and tx.to_wallet not in all_wallets:
                all_wallets.append(tx.to_wallet)

        # Store all wallet objects first
        for wallet in all_wallets:
            self.get_or_create_wallet(conn, wallet)
        conn.commit()
        # Get all unique addresses (for wallets that might not have Wallet objects)
        all_addresses = set()
        for tx in transactions:
            # Only add addresses that don't have Wallet objects
            if not tx.from_wallet:
                all_addresses.add(tx.from_address.lower() if tx.from_address else "")
            if not tx.to_wallet:
                all_addresses.add(tx.to_address.lower() if tx.to_address else "")

        # Get or create wallets for addresses without Wallet objects
        address_wallets = self.get_wallets_batch(conn, list(all_addresses))

        # Get or create chain and tokens
        chain_id = self.get_or_create_chain(conn, "ethereum")
        token_ids = {}
        for tx in transactions:
            if tx.token not in token_ids:
                token_ids[tx.token] = self.get_or_create_token(conn, tx.token, chain_id)

        # Prepare transaction data for batch insert
        tx_data = []
        for tx in transactions:
            # Get wallet IDs - prioritize Wallet objects over address lookups
            if tx.from_wallet and tx.from_wallet.id:
                from_wallet_id = tx.from_wallet.id
            else:
                from_address = tx.from_address.lower() if tx.from_address else ""
                from_wallet = address_wallets.get(from_address)
                if from_wallet:
                    from_wallet_id = from_wallet.id
                else:
                    # Create a new wallet for this address
                    temp_wallet = Wallet(address=from_address)
                    from_wallet_id = self.get_or_create_wallet(conn, temp_wallet)

            if tx.to_wallet and tx.to_wallet.id:
                to_wallet_id = tx.to_wallet.id
            else:
                to_address = tx.to_address.lower() if tx.to_address else ""
                to_wallet = address_wallets.get(to_address)
                if to_wallet:
                    to_wallet_id = to_wallet.id
                else:
                    # Create a new wallet for this address
                    temp_wallet = Wallet(address=to_address)
                    to_wallet_id = self.get_or_create_wallet(conn, temp_wallet)

            # Handle None amount values
            amount_value = tx.amount if tx.amount is not None else Decimal(0.0)

            tx_data.append(
                (
                    tx.hash.hex() if isinstance(tx.hash, bytes) else tx.hash,
                    tx.block_number,
                    from_wallet_id,
                    to_wallet_id,
                    token_ids[tx.token],
                    amount_value,
                    tx.timestamp,
                    chain_id,
                    tx.usd_value if tx.usd_value else None,
                    tx.from_balance,
                    tx.to_balance,
                )
            )

        # Batch insert transactions
        with conn.cursor() as cur:
            execute_batch(
                cur,
                """
                INSERT INTO transactions (hash, block_number, from_wallet_id, to_wallet_id, 
                                        token_id, amount, timestamp, chain_id, usd_value, from_balance, to_balance)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (hash) DO NOTHING
                """,
                tx_data,
                page_size=100,
            )

        logger.info(f"Stored {len(transactions)} transactions in batch")

    def get_hot_wallets(self, conn, all_addresses: bool = False) -> Dict[str, Wallet]:
        """Get hot wallets with caching."""
        with conn.cursor() as cur:
            if all_addresses:
                cur.execute(
                    """
                    SELECT w.id, lower(w.address), w.grp_name, w.friendly_name, w.grp_type, wt.name as wallet_type
                    FROM wallets w
                    LEFT JOIN wallet_types wt ON w.wallet_type_id = wt.id
                    """
                )
            else:
                cur.execute(
                    """
                    SELECT w.id, lower(w.address), w.grp_name, w.friendly_name, w.grp_type, wt.name as wallet_type
                    FROM wallets w
                    LEFT JOIN wallet_types wt ON w.wallet_type_id = wt.id
                    WHERE w.grp_type = 'Hot' AND w.chain_id = (SELECT id FROM chains WHERE name = 'ethereum')
                    """
                )

            wallets = {}
            for row in cur.fetchall():
                wallet = Wallet(
                    id=row[0],
                    address=row[1].lower() if row[1] else "",  # 确保address为小写
                    grp_name=row[2],
                    friendly_name=row[3],
                    grp_type=row[4],
                    wallet_type=row[5],
                )
                wallets[wallet.address] = wallet
                self._wallet_cache[wallet.address] = wallet

            return wallets

    def store_all_data(self, transactions: List[Transaction]) -> None:
        """Store all data in a single transaction with batch operations."""
        try:
            with self.get_connection() as conn:

                # Store transactions
                self.store_transactions_batch(conn, transactions)

                conn.commit()
                logger.info(f"Successfully stored {len(transactions)} transactions")

        except Exception as e:
            logger.error(f"Error storing data: {e}", exc_info=True)
            raise
