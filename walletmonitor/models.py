"""
Data models for wallet monitoring system.
"""

from dataclasses import dataclass, field
from decimal import Decimal
from typing import List, Optional


@dataclass
class Wallet:
    """Wallet model representing a blockchain address."""

    address: str
    chain_id: str = "ethereum"
    friendly_name: Optional[str] = None
    grp_type: Optional[str] = None
    grp_name: Optional[str] = None
    wallet_type: Optional[str] = None
    id: Optional[int] = None

    def __post_init__(self):
        """Normalize address to lowercase."""
        self.address = self.address.lower() if self.address else ""

    @classmethod
    def from_dict(cls, data: dict) -> "Wallet":
        """Create Wallet instance from dictionary."""
        return cls(
            address=data.get("address", ""),
            chain_id=data.get("chain_id", "ethereum"),
            friendly_name=data.get("friendly_name"),
            grp_type=data.get("grp_type"),
            grp_name=data.get("grp_name"),
            wallet_type=data.get("wallet_type"),
            id=data.get("id"),
        )

    def to_dict(self) -> dict:
        """Convert to dictionary for database operations."""
        return {
            "address": self.address,
            "chain_id": self.chain_id,
            "friendly_name": self.friendly_name,
            "grp_type": self.grp_type,
            "grp_name": self.grp_name,
            "wallet_type": self.wallet_type,
            "id": self.id,
        }


