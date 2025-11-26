"""
TxExtractor: Extracts and flattens transactions from blocks.
"""

import logging
import time
from typing import Dict, List, Optional

import requests
from web3 import Web3

logger = logging.getLogger(__name__)
import json

from arkham import ArkhamClient
from db import store_flows, upsert_transactions
from get_price import get_eth_usdt_price_at_unix
from web3 import Web3

# ERC20 transfer 方法的标准签名 keccak
ERC20_TRANSFER_TOPIC = Web3.keccak(text="Transfer(address,address,uint256)").hex()
USDT_CONTRACT = Web3.to_checksum_address("0xdAC17F958D2ee523a2206206994597C13D831ec7")
USDC_CONTRACT = Web3.to_checksum_address("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48")
WETH_CONTRACT = Web3.to_checksum_address("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2")
DAI_CONTRACT = Web3.to_checksum_address("0x6B175474E89094C44Da98b954EedeAC495271d0F")
TARGET_CONTRACTS = {USDT_CONTRACT, USDC_CONTRACT, WETH_CONTRACT, DAI_CONTRACT}


def extract_token_transfers(
    tx,
    web3: Web3,
    ts: int,
    min_eth: float,
    eth_price: float,
    to_entity: Optional[Dict[str, str]] = {},
    from_entity: Optional[Dict[str, str]] = {},
    full_addresses: Dict[str, Dict[str, str]] = {},
):
    """
    提取一笔交易内 ETH、USDT、USDC 转账记录
    - tx: web3.eth.get_transaction(tx_hash) 结果
    - receipt: web3.eth.get_transaction_receipt(tx_hash) 结果
    - web3: Web3 实例
    返回: [{'token': 'ETH/USDT/USDC', 'from': ..., 'to': ..., 'amount': ...}]
    tx_data = {
                    "hash": (
                        tx["hash"].hex() if hasattr(tx["hash"], "hex") else tx["hash"]
                    ),
                    "block_number": tx["blockNumber"],
                    "from": tx["from"],
                    "to": tx["to"],
                    "amount": int(tx["value"]),
                    "timestamp": block["timestamp"],
                    "chain": tx["chainId"],
                    "token": tx["input"],
                }
    """
    transfers = []

    # 1. ETH 原生转账
    if tx["value"] and tx["value"] > 0:
        if float(web3.from_wei(tx["value"], "ether")) >= min_eth:
            if not from_entity and tx["from"].lower() not in full_addresses:
                from_entity = extract_wallet_labels(tx["from"])
            if not to_entity and tx["to"].lower() not in full_addresses:
                to_entity = extract_wallet_labels(tx["to"])
            transfers.append(
                {
                    "hash": f"0x{tx['hash'].hex() if hasattr(tx['hash'], 'hex') else tx['hash']}",
                    "token": "ETH",
                    "from": tx["from"],
                    "to": tx["to"],
                    "amount": float(web3.from_wei(tx["value"], "ether")),
                    "block_number": tx["blockNumber"],
                    "timestamp": ts,
                    "chain": "ethereum" if tx["chainId"] == 1 else tx["chainId"],
                    "usd_value": float(web3.from_wei(tx["value"], "ether")) * eth_price,
                    "from_friendly_name": from_entity.get("friendly_name", "UNK"),
                    "from_grp_name": from_entity.get("grp_name", "UNK"),
                    "from_grp_type": from_entity.get("grp_type", "UNK"),
                    "to_friendly_name": to_entity.get("friendly_name", "UNK"),
                    "to_grp_name": to_entity.get("grp_name", "UNK"),
                    "to_grp_type": to_entity.get("grp_type", "UNK"),
                }
            )
        return transfers
    # 2. ERC20 Token 转账 (只提取 USDT/USDC)
    receipt = web3.eth.get_transaction_receipt(tx["hash"])
    for log in receipt["logs"]:
        # ERC20 Transfer 事件
        if (
            log["address"] in TARGET_CONTRACTS
            and log["topics"][0].hex() == ERC20_TRANSFER_TOPIC
            and len(log["topics"]) == 3
        ):
            token = None
            if log["address"] == USDT_CONTRACT:
                token = "USDT"
            elif log["address"] == USDC_CONTRACT:
                token = "USDC"
            elif log["address"] == WETH_CONTRACT:
                token = "WETH"
            else:
                continue  # 非目标

            # decode from, to, amount
            from_addr = Web3.to_checksum_address("0x" + log["topics"][1].hex()[-40:])
            to_addr = Web3.to_checksum_address("0x" + log["topics"][2].hex()[-40:])
            amount = int.from_bytes(log["data"], "big")

            # 单位换算
            if token == "USDT":
                amount = amount / 1e6  # USDT 6位小数
            elif token == "USDC":
                amount = amount / 1e6  # USDC 6位小数
            elif token == "WETH":
                amount = eth_price * amount / 1e18  # WETH 18位小数
            if amount <= min_eth * eth_price:
                continue
            if not from_entity and tx["from"].lower() not in full_addresses:
                from_entity = extract_wallet_labels(tx["from"])
            if not to_entity and tx["to"].lower() not in full_addresses:
                to_entity = extract_wallet_labels(tx["to"])
            transfers.append(
                {
                    "hash": f"0x{tx['hash'].hex() if hasattr(tx['hash'], 'hex') else tx['hash']}",
                    "token": token,
                    "from": from_addr,
                    "to": to_addr,
                    "amount": amount,
                    "timestamp": ts,
                    "block_number": tx["blockNumber"],
                    "chain": "ethereum" if tx["chainId"] == 1 else tx["chainId"],
                    "usd_value": amount,
                    "from_friendly_name": from_entity.get("friendly_name", "UNK"),
                    "from_grp_name": from_entity.get("grp_name", "UNK"),
                    "from_grp_type": from_entity.get("grp_type", "UNK"),
                    "to_friendly_name": to_entity.get("friendly_name", "UNK"),
                    "to_grp_name": to_entity.get("grp_name", "UNK"),
                    "to_grp_type": to_entity.get("grp_type", "UNK"),
                }
            )
    return transfers


