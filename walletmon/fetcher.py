"""
BlockFetcher: Fetches recent block numbers covering a wall-clock window.
"""

import logging
from typing import List

from web3 import Web3

logger = logging.getLogger(__name__)


def get_recent_blocks(w3: Web3, minutes: int) -> List[int]:
    """Return block numbers covering the last `minutes` wall‑clock time."""
    logger.info(f"Fetching blocks for last {minutes} minutes")

    latest_block = w3.eth.get_block("latest")
    latest_number = latest_block["number"]
    latest_timestamp = latest_block["timestamp"]

    logger.info(f"Latest block: {latest_number} at timestamp {latest_timestamp}")

    # Find the oldest block within the window
    block_numbers = [latest_number]
    current_number = latest_number
    blocks_checked = 0

    while True:
        current_number -= 1
        if current_number < 0:
            logger.warning("Reached block 0, stopping search")
            break

        block = w3.eth.get_block(current_number)
        blocks_checked += 1

        if latest_timestamp - block["timestamp"] > minutes * 60:
            logger.info(
                f"Block {current_number} is older than {minutes} minutes, stopping search"
            )
            break
        block_numbers.append(current_number)

        # Log progress every 10 blocks
        if blocks_checked % 10 == 0:
            logger.info(
                f"Checked {blocks_checked} blocks, found {len(block_numbers)} in time window"
            )

    sorted_blocks = sorted(block_numbers)
    logger.info(
        f"Total blocks found: {len(sorted_blocks)} (range: {sorted_blocks[0]} to {sorted_blocks[-1]})"
    )
    return sorted_blocks
