"""
Database check script for wallet monitoring system.
"""

import logging

from database import DatabaseManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_database():
    """Check database tables and data."""
    try:
        db_manager = DatabaseManager()

        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                # Check chains
                cur.execute("SELECT * FROM chains")
                chains = cur.fetchall()
                logger.info(f"Chains: {len(chains)} records")
                for chain in chains:
                    logger.info(f"  - {chain}")

                # Check tokens
                cur.execute("SELECT * FROM tokens")
                tokens = cur.fetchall()
                logger.info(f"Tokens: {len(tokens)} records")
                for token in tokens:
                    logger.info(f"  - {token}")

                # Check wallets
                cur.execute("SELECT * FROM wallets")
                wallets = cur.fetchall()
                logger.info(f"Wallets: {len(wallets)} records")
                for wallet in wallets:
                    logger.info(f"  - {wallet}")

                # Check transactions
                cur.execute("SELECT COUNT(*) FROM transactions")
                result = cur.fetchone()
                tx_count = result[0] if result else 0
                logger.info(f"Transactions: {tx_count} records")

                # Check ex_flows
                cur.execute("SELECT COUNT(*) FROM ex_flows")
                result = cur.fetchone()
                flow_count = result[0] if result else 0
                logger.info(f"Exchange Flows: {flow_count} records")

    except Exception as e:
        logger.error(f"Database check failed: {e}")


if __name__ == "__main__":
    check_database()