def wei_to_eth(wei: int) -> float:
    """Convert WEI to ETH."""
    return wei / 1e18


def get_eth_price():
    try:
        resp = requests.get(
            "https://api.binance.com/api/v3/ticker/price", params={"symbol": "ETHUSDT"}
        ).json()
        return float(resp["price"])
    except:
        return 0.0


def process_arkham_response(response_data: dict) -> tuple[str, str, str]:
    """Process Arkham API response to extract friendly name.

    Args:
        response_data: JSON response from Arkham API

    Returns:
        Optional[str]: Combined friendly name if available, None otherwise
            "arkhamEntity": {
                    "name": "Binance",
                    "note": "",
                    "id": "binance",
                    "type": "cex",
                    "service": null,
                    "addresses": null,
                    "website": "https://binance.com",
                    "twitter": "https://twitter.com/binance",
                    "crunchbase": "https://www.crunchbase.com/organization/binance",
                    "linkedin": "https://www.linkedin.com/company/binance"
                },
                "arkhamLabel": {
                    "name": "Hot Wallet",
                    "address": "0xB38e8c17e38363aF6EbdCb3dAE12e0243582891D",
                    "chainType": "evm"
                },
    """
    try:
        if not response_data or not isinstance(response_data, dict):
            return "UNK", "UNK", "UNK"

        friendly_name = "UNK"
        grp_name = "UNK"
        grp_type = "UNK"
        # Process all arkham-prefixed fields
        for key, value in response_data.items():
            if key.lower().startswith("arkham") and isinstance(value, dict):
                if key == "arkhamEntity":
                    friendly_name = value.get("name", "UNK")
                    grp_name = value.get("id", "UNK")
                    grp_type = value.get("type", "UNK")
                elif key == "arkhamLabel":
                    name = value.get("name")
                    if name:
                        friendly_name = friendly_name + " " + name

        return friendly_name, grp_name, grp_type
    except Exception as e:
        logger.error(f"Error in process_arkham_response: {e}")
        return "UNK", "UNK", "UNK"


