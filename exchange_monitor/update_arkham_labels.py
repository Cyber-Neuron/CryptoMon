import json
import logging
import time
from typing import Optional

from arkham import ArkhamClient
from db_utils import (
    get_db_connection,
    get_wallets_to_update,
    process_arkham_response,
    update_wallet_friendly_name,
)

logger = logging.getLogger(__name__)


def update_wallet_labels(proxies):
    """Main function to update wallet labels from Arkham."""
    conn = get_db_connection()
    cur = conn.cursor()

    # Initialize Arkham client
    client = ArkhamClient(proxies)

    try:
        # Get all wallets that need updating
        wallets = get_wallets_to_update(cur)
        logger.info(f"Found {len(wallets)} wallets to update")

        for wallet_id, address, friendly_name in wallets:
            try:
                # Query Arkham API
                # if not friendly_name.startswith("Exchange Wallet"):
                #     continue
                logger.info(f"Updating wallet {address}, {friendly_name}")
                response = client.get_address_info(address)

                if response.status_code != 200:
                    logger.warning(
                        f"Failed to get Arkham data for {address}: {response.status_code}"
                    )
                    continue

                # Parse response
                response_data = json.loads(response.text)
                friendly_name, grp_name = process_arkham_response(response_data)

                if not friendly_name:
                    friendly_name = ""
                    grp_name = ""
                    logger.info(f"No Arkham label found for {address}, skipping")
                else:
                    logger.info(
                        f"Updated wallet {address} with label: {friendly_name}, {grp_name}"
                    )
                update_wallet_friendly_name(cur, wallet_id, friendly_name, grp_name)
                time.sleep(0.5)
            except Exception as e:
                logger.error(f"Error processing wallet {address}, {wallet_id}: {e}")
                continue

            # Commit all changes
            conn.commit()

    except Exception as e:
        logger.error(f"Error in update_wallet_labels: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    proxies = {
        "http": "socks5h://127.0.0.1:9050",
        "https": "socks5h://127.0.0.1:9050",
    }

    logging.basicConfig(level=logging.INFO)
    update_wallet_labels(proxies)
