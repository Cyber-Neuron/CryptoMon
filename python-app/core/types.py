"""Type definitions for the monitoring system."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class UTXO:
    """Represents an unspent transaction output."""

    txid: str
    vout: int
    value: int  # in satoshis
    script_pubkey: bytes
    address: Optional[str] = None