def extract_wallet_labels(address):
    proxies = {
        "http": "socks5h://127.0.0.1:9050",
        "https": "socks5h://127.0.0.1:9050",
    }
    """Main function to update wallet labels from Arkham."""

    # Initialize Arkham client
    client = ArkhamClient(proxies)
    friendly_name = "UNK"
    grp_name = "UNK"
    grp_type = "UNK"
    entity = {
        "grp_name": grp_name,
        "friendly_name": friendly_name,
        "grp_type": grp_type,
    }
    try:
        # Get all wallets that need updating
        # wallets = get_wallets_to_update(cur)
        # logger.info(f"Found {len(wallets)} wallets to update")

        # for wallet_id, address, friendly_name in wallets:
        try:

            response = client.get_address_info(address)

            if response.status_code != 200:
                logger.error(
                    f"Failed to get Arkham data for {address}: {response.status_code}"
                )
                return entity

            # Parse response
            response_data = json.loads(response.text)
            friendly_name, grp_name, grp_type = process_arkham_response(response_data)
            logger.info(
                f"Retrieved wallet {address} with label: {friendly_name}, {grp_name}, {grp_type}"
            )
            entity["friendly_name"] = friendly_name
            entity["grp_name"] = grp_name
            entity["grp_type"] = grp_type

            return entity
        except Exception as e:
            logger.error(f"Error processing wallet {address}: {e}")

        # Commit all changes

        return entity
    except Exception as e:
        logger.error(f"Error in update_wallet_labels: {e}")
        return entity


def extract_transactions(
    w3: Web3,
    watch_addresses: Dict[str, Dict[str, str]],
    min_eth: float,
    full_addresses: Dict[str, Dict[str, str]],
    minutes: int,
) -> List[Dict]:
    """Flatten all external txs for given blocks."""

    txs = []
    # eth_price = get_eth_price()
    #
    current_number = w3.eth.get_block_number()
    i = 0
    latest_timestamp = 0
    while True:
        current_number -= 1
        i += 1
        logger.info(f"Processing block {i}-th {current_number}")

        try:
            block = w3.eth.get_block(current_number, full_transactions=True)
            if i == 1:
                latest_timestamp = block["timestamp"]

            if latest_timestamp - block["timestamp"] > minutes * 60:
                logger.info(
                    f"Block {current_number} is older than {minutes} minutes, stopping search"
                )
                break
            logger.info(
                f"Processing block {i}-th {current_number}, {((latest_timestamp - block['timestamp'])//60)} mins ago."
            )
            time.sleep(1)
            eth_price = get_eth_usdt_price_at_unix(int(block["timestamp"]))
            if eth_price is None:
                logger.error(
                    f"History ETH price is None, getting from binance realtime"
                )
                eth_price = get_eth_price()
            logger.info(f"ETH price: {eth_price}")
            block_txs = block["transactions"]
            logger.info(
                f"Block {current_number} contains {len(block_txs)} transactions"
            )

            for tx in block_txs:
                if tx["to"] is None or tx["from"] is None:
                    logger.info("found tx with no to or from address")
                    try:
                        logger.info(tx["hash"].hex())
                    except:
                        # logger.info(tx["hash"])
                        _ = 1
                    continue
                if (
                    tx["to"].lower() in watch_addresses
                    or tx["from"].lower() in watch_addresses
                ):
                    from_entity = watch_addresses.get(tx["from"].lower(), {})
                    to_entity = watch_addresses.get(tx["to"].lower(), {})
                    if not from_entity:
                        from_entity = full_addresses.get(tx["from"].lower(), {})
                    if not to_entity:
                        to_entity = full_addresses.get(tx["to"].lower(), {})
                    tx_data = extract_token_transfers(
                        tx,
                        w3,
                        ts=block["timestamp"],
                        min_eth=min_eth,
                        eth_price=eth_price,
                        to_entity=to_entity,
                        from_entity=from_entity,
                        full_addresses=full_addresses,
                    )

                    txs.extend(tx_data)
            # Store transactions
            if txs:
                logger.info("Storing filtered transactions to database")
                upsert_transactions(txs)
                logger.info(f"Successfully stored {len(txs)} transactions")
                store_flows(txs)
                txs = []
            else:
                logger.info("No transactions to store")
        except Exception as e:
            logger.error(f"Error processing block {current_number}: {e}")
            continue

    logger.info(f"Total transactions extracted: {len(txs)}")
    if txs:

        total_value_eth = sum(tx["amount"] for tx in txs if tx["token"] == "ETH")
        total_value_usd = sum(tx["usd_value"] for tx in txs if tx["token"] != "ETH")
        logger.info(
            f"Total value in transactions: {total_value_usd} USD ({total_value_eth:.6f} ETH)"
        )

    return txs
