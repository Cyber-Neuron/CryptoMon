"""Arbitrage signal generation based on transaction patterns."""

from typing import Optional

from bitcoin.core import CTransaction
from core.constants import ARBITRAGE_THRESHOLD_BTC, MEMPOOL_SIZE_THRESHOLD
from monitors.utxo_tracker import UTXOTracker
from utils.logging_utils import setup_logging

logger = setup_logging()


class ArbitrageSignalGenerator:
    """Generates arbitrage signals based on transaction patterns."""

    def __init__(self, utxo_tracker: UTXOTracker):
        self.utxo_tracker = utxo_tracker
        self.current_height = 0
        self.mempool_size = 0

    def update_chain_state(self, height: int, mempool_size: int) -> None:
        """Update current chain state."""
        self.current_height = height
        self.mempool_size = mempool_size

    def analyze_transaction(self, tx: CTransaction) -> Optional[str]:
        """Analyze a transaction for arbitrage opportunities."""
        total_output = sum(vout.nValue for vout in tx.vout) / 1e8

        if (
            total_output >= ARBITRAGE_THRESHOLD_BTC
            and self.mempool_size < MEMPOOL_SIZE_THRESHOLD
        ):
            # Check if transaction involves whale addresses
            input_addresses = []
            for vin in tx.vin:
                prev_utxo = self.utxo_tracker.spend_utxo(
                    vin.prevout.hash.hex(), vin.prevout.n
                )
                if prev_utxo and prev_utxo.address:
                    input_addresses.append(prev_utxo.address)

            # Generate signal if whale address is involved
            for addr in input_addresses:
                if addr in self.utxo_tracker.address_clusters:
                    return f"⚠️ Arbitrage Opportunity: Whale movement detected with low mempool congestion"

        return None
