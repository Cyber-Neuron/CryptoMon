"""
DBWriter: Handles database operations for transactions.
"""

import logging
from typing import Dict, List

from db_utils import get_db_connection, store_ex_flows, store_transactions

logger = logging.getLogger(__name__)


def upsert_transactions(txs: List[Dict]) -> None:
    """Bulk‑upsert transactions into PostgreSQL."""
    if not txs:
        logger.info("No transactions to store")
        return

    logger.info(f"Storing {len(txs)} transactions to database")

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                logger.info("Starting transaction storage")
                store_transactions(cur, txs)
                logger.info("Transaction storage completed")
            conn.commit()
            logger.info("Database transaction committed successfully")
    except Exception as e:
        logger.error(f"Error storing transactions: {e}", exc_info=True)
        raise


def store_flows(flows: List[Dict]) -> None:
    """Store flows in the database."""
    if not flows:
        logger.info("No flows to store")
        return

    logger.info(f"Storing {len(flows)} flows to database")

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                logger.info("Starting flow storage")
                store_ex_flows(cur, flows)
                logger.info("Flow storage completed")
            conn.commit()
            logger.info("Database transaction committed successfully")
    except Exception as e:
        logger.error(f"Error storing flows: {e}", exc_info=True)
        raise