@dataclass
class Transaction:
    """Transaction model representing a blockchain transaction."""

    # Core transaction fields
    hash: str
    block_number: int
    from_address: str
    to_address: str
    value: Optional[int] = None

    # Ethereum specific fields
    block_hash: Optional[str] = None
    chain_id: Optional[str] = None
    gas: Optional[int] = None
    gas_price: Optional[int] = None
    input: Optional[str] = None
    max_fee_per_gas: Optional[int] = None
    max_priority_fee_per_gas: Optional[int] = None
    nonce: Optional[int] = None
    r: Optional[str] = None
    s: Optional[str] = None
    v: Optional[int] = None
    transaction_index: Optional[int] = None
    type: Optional[int] = None
    y_parity: Optional[int] = None

    # Custom fields for business logic
    amount: Optional[Decimal] = None
    token: str = "ETH"
    timestamp: Optional[int] = None
    chain: str = "ethereum"
    usd_value: Optional[Decimal] = None
    from_wallet: Optional[Wallet] = None
    to_wallet: Optional[Wallet] = None
    id: Optional[int] = None
    from_balance: Optional[Decimal] = None
    to_balance: Optional[Decimal] = None

    def __post_init__(self):
        """Normalize addresses to lowercase and convert hex values."""
        self.from_address = self.from_address.lower() if self.from_address else ""
        self.to_address = self.to_address.lower() if self.to_address else ""

        # Convert hex values to integers
        if isinstance(self.block_number, str) and self.block_number.startswith("0x"):
            self.block_number = int(self.block_number, 16)
        if isinstance(self.value, str) and self.value.startswith("0x"):
            self.value = int(self.value, 16)
        if isinstance(self.gas, str) and self.gas.startswith("0x"):
            self.gas = int(self.gas, 16)
        if isinstance(self.gas_price, str) and self.gas_price.startswith("0x"):
            self.gas_price = int(self.gas_price, 16)
        if isinstance(self.max_fee_per_gas, str) and self.max_fee_per_gas.startswith(
            "0x"
        ):
            self.max_fee_per_gas = int(self.max_fee_per_gas, 16)
        if isinstance(
            self.max_priority_fee_per_gas, str
        ) and self.max_priority_fee_per_gas.startswith("0x"):
            self.max_priority_fee_per_gas = int(self.max_priority_fee_per_gas, 16)
        if isinstance(self.nonce, str) and self.nonce.startswith("0x"):
            self.nonce = int(self.nonce, 16)
        if isinstance(self.v, str) and self.v.startswith("0x"):
            self.v = int(self.v, 16)
        if isinstance(
            self.transaction_index, str
        ) and self.transaction_index.startswith("0x"):
            self.transaction_index = int(self.transaction_index, 16)
        if isinstance(self.type, str) and self.type.startswith("0x"):
            self.type = int(self.type, 16)
        if isinstance(self.y_parity, str) and self.y_parity.startswith("0x"):
            self.y_parity = int(self.y_parity, 16)
        if isinstance(self.chain_id, str) and self.chain_id.startswith("0x"):
            self.chain_id = str(int(self.chain_id, 16))

        # Convert amount and usd_value to Decimal
        if isinstance(self.amount, (int, float)):
            self.amount = Decimal(str(self.amount))
        if isinstance(self.usd_value, (int, float)):
            self.usd_value = Decimal(str(self.usd_value))
        if isinstance(self.from_balance, (int, float)):
            self.from_balance = Decimal(str(self.from_balance))
        if isinstance(self.to_balance, (int, float)):
            self.to_balance = Decimal(str(self.to_balance))

    @classmethod
    def from_dict(cls, data: dict) -> "Transaction":
        """Create Transaction instance from dictionary."""
        return cls(
            # Core fields
            hash=data.get("hash", "").hex(),
            block_number=data.get("blockNumber", data.get("block_number", 0)),
            from_address=data.get("from", ""),
            to_address=data.get("to", ""),
            value=data.get("value"),
            # Ethereum specific fields
            block_hash=data.get("blockHash"),
            chain_id=data.get("chainId"),
            gas=data.get("gas"),
            gas_price=data.get("gasPrice"),
            input=data.get("input"),
            max_fee_per_gas=data.get("maxFeePerGas"),
            max_priority_fee_per_gas=data.get("maxPriorityFeePerGas"),
            nonce=data.get("nonce"),
            r=data.get("r"),
            s=data.get("s"),
            v=data.get("v"),
            transaction_index=data.get("transactionIndex"),
            type=data.get("type"),
            y_parity=data.get("yParity"),
            # Custom fields
            amount=data.get("amount"),
            token=data.get("token", "ETH"),
            timestamp=data.get("timestamp"),
            chain=data.get("chain", "ethereum"),
            usd_value=data.get("usd_value"),
            from_wallet=(
                Wallet.from_dict(data.get("from_wallet", {}))
                if data.get("from_wallet")
                else None
            ),
            to_wallet=(
                Wallet.from_dict(data.get("to_wallet", {}))
                if data.get("to_wallet")
                else None
            ),
            id=data.get("id"),
            from_balance=data.get("from_balance"),
            to_balance=data.get("to_balance"),
        )

    def to_dict(self) -> dict:
        """Convert to dictionary for database operations."""
        return {
            # Core fields
            "hash": self.hash,
            "block_number": self.block_number,
            "from_address": self.from_address,
            "to_address": self.to_address,
            "value": self.value,
            # Ethereum specific fields
            "block_hash": self.block_hash,
            "chain_id": self.chain_id,
            "gas": self.gas,
            "gas_price": self.gas_price,
            "input": self.input,
            "max_fee_per_gas": self.max_fee_per_gas,
            "max_priority_fee_per_gas": self.max_priority_fee_per_gas,
            "nonce": self.nonce,
            "r": self.r,
            "s": self.s,
            "v": self.v,
            "transaction_index": self.transaction_index,
            "type": self.type,
            "y_parity": self.y_parity,
            # Custom fields
            "amount": float(self.amount) if self.amount else None,
            "token": self.token,
            "timestamp": self.timestamp,
            "chain": self.chain,
            "usd_value": float(self.usd_value) if self.usd_value else None,
            "id": self.id,
            "from_balance": float(self.from_balance) if self.from_balance else None,
            "to_balance": float(self.to_balance) if self.to_balance else None,
        }


@dataclass
class BlockData:
    """Block data model for processing."""

    number: int
    timestamp: int
    transactions: List[Transaction] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "BlockData":
        """Create BlockData instance from dictionary."""
        # Convert transaction dictionaries to Transaction objects
        transactions_data = data.get("transactions", [])
        transactions = []

        for tx_data in transactions_data:
            if isinstance(tx_data, dict):
                # If it's a dictionary, create Transaction object
                transactions.append(Transaction.from_dict(tx_data))
            elif isinstance(tx_data, Transaction):
                # If it's already a Transaction object, use it directly
                transactions.append(tx_data)
            else:
                # Skip invalid transaction data
                continue

        return cls(
            number=data.get("number", 0),
            timestamp=data.get("timestamp", 0),
            transactions=transactions,
        )
