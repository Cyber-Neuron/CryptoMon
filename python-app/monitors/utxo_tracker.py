"""UTXO tracking and address clustering."""

from collections import defaultdict
from typing import Dict, List, Optional, Set

from core.types import UTXO
from utils.logging_utils import setup_logging

logger = setup_logging()


class UTXOTracker:
    """Tracks UTXOs and manages address clustering."""

    def __init__(self):
        self.utxos: Dict[str, UTXO] = {}  # txid:vout -> UTXO
        self.address_utxos: Dict[str, Set[str]] = defaultdict(
            set
        )  # address -> set of txid:vout
        self.address_clusters: Dict[str, Set[str]] = defaultdict(
            set
        )  # address -> set of related addresses

    def add_utxo(self, utxo: UTXO) -> None:
        """Add a new UTXO to the tracker."""
        key = f"{utxo.txid}:{utxo.vout}"
        self.utxos[key] = utxo
        if utxo.address:
            self.address_utxos[utxo.address].add(key)

    def spend_utxo(self, txid: str, vout: int) -> Optional[UTXO]:
        """Mark a UTXO as spent and return it."""
        key = f"{txid}:{vout}"
        utxo = self.utxos.pop(key, None)
        if utxo and utxo.address:
            self.address_utxos[utxo.address].discard(key)
        return utxo

    def get_address_balance(self, address: str) -> int:
        """Get total balance for an address in satoshis."""
        return sum(
            self.utxos[key].value
            for key in self.address_utxos[address]
            if key in self.utxos
        )

    def update_address_cluster(self, addresses: List[str]) -> None:
        """Update address clusters based on shared inputs."""
        if len(addresses) <= 1:
            return

        # Add all addresses to each other's clusters
        for addr in addresses:
            self.address_clusters[addr].update(addresses)

    def get_cluster_balance(self, address: str) -> int:
        """Get total balance for an address cluster in satoshis."""
        cluster = self.address_clusters[address]
        return sum(self.get_address_balance(addr) for addr in cluster)
