#!/usr/bin/env python3
"""
Real-time block data fetcher using Web3 API to get block information and parse transactions.
"""

import json
import logging
import os
import sys
from typing import Optional

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from web3 import Web3

from walletmonitor.config import load_config
from walletmonitor.models import BlockData, Transaction

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class EthereumBlockFetcher:
    """Fetcher for Ethereum block data using Web3."""

    def __init__(self, rpc_url: str):
        """Initialize the fetcher with RPC URL."""
        self.web3 = Web3(Web3.HTTPProvider(rpc_url))
        if not self.web3.is_connected():
            raise ConnectionError(f"Failed to connect to Ethereum node at {rpc_url}")
        logger.info(f"Connected to Ethereum node: {rpc_url}")

    def get_latest_block_number(self) -> int:
        """Get the latest block number."""
        return self.web3.eth.block_number

    def get_block_by_number(
        self, block_number: int, full_transactions: bool = True
    ) -> Optional[dict]:
        """Get block data by block number."""
        try:
            block = self.web3.eth.get_block(
                block_number, full_transactions=full_transactions
            )
            return block
        except Exception as e:
            logger.error(f"Failed to get block {block_number}: {e}")
            return None

    def get_block_by_hash(
        self, block_hash: str, full_transactions: bool = True
    ) -> Optional[dict]:
        """Get block data by block hash."""
        try:
            # Use string directly, Web3 should handle it
            block = self.web3.eth.get_block(
                block_hash, full_transactions=full_transactions
            )
            return block
        except Exception as e:
            logger.error(f"Failed to get block {block_hash}: {e}")
            return None

    def convert_web3_transaction_to_dict(self, tx) -> dict:
        """Convert Web3 transaction object to dictionary format."""
        return {
            "hash": tx["hash"].hex(),
            "blockNumber": hex(tx["blockNumber"]),
            "blockHash": tx["blockHash"].hex(),
            "chainId": hex(tx.get("chainId", 1)),
            "from": tx["from"],
            "to": tx["to"],
            "gas": hex(tx["gas"]),
            "gasPrice": hex(tx["gasPrice"]),
            "input": tx["input"],
            "maxFeePerGas": hex(tx.get("maxFeePerGas", 0)),
            "maxPriorityFeePerGas": hex(tx.get("maxPriorityFeePerGas", 0)),
            "nonce": hex(tx["nonce"]),
            "r": tx.get("r", "").hex() if tx.get("r") else "",
            "s": tx.get("s", "").hex() if tx.get("s") else "",
            "v": hex(tx.get("v", 0)),
            "transactionIndex": hex(tx["transactionIndex"]),
            "type": hex(tx.get("type", 0)),
            "value": hex(tx["value"]),
            "yParity": hex(tx.get("yParity", 0)),
        }

    def get_block_data(
        self, block_number: Optional[int] = None, block_hash: Optional[str] = None
    ) -> Optional[BlockData]:
        """Get block data and convert to BlockData model."""
        raw_block: Optional[dict] = None

        if block_number is not None:
            raw_block = self.get_block_by_number(block_number)
        elif block_hash is not None:
            raw_block = self.get_block_by_hash(block_hash)
        else:
            logger.error("Either block_number or block_hash must be provided")
            return None

        if not raw_block:
            return None

        # Convert transactions to our format
        transactions = []
        for raw_tx in raw_block["transactions"]:
            # tx_dict = self.convert_web3_transaction_to_dict(tx)
            # transactions.append(tx_dict)
            tx = Transaction.from_dict(raw_tx)
            transactions.append(tx)

        # Create block data dictionary
        block_data = {
            "number": raw_block["number"],
            "timestamp": raw_block["timestamp"],
            "transactions": transactions,
        }

        # Convert to BlockData model
        return BlockData.from_dict(block_data)


def main():
    """Main function to demonstrate block fetching."""
    # Load configuration
    config = load_config()

    # Initialize fetcher
    try:
        fetcher = EthereumBlockFetcher(config.PUBLICNODE_URL)
    except Exception as e:
        logger.error(f"Failed to initialize fetcher: {e}")
        return

    # Get latest block number
    latest_block = fetcher.get_latest_block_number()
    logger.info(f"Latest block number: {latest_block}")

    # Fetch a recent block (e.g., 10 blocks ago to ensure it's confirmed)
    target_block = latest_block - 10
    logger.info(f"Fetching block {target_block}...")

    # Get block data
    block_data = fetcher.get_block_data(block_number=target_block)

    if not block_data:
        logger.error("Failed to fetch block data")
        return

    # Display block information
    print("\n" + "=" * 60)
    print("BLOCK INFORMATION")
    print("=" * 60)
    print(f"Block Number: {block_data.number}")
    print(f"Block Timestamp: {block_data.timestamp}")
    print(f"Number of Transactions: {len(block_data.transactions)}")

    # Display transaction details
    print(f"\n" + "=" * 60)
    print("TRANSACTION DETAILS")
    print("=" * 60)

    for i, tx in enumerate(block_data.transactions):
        print(f"\nTransaction {i+1}:")
        print(f"  Hash: {tx.hash}")
        print(f"  From: {tx.from_address}")
        print(f"  To: {tx.to_address}")
        print(f"  Value: {tx.value} wei ({(tx.value or 0) / 1e18:.6f} ETH)")
        print(f"  Gas: {tx.gas}")
        print(f"  Gas Price: {tx.gas_price} wei")
        print(f"  Transaction Index: {tx.transaction_index}")
        print(f"  Type: {tx.type}")
        print(f"  Chain ID: {tx.chain_id}")

        # Show additional details for EIP-1559 transactions
        if tx.type == 2:
            print(f"  Max Fee Per Gas: {tx.max_fee_per_gas} wei")
            print(f"  Max Priority Fee Per Gas: {tx.max_priority_fee_per_gas} wei")

        # Show input data if not empty
        if tx.input and tx.input != "0x":
            print(f"  Input Data: {tx.input[:50]}{'...' if len(tx.input) > 50 else ''}")

    # Summary statistics
    print(f"\n" + "=" * 60)
    print("SUMMARY STATISTICS")
    print("=" * 60)

    total_value = sum(tx.value or 0 for tx in block_data.transactions)
    total_gas = sum(tx.gas or 0 for tx in block_data.transactions)
    eth_transfers = [tx for tx in block_data.transactions if tx.value and tx.value > 0]
    contract_calls = [
        tx for tx in block_data.transactions if tx.input and tx.input != "0x"
    ]

    print(f"Total ETH Transferred: {total_value / 1e18:.6f} ETH")
    print(f"Total Gas Used: {total_gas:,}")
    print(f"ETH Transfer Transactions: {len(eth_transfers)}")
    print(f"Contract Call Transactions: {len(contract_calls)}")
    print(
        f"Empty Transactions: {len(block_data.transactions) - len(eth_transfers) - len(contract_calls)}"
    )

    print(f"\n" + "=" * 60)
    print("SUCCESS: Block data fetched and parsed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
