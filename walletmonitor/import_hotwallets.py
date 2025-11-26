"""
Import hot wallet data from CSV to database.
"""

import csv
import logging
from typing import Dict, List

from database import DatabaseManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_chain_mapping() -> Dict[int, str]:
    """Get mapping from CSV chain_id to database chain name."""
    return {
        1: "ethereum",  # Ethereum
        7: "tron",  # Tron
    }


def import_hotwallets(csv_file: str = "hotwallet.csv"):
    """Import hot wallet data from CSV file."""
    try:
        db_manager = DatabaseManager()
        chain_mapping = get_chain_mapping()

        # First, ensure we have all required chains in the database
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                # Insert chains if they don't exist
                for chain_id, chain_name in chain_mapping.items():
                    cur.execute(
                        "INSERT INTO chains (name, native_sym) VALUES (%s, %s) ON CONFLICT (name) DO NOTHING",
                        (chain_name, "ETH" if chain_name == "ethereum" else "TRX"),
                    )

                # Get chain ID mappings from database
                cur.execute(
                    "SELECT id, name FROM chains WHERE name IN %s",
                    (tuple(chain_mapping.values()),),
                )
                db_chains = {row[1]: row[0] for row in cur.fetchall()}

                logger.info(f"Found chains in database: {db_chains}")

        # Read CSV and prepare data for insertion
        wallets_to_insert = []

        with open(csv_file, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                csv_chain_id = int(row["chain_id"])
                if csv_chain_id not in chain_mapping:
                    logger.warning(f"Skipping unknown chain_id: {csv_chain_id}")
                    continue

                chain_name = chain_mapping[csv_chain_id]
                db_chain_id = db_chains.get(chain_name)

                if not db_chain_id:
                    logger.error(f"Chain {chain_name} not found in database")
                    continue

                # Skip Tron addresses for now (chain_id = 7)
                if csv_chain_id == 7:
                    logger.info(f"Skipping Tron address: {row['address']}")
                    continue

                # Validate address length (max 42 characters for Ethereum)
                address = row["address"]
                if len(address) > 42:
                    logger.warning(f"Address too long, skipping: {address}")
                    continue

                wallet_data = {
                    "address": address,
                    "chain_id": db_chain_id,
                    "friendly_name": row["friendly_name"],
                    "grp_type": row["grp_type"],
                    "grp_name": row["grp_name"].lower() if row["grp_name"] else None,
                }

                wallets_to_insert.append(wallet_data)

        logger.info(f"Prepared {len(wallets_to_insert)} wallets for insertion")

        # Insert wallets in batches
        batch_size = 100
        inserted_count = 0
        skipped_count = 0

        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                for i in range(0, len(wallets_to_insert), batch_size):
                    batch = wallets_to_insert[i : i + batch_size]

                    # Use ON CONFLICT to skip duplicates
                    for wallet in batch:
                        try:
                            cur.execute(
                                """
                                INSERT INTO wallets (address, chain_id, friendly_name, grp_type, grp_name)
                                VALUES (%(address)s, %(chain_id)s, %(friendly_name)s, %(grp_type)s, %(grp_name)s)
                                ON CONFLICT (address, chain_id) DO NOTHING
                            """,
                                wallet,
                            )

                            if cur.rowcount > 0:
                                inserted_count += 1
                            else:
                                skipped_count += 1

                        except Exception as e:
                            logger.error(
                                f"Error inserting wallet {wallet['address']}: {e}"
                            )
                            skipped_count += 1

                    conn.commit()
                    logger.info(
                        f"Processed batch {i//batch_size + 1}, inserted: {inserted_count}, skipped: {skipped_count}"
                    )

        logger.info(
            f"Import completed! Inserted: {inserted_count}, Skipped: {skipped_count}"
        )
        return True

    except Exception as e:
        logger.error(f"Import failed: {e}")
        return False


def verify_import():
    """Verify the imported data."""
    try:
        db_manager = DatabaseManager()

        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                # Count total wallets
                cur.execute("SELECT COUNT(*) FROM wallets")
                result = cur.fetchone()
                total_wallets = result[0] if result else 0

                # Count by group
                cur.execute(
                    """
                    SELECT grp_name, COUNT(*) 
                    FROM wallets 
                    WHERE grp_name IS NOT NULL 
                    GROUP BY grp_name 
                    ORDER BY COUNT(*) DESC
                """
                )
                group_counts = cur.fetchall()

                # Count by chain
                cur.execute(
                    """
                    SELECT c.name, COUNT(*) 
                    FROM wallets w 
                    JOIN chains c ON w.chain_id = c.id 
                    GROUP BY c.name
                """
                )
                chain_counts = cur.fetchall()

                logger.info(f"Total wallets: {total_wallets}")
                logger.info("Wallets by group:")
                for group, count in group_counts:
                    logger.info(f"  {group}: {count}")

                logger.info("Wallets by chain:")
                for chain, count in chain_counts:
                    logger.info(f"  {chain}: {count}")

    except Exception as e:
        logger.error(f"Verification failed: {e}")


def main():
    """Main function."""
    logger.info("Starting hot wallet import...")

    # Import data
    success = import_hotwallets()

    if success:
        # Verify import
        logger.info("Verifying import...")
        verify_import()
    else:
        logger.error("Import failed!")


if __name__ == "__main__":
    main()
