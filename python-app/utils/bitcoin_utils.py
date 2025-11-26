"""Bitcoin utility functions."""

import hashlib
import struct
from typing import Optional

from bitcoin.core import CTransaction
from bitcoin.core.script import CScript
from core.constants import MAGIC_MAINNET


def sha256d(data: bytes) -> bytes:
    """Double SHA256 hash."""
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()


def make_message(command: str, payload: bytes) -> bytes:
    """Build a Bitcoin P2P message."""
    command_bytes = command.encode("ascii") + b"\x00" * (12 - len(command))
    length = struct.pack("<I", len(payload))
    checksum = sha256d(payload)[:4]
    return MAGIC_MAINNET + command_bytes + length + checksum + payload


def get_address_from_script(script: CScript) -> Optional[str]:
    """Extract address from scriptPubKey."""
    try:
        # This is a simplified version - you might want to use a proper Bitcoin library
        # to handle all script types
        if hasattr(script, "is_p2pkh") and script.is_p2pkh():
            return bytes(script[2]).hex()
        elif hasattr(script, "is_p2sh") and script.is_p2sh():
            return bytes(script[1]).hex()
        return None
    except:
        return None
