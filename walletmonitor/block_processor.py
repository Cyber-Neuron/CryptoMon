"""
Optimized block processor for extracting and processing transactions.
"""

import logging
import time
from decimal import Decimal
from typing import Dict, List, Optional, Set

import requests
from arkham import ArkhamClient
from config import Config
from database import DatabaseManager
from models import BlockData, Transaction, Wallet
from web3 import Web3
from web3.types import TxReceipt

logger = logging.getLogger(__name__)

# ERC20 transfer method signature
ERC20_TRANSFER_TOPIC = Web3.keccak(text="Transfer(address,address,uint256)").hex()

# Target token contracts
TARGET_CONTRACTS = {
    Web3.to_checksum_address(
        "0xdAC17F958D2ee523a2206206994597C13D831ec7"
    ): "USDT",  # USDT
    Web3.to_checksum_address(
        "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
    ): "USDC",  # USDC
    Web3.to_checksum_address(
        "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
    ): "WETH",  # WETH
    Web3.to_checksum_address(
        "0x6B175474E89094C44Da98b954EedeAC495271d0F"
    ): "DAI",  # DAI
}
CONTRACT_ADDRESS = {
    "USDT": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
    "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
    "WETH": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
    "DAI": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
}


class BlockProcessor:
    """Optimized block processor for transaction extraction and processing."""

    def __init__(self, web3: Web3, db_manager: DatabaseManager, config: Config):
        self.web3 = web3
        self.db_manager = db_manager
        self.config = config
        self.arkham_client = ArkhamClient()
        self._eth_price_cache = 0.0
        self._last_price_update = 0
        logger.debug(f"BlockProcessor initialized with debug mode: {config.DEBUG_MODE}")

    def get_eth_usdt_price_at_unix(self, unix_ts: int) -> float:
        """
        使用 Binance K线接口获取指定 unix_ts（秒）时间点的 ETH/USDT 开盘价格。
        精度为 1 分钟，返回 float（价格）或 None。
        """
        ms = unix_ts * 1000  # Binance 使用毫秒单位
        url = "https://api.binance.com/api/v3/klines"
        params = {
            "symbol": "ETHUSDT",
            "interval": "1m",
            "startTime": ms - 60_000,
            "endTime": ms,
        }

        try:
            resp = requests.get(url, params=params, timeout=5)
            data = resp.json()

            if isinstance(data, list) and len(data) > 0:
                open_price = float(data[0][1])  # [1] 是 open
                self._eth_price_cache = open_price
                return open_price
            else:
                print("No data returned for that timestamp.")
                return self._eth_price_cache
        except Exception as e:
            print("Error:", e)
            return self._eth_price_cache

    def get_usd_balance(
        self, address: str, token_address: str, block_number: int
    ) -> float:
        """Get USD balance of a token for a given address."""
        ERC20_ABI = '[{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"type":"function"}]'

        contract = self.web3.eth.contract(
            address=Web3.to_checksum_address(token_address), abi=ERC20_ABI
        )

        wallet = Web3.to_checksum_address(address)

        balance = contract.functions.balanceOf(wallet).call(
            block_identifier=block_number
        )
        return balance

    def get_eth_price(self) -> float:
        """Get ETH price with caching."""
        current_time = time.time()
        if current_time - self._last_price_update > 60:  # Cache for 1 minute
            try:
                resp = requests.get(
                    "https://api.binance.com/api/v3/ticker/price",
                    params={"symbol": "ETHUSDT"},
                    timeout=5,
                ).json()
                self._eth_price_cache = float(resp["price"])
                self._last_price_update = current_time
            except Exception as e:
                logger.warning(f"Failed to get ETH price: {e}")
        return self._eth_price_cache

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

    def extract_wallet_info(self, address: str) -> Wallet:
        """Extract wallet information from Arkham API."""
        if self.config.DEBUG_WALLET_INFO:
            logger.debug(f"Extracting wallet info for address: {address}")

        try:
            response = self.arkham_client.get_address_info(address)
            if response and isinstance(response, dict):
                if self.config.DEBUG_WALLET_INFO:
                    logger.debug(f"Arkham API response for {address}: {response}")

                # Process Arkham response
                friendly_name = "UNK"
                grp_name = "UNK"
                grp_type = "UNK"

                for key, value in response.items():
                    if key.lower().startswith("arkham") and isinstance(value, dict):
                        if key == "arkhamEntity":
                            friendly_name = value.get("name", "UNK")
                            grp_name = value.get("id", "UNK")
                            grp_type = value.get("type", "UNK")
                        elif key == "arkhamLabel":
                            if not friendly_name or friendly_name == "UNK":
                                friendly_name = value.get("name", "UNK")
                            if not grp_name or grp_name == "UNK":
                                grp_name = friendly_name.split(" ")[0]

                wallet = Wallet(
                    address=address,
                    friendly_name=friendly_name,
                    grp_name=grp_name,
                    grp_type=grp_type,
                )

                if self.config.DEBUG_WALLET_INFO:
                    logger.debug(
                        f"Created wallet info: {wallet.friendly_name} ({wallet.grp_name}) for {address}"
                    )

                return wallet
        except Exception as e:
            logger.warning(f"Failed to extract wallet info for {address}: {e}")

        if self.config.DEBUG_WALLET_INFO:
            logger.debug(f"Using default wallet info for {address}")
        return Wallet(address=address)

    def process_eth_transfer(
        self,
        tx: Transaction,
        block_timestamp: int,
        min_eth: float,
        eth_price: float,
        watch_addresses: Dict[str, Wallet],
        full_addresses: Dict[str, Wallet],
    ) -> Optional[Transaction]:
        """Process ETH native transfer."""
        if self.config.DEBUG_TRANSACTION_DETAILS:
            logger.debug(f"Processing ETH transfer: {tx.hash}")
            logger.debug(f"  From: {tx.from_address}")
            logger.debug(f"  To: {tx.to_address}")
            logger.debug(f"  Value: {tx.value} wei")

        if not tx.value or tx.value <= 0:
            if self.config.DEBUG_TRANSACTION_DETAILS:
                logger.debug("  Skipping: No ETH value in transaction")
            return None

        eth_amount = float(self.web3.from_wei(tx.value, "ether"))
        if self.config.DEBUG_TRANSACTION_DETAILS:
            logger.debug(f"  ETH amount: {eth_amount} ETH")
            logger.debug(f"  Minimum required: {min_eth} ETH")

        if eth_amount < min_eth:
            if self.config.DEBUG_TRANSACTION_DETAILS:
                logger.debug(
                    f"  Skipping: Amount below minimum threshold, {eth_amount} < {min_eth}"
                )
            return None

        # Get wallet information
        from_address = tx.from_address.lower()
        to_address = tx.to_address.lower()
        from_balance = self.web3.eth.get_balance(
            Web3.to_checksum_address(from_address),
            block_identifier=tx.block_number,
        )
        to_balance = self.web3.eth.get_balance(
            Web3.to_checksum_address(to_address),
            block_identifier=tx.block_number,
        )
        tx.from_balance = Decimal(self.web3.from_wei(from_balance, "ether"))
        tx.to_balance = Decimal(self.web3.from_wei(to_balance, "ether"))
        if self.config.DEBUG_TRANSACTION_DETAILS:
            logger.debug(f"  Processing from address: {from_address}")
            logger.debug(f"  Processing to address: {to_address}")

        from_wallet = watch_addresses.get(from_address) or full_addresses.get(
            from_address
        )
        if not from_wallet:
            if self.config.DEBUG_TRANSACTION_DETAILS:
                logger.info(
                    f"  From address not in watch list, extracting info... {tx.from_address}"
                )
            from_wallet = self.extract_wallet_info(tx.from_address)

        to_wallet = watch_addresses.get(to_address) or full_addresses.get(to_address)
        if not to_wallet:
            if self.config.DEBUG_TRANSACTION_DETAILS:
                logger.info(
                    f"  To address not in watch list, extracting info... {tx.to_address}"
                )
            to_wallet = self.extract_wallet_info(tx.to_address)

        tx.from_wallet = from_wallet
        tx.to_wallet = to_wallet
        tx.timestamp = block_timestamp
        tx.usd_value = Decimal(eth_amount * eth_price)
        tx.amount = Decimal(eth_amount)

        if self.config.DEBUG_TRANSACTION_DETAILS:
            logger.debug(f"  Created ETH transaction: {tx.hash}")
            logger.debug(f"    From: {from_wallet.friendly_name} ({from_address})")
            logger.debug(f"    To: {to_wallet.friendly_name} ({to_address})")
            logger.debug(
                f"    Amount: {eth_amount} ETH (${eth_amount * eth_price:.2f})"
            )

        return tx

    def process_erc20_transfer(
        self,
        tx: Transaction,
        receipt: TxReceipt,
        block_timestamp: int,
        min_eth: float,
        eth_price: float,
        watch_addresses: Dict[str, Wallet],
        full_addresses: Dict[str, Wallet],
    ) -> List[Transaction]:
        """Process ERC20 token transfers."""
        transactions = []

        if self.config.DEBUG_TRANSACTION_DETAILS:
            logger.debug(f"Processing ERC20 transfers for tx: {tx.hash}")
            logger.debug(f"  Number of logs: {len(receipt.get('logs', []))}")

        for i, log in enumerate(receipt["logs"]):
            if self.config.DEBUG_TRANSACTION_DETAILS:
                logger.debug(f"  Processing log {i+1}/{len(receipt['logs'])}")
                logger.debug(f"    Contract: {log.get('address', 'unknown')}")
                logger.debug(
                    f"    Topic0: {log.get('topics', [''])[0].hex() if log.get('topics') else 'none'}"
                )

            if (
                log["address"] in TARGET_CONTRACTS
                and log["topics"][0].hex() == ERC20_TRANSFER_TOPIC
                and len(log["topics"]) == 3
            ):
                token_symbol = TARGET_CONTRACTS[log["address"]]

                if self.config.DEBUG_TRANSACTION_DETAILS:
                    logger.debug(f"    Found {token_symbol} transfer")

                # Decode transfer parameters
                from_addr = Web3.to_checksum_address(
                    "0x" + log["topics"][1].hex()[-40:]
                )
                to_addr = Web3.to_checksum_address("0x" + log["topics"][2].hex()[-40:])
                amount = int.from_bytes(log["data"], "big")

                if self.config.DEBUG_TRANSACTION_DETAILS:
                    logger.debug(f"    From: {from_addr}")
                    logger.debug(f"    To: {to_addr}")
                    logger.debug(f"    Raw amount: {amount}")

                # Convert to proper units
                if token_symbol in ["USDT", "USDC"]:
                    amount = amount / 1e6
                elif token_symbol == "WETH":
                    amount = eth_price * amount / 1e18
                elif token_symbol == "DAI":
                    amount = amount / 1e18

                if self.config.DEBUG_TRANSACTION_DETAILS:
                    logger.debug(f"    Converted amount: {amount} {token_symbol}")

                # Check minimum amount
                if token_symbol in ["USDT", "USDC"]:
                    min_amount = min_eth * eth_price
                else:
                    min_amount = min_eth * eth_price

                if self.config.DEBUG_TRANSACTION_DETAILS:
                    logger.debug(f"    Minimum required: {min_amount} USD")

                if amount < min_amount:
                    if self.config.DEBUG_TRANSACTION_DETAILS:
                        logger.debug(
                            f"    Skipping: Amount below minimum threshold, {amount} < {min_amount}"
                        )
                    continue

                # Get wallet information
                from_address = from_addr.lower()
                to_address = to_addr.lower()
                from_balance = self.get_usd_balance(
                    from_address, CONTRACT_ADDRESS[token_symbol], tx.block_number
                )
                to_balance = self.get_usd_balance(
                    to_address, CONTRACT_ADDRESS[token_symbol], tx.block_number
                )
                if self.config.DEBUG_TRANSACTION_DETAILS:
                    logger.debug(f"    Processing from address: {from_address}")
                    logger.debug(f"    Processing to address: {to_address}")

                from_wallet = watch_addresses.get(from_address) or full_addresses.get(
                    from_address
                )
                if not from_wallet:
                    if self.config.DEBUG_TRANSACTION_DETAILS:
                        logger.info(
                            f"    From address not in watch list, extracting info... {from_addr}"
                        )
                    from_wallet = self.extract_wallet_info(from_addr)

                to_wallet = watch_addresses.get(to_address) or full_addresses.get(
                    to_address
                )
                if not to_wallet:
                    if self.config.DEBUG_TRANSACTION_DETAILS:
                        logger.info(
                            f"    To address not in watch list, extracting info... {to_addr}"
                        )
                    to_wallet = self.extract_wallet_info(to_addr)
                tx.from_wallet = from_wallet
                tx.to_wallet = to_wallet
                tx.timestamp = block_timestamp
                tx.usd_value = Decimal(amount)
                tx.amount = Decimal(amount)
                tx.token = token_symbol
                if token_symbol == "USDT" or token_symbol == "USDC":
                    tx.from_balance = Decimal(from_balance) / Decimal("1e6")
                    tx.to_balance = Decimal(to_balance) / Decimal("1e6")
                else:
                    tx.from_balance = Decimal(from_balance) / Decimal("1e18")
                    tx.to_balance = Decimal(to_balance) / Decimal("1e18")
                if self.config.DEBUG_TRANSACTION_DETAILS:
                    logger.debug(f"    Created {token_symbol} transaction: {tx.hash}")
                    logger.debug(
                        f"      From: {from_wallet.friendly_name} ({from_address})"
                    )
                    logger.debug(f"      To: {to_wallet.friendly_name} ({to_address})")
                    logger.debug(f"      Amount: {amount} {token_symbol}")

                transactions.append(tx)

        if self.config.DEBUG_TRANSACTION_DETAILS:
            logger.debug(f"  Total ERC20 transactions found: {len(transactions)}")

        return transactions

    def process_transaction(
        self,
        tx: Transaction,
        block_timestamp: int,
        min_eth: float,
        eth_price: float,
        watch_addresses: Dict[str, Wallet],
        full_addresses: Dict[str, Wallet],
    ) -> List[Transaction]:
        """Process a single transaction."""
        if self.config.DEBUG_TRANSACTION_DETAILS:
            logger.debug(f"Processing transaction: {tx.hash}")

        try:

            transactions = []

            # Process ETH transfer
            if self.config.DEBUG_TRANSACTION_DETAILS:
                logger.debug(f"  Checking for ETH transfer...")
            if tx.value > 0:
                eth_tx = self.process_eth_transfer(
                    tx,
                    block_timestamp,
                    min_eth,
                    eth_price,
                    watch_addresses,
                    full_addresses,
                )
                if eth_tx:
                    transactions.append(eth_tx)
                    if self.config.DEBUG_TRANSACTION_DETAILS:
                        logger.debug(f"  Found ETH transfer, skipping ERC20 processing")
                return transactions  # If ETH transfer found, skip ERC20 processing

            # Process ERC20 transfers
            if self.config.DEBUG_TRANSACTION_DETAILS:
                logger.debug(f" No ETH transfer found, checking for ERC20 transfers...")
            receipt = self.web3.eth.get_transaction_receipt(tx.hash)
            if receipt:
                erc20_txs = self.process_erc20_transfer(
                    tx,
                    receipt,
                    block_timestamp,
                    min_eth,
                    eth_price,
                    watch_addresses,
                    full_addresses,
                )
                transactions.extend(erc20_txs)
            else:
                if self.config.DEBUG_TRANSACTION_DETAILS:
                    logger.debug(f"No transaction receipt found")

            if self.config.DEBUG_TRANSACTION_DETAILS:
                logger.debug(f"  Total transactions found: {len(transactions)}")

            return transactions

        except Exception as e:
            logger.warning(f"Failed to process transaction {tx.hash}: {e}")
            if self.config.DEBUG_TRANSACTION_DETAILS:
                logger.debug(f"  Exception details: {e}", exc_info=True)
            return []

    def process_blocks(
        self,
        blocks: List[BlockData],
        min_eth: float,
        watch_addresses: Dict[str, Wallet],
        full_addresses: Dict[str, Wallet],
    ) -> List[Transaction]:
        """Process multiple blocks and extract transactions."""
        all_transactions = []

        logger.debug(
            f"Processing {len(blocks)} blocks with {len(watch_addresses)} watch addresses"
        )

        logger.debug(f"Minimum ETH threshold: {min_eth} ETH")

        for block_idx, block in enumerate(blocks):
            logger.info(
                f"Processing block {block.number} ({block_idx + 1}/{len(blocks)}) with {len(block.transactions)} transactions"
            )
            eth_price = self.get_eth_usdt_price_at_unix(block.timestamp)
            logger.info(f"ETH price: ${eth_price:.2f}")
            if self.config.DEBUG_MODE:
                logger.debug(f"  Block timestamp: {block.timestamp}")
                logger.debug(f"  Block hash: {block.number}")

            block_transactions = 0

            for tx_idx, transaction in enumerate(block.transactions):
                if self.config.DEBUG_MODE:
                    logger.debug(
                        f"    Processing transaction {tx_idx + 1}/{len(block.transactions)}: {transaction.hash}"
                    )
                if (
                    transaction.from_address not in watch_addresses
                    and transaction.to_address not in watch_addresses
                ):
                    continue
                if transaction.from_address is None or transaction.to_address is None:
                    continue
                transactions = self.process_transaction(
                    transaction,
                    block.timestamp,
                    min_eth,
                    eth_price,
                    watch_addresses,
                    full_addresses,
                )
                all_transactions.extend(transactions)
                block_transactions += len(transactions)

                if self.config.DEBUG_MODE and transactions:
                    logger.debug(f"    Found {len(transactions)} relevant transactions")

            if self.config.DEBUG_MODE:
                logger.debug(
                    f"  Block {block.number} summary: {block_transactions} relevant transactions"
                )

        logger.info(f"Extracted {len(all_transactions)} transactions")

        if self.config.DEBUG_MODE:
            logger.debug("Transaction summary:")
            for tx in all_transactions:
                logger.debug(
                    f"  {tx.hash}: {tx.from_wallet.friendly_name if tx.from_wallet else 'Unknown'} -> {tx.to_wallet.friendly_name if tx.to_wallet else 'Unknown'} ({tx.amount} {tx.token})"
                )

        return all_transactions

    def get_recent_blocks(self, minutes: int = 10) -> List[BlockData]:
        """Get recent blocks within specified time range."""
        try:
            logger.debug(f"Fetching recent blocks from last {minutes} minutes...")

            current_block = self.web3.eth.block_number
            logger.debug(f"Current block number: {current_block}")
            time.sleep(1)
            current_timestamp = self.web3.eth.get_block(current_block)["timestamp"]
            target_timestamp = current_timestamp - (minutes * 60)

            logger.debug(f"Current timestamp: {current_timestamp}")
            logger.debug(
                f"Target timestamp: {target_timestamp} (looking back {minutes} minutes)"
            )

            blocks = []
            blocks_checked = 0
            max_blocks_to_check = 1000000  # Limit to prevent infinite loops

            for block_num in range(
                current_block, max(0, current_block - max_blocks_to_check), -1
            ):
                try:
                    blocks_checked += 1
                    if self.config.DEBUG_MODE:
                        logger.debug(
                            f"  Checking block {block_num} ({blocks_checked}/{max_blocks_to_check})"
                        )

                    block = self.web3.eth.get_block(block_num, full_transactions=True)
                    block_timestamp = block["timestamp"]

                    if self.config.DEBUG_MODE:
                        logger.debug(
                            f"    Block {block_num} timestamp: {block_timestamp}"
                        )

                    if block_timestamp < target_timestamp:
                        if self.config.DEBUG_MODE:
                            logger.debug(
                                f"    Block {block_num} is too old (timestamp {block_timestamp} < target {target_timestamp})"
                            )
                        break
                    transactions = []
                    for raw_tx in block["transactions"]:
                        tx = Transaction.from_dict(raw_tx)
                        transactions.append(tx)

                    # Create block data dictionary
                    block_data = {
                        "number": block["number"],
                        "timestamp": block["timestamp"],
                        "transactions": transactions,
                    }

                    # Convert to BlockData model

                    blocks.append(BlockData.from_dict(block_data))

                    if self.config.DEBUG_MODE:
                        logger.debug(
                            f"    Added block {block_num} with {len(block['transactions'])} transactions"
                        )

                except Exception as e:
                    logger.warning(f"Failed to get block {block_num}: {e}")
                    if self.config.DEBUG_MODE:
                        logger.debug(f"    Exception details: {e}")
                    continue

            logger.info(
                f"Retrieved {len(blocks)} blocks from the last {minutes} minutes (checked {blocks_checked} blocks)"
            )

            if self.config.DEBUG_MODE:
                logger.debug("Block summary:")
                for block in blocks:
                    logger.debug(
                        f"  Block {block.number}: {len(block.transactions)} transactions"
                    )

            return blocks

        except Exception as e:
            logger.error(f"Failed to get recent blocks: {e}", exc_info=True)
            return []
