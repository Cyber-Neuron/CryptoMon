"""Python client for Blockscout API."""

from dataclasses import dataclass
from typing import List, Optional

import requests


@dataclass
class AccountBalance:
    """Account balance result."""

    address: str
    balance: int


@dataclass
class BlockReward:
    """Information about block reward."""

    block_number: int
    block_miner: str
    block_reward: int
    timestamp: int
    uncle_inclusion_reward: int
    uncles: List[str]


@dataclass
class Transaction:
    """Simplified Ethereum transaction structure."""

    block_hash: str
    block_number: int
    from_addr: str
    to_addr: Optional[str]
    value: int
    gas: int
    gas_price: int
    hash: str


@dataclass
class Address:
    """Simplified address information used in REST v2 responses."""

    hash: str
    coin_balance: Optional[str] = None
    transaction_count: Optional[str] = None
    is_contract: Optional[bool] = None
    is_scam: Optional[bool] = None
    is_verified: Optional[bool] = None
    name: Optional[str] = None


@dataclass
class Token:
    """Token information returned by REST v2 endpoints."""

    address: str
    name: Optional[str] = None
    symbol: Optional[str] = None
    decimals: Optional[str] = None
    total_supply: Optional[str] = None
    holders: Optional[str] = None
    volume_24h: Optional[str] = None
    type: Optional[str] = None
    icon_url: Optional[str] = None
    exchange_rate: Optional[str] = None


@dataclass
class TokenValue:
    """Helper structure for token value objects."""

    decimals: str
    value: str


@dataclass
class Transfer:
    """Token transfer object."""

    block_number: int
    block_hash: str
    transaction_hash: str
    timestamp: str
    from_addr: Address
    to_addr: Address
    token: Token
    total: TokenValue
    log_index: Optional[int] = None
    method: Optional[str] = None
    type: Optional[str] = None


@dataclass
class AddressCounters:
    """Counters for an address."""

    transactions_count: str
    token_transfers_count: str
    gas_usage_count: str
    validations_count: str


@dataclass
class TokenHolder:
    """Information about a token holder."""

    address: Address
    token_id: Optional[str]
    value: str


@dataclass
class TokenBalance:
    """Token balance associated with an address."""

    token: Token
    token_id: Optional[str]
    token_instance: Optional[NFTInstance]
    value: str


@dataclass
class BalanceHistoryItem:
    """Coin balance history record."""

    block_number: int
    block_timestamp: str
    delta: str
    transaction_hash: Optional[str]
    value: str


@dataclass
class BalanceHistoryByDay:
    """Daily coin balance history record."""

    date: str
    value: str


@dataclass
class BlockInfo:
    """Simplified block information for validated blocks."""

    hash: str
    height: int
    timestamp: str


@dataclass
class InternalTransaction:
    """Internal transaction record."""

    block_number: int
    transaction_hash: str
    from_addr: str
    to_addr: Optional[str]
    value: str
    success: bool
    index: int
    block_index: int
    gas_limit: Optional[str] = None
    created_contract: Optional[str] = None
    timestamp: Optional[str] = None
    type: Optional[str] = None


@dataclass
class LogEntry:
    """Log entry returned by REST v2."""

    address: str
    block_hash: str
    block_number: int
    transaction_hash: str
    data: str
    topics: List[str]
    index: int


@dataclass
class NFTInstance:
    """NFT instance information."""

    id: str
    owner: Address
    token: Token
    image_url: Optional[str] = None
    metadata: Optional[dict] = None
    media_url: Optional[str] = None
    animation_url: Optional[str] = None
    external_app_url: Optional[str] = None
    is_unique: Optional[bool] = None
    media_type: Optional[str] = None
    thumbnails: Optional[str] = None


@dataclass
class PaginatedResult:
    """Generic paginated response."""

    items: List
    next_page_params: Optional[dict] = None


class BlockscoutClient:
    """Simple client for the Blockscout explorer API."""

    def __init__(
        self,
        base_url: str = "https://eth.blockscout.com/api",
        api_v2_url: str = "https://eth.blockscout.com/api/v2",
    ) -> None:
        self.base_url = base_url
        self.api_v2_url = api_v2_url
        self.session = requests.Session()

    def _request(self, params: dict) -> dict:
        response = self.session.get(self.base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("status") == "0" and data.get("message") != "OK":
            raise ValueError(f"API error: {data.get('message')}")
        return data

    def _request_v2(
        self,
        path: str,
        params: Optional[dict] = None,
        method: str = "GET",
    ) -> dict:
        """Make a request to the REST v2 API."""
        url = f"{self.api_v2_url}{path}"
        response = self.session.request(method, url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    # --- helper parsers for REST v2 ---

    @staticmethod
    def _parse_address(data: dict) -> Address:
        return Address(
            hash=data.get("hash"),
            coin_balance=data.get("coin_balance"),
            transaction_count=data.get("transaction_count") or data.get("transactions_count"),
            is_contract=data.get("is_contract"),
            is_scam=data.get("is_scam"),
            is_verified=data.get("is_verified"),
            name=data.get("name"),
        )

    @staticmethod
    def _parse_token(data: dict) -> Token:
        return Token(
            address=data.get("address") or data.get("address_hash"),
            name=data.get("name"),
            symbol=data.get("symbol"),
            decimals=data.get("decimals"),
            total_supply=data.get("total_supply"),
            holders=data.get("holders") or data.get("holders_count"),
            volume_24h=data.get("volume_24h"),
            type=data.get("type"),
            icon_url=data.get("icon_url"),
            exchange_rate=data.get("exchange_rate"),
        )

    @staticmethod
    def _parse_transfer(data: dict) -> Transfer:
        return Transfer(
            block_number=int(data.get("block_number")),
            block_hash=data.get("block_hash"),
            transaction_hash=data.get("transaction_hash"),
            timestamp=data.get("timestamp"),
            from_addr=BlockscoutClient._parse_address(data.get("from", {})),
            to_addr=BlockscoutClient._parse_address(data.get("to", {})),
            token=BlockscoutClient._parse_token(data.get("token", {})),
            total=TokenValue(
                decimals=str(data.get("total", {}).get("decimals")),
                value=str(data.get("total", {}).get("value")),
            ),
            log_index=data.get("log_index"),
            method=data.get("method"),
            type=data.get("type"),
        )

    @staticmethod
    def _parse_internal_tx(data: dict) -> InternalTransaction:
        return InternalTransaction(
            block_number=int(data.get("block_number")),
            transaction_hash=data.get("transaction_hash"),
            from_addr=data.get("from"),
            to_addr=data.get("to"),
            value=data.get("value"),
            success=bool(data.get("success")),
            index=int(data.get("index")),
            block_index=int(data.get("block_index")),
            gas_limit=data.get("gas_limit"),
            created_contract=data.get("created_contract"),
            timestamp=data.get("timestamp"),
            type=data.get("type"),
        )

    @staticmethod
    def _parse_log(data: dict) -> LogEntry:
        return LogEntry(
            address=data.get("address"),
            block_hash=data.get("block_hash"),
            block_number=int(data.get("block_number")),
            transaction_hash=data.get("transaction_hash"),
            data=data.get("data"),
            topics=data.get("topics", []),
            index=int(data.get("index")),
        )

    @staticmethod
    def _parse_nft_instance(data: dict) -> NFTInstance:
        return NFTInstance(
            id=str(data.get("id")),
            owner=BlockscoutClient._parse_address(data.get("owner", {})),
            token=BlockscoutClient._parse_token(data.get("token", {})),
            image_url=data.get("image_url"),
            metadata=data.get("metadata"),
            media_url=data.get("media_url"),
            animation_url=data.get("animation_url"),
            external_app_url=data.get("external_app_url"),
            is_unique=data.get("is_unique"),
            media_type=data.get("media_type"),
            thumbnails=data.get("thumbnails"),
        )

    @staticmethod
    def _paginate(data: dict, item_parser) -> PaginatedResult:
        items = [item_parser(it) for it in data.get("items", [])]
        return PaginatedResult(items=items, next_page_params=data.get("next_page_params"))

    @staticmethod
    def _parse_tx_v2(data: dict) -> Transaction:
        return Transaction(
            block_hash=data.get("block_hash"),
            block_number=int(data.get("block_number")),
            from_addr=(data.get("from") or {}).get("hash") if isinstance(data.get("from"), dict) else data.get("from"),
            to_addr=(data.get("to") or {}).get("hash") if isinstance(data.get("to"), dict) else data.get("to"),
            value=int(data.get("value", 0)),
            gas=int(data.get("gas_used") or data.get("gas_limit") or 0),
            gas_price=int(data.get("gas_price") or 0),
            hash=data.get("hash"),
        )

    def get_block_number(self) -> int:
        """Return the latest block number."""
        data = self._request({"module": "block", "action": "eth_block_number"})
        result = data.get("result")
        if isinstance(result, str) and result.startswith("0x"):
            return int(result, 16)
        return int(result)

    def get_block_reward(self, block_number: int) -> BlockReward:
        params = {
            "module": "block",
            "action": "getblockreward",
            "blockno": block_number,
        }
        data = self._request(params)["result"]
        return BlockReward(
            block_number=int(data["blockNumber"]),
            block_miner=data["blockMiner"],
            block_reward=int(data["blockReward"]),
            timestamp=int(data["timeStamp"]),
            uncle_inclusion_reward=int(data.get("uncleInclusionReward", 0)),
            uncles=data.get("uncles", []),
        )

    def get_account_balance(self, address: str) -> AccountBalance:
        params = {
            "module": "account",
            "action": "balance",
            "address": address,
        }
        data = self._request(params)
        balance = int(data["result"])
        return AccountBalance(address=address, balance=balance)

    def get_transaction(self, txhash: str) -> Transaction:
        params = {
            "module": "transaction",
            "action": "gettxinfo",
            "txhash": txhash,
        }
        data = self._request(params)["result"]
        return Transaction(
            block_hash=data["blockHash"],
            block_number=int(data["blockNumber"]),
            from_addr=data["from"],
            to_addr=data.get("to"),
            value=int(data.get("value", 0)),
            gas=int(data.get("gas", 0)),
            gas_price=int(data.get("gasPrice", 0)),
            hash=data["hash"],
        )

    def get_account_transactions(
        self,
        address: str,
        page: int = 1,
        offset: int = 10,
        sort: str = "asc",
    ) -> List[Transaction]:
        params = {
            "module": "account",
            "action": "txlist",
            "address": address,
            "startblock": 0,
            "endblock": 99999999,
            "page": page,
            "offset": offset,
            "sort": sort,
        }
        data = self._request(params)["result"]
        txs = []
        for item in data:
            txs.append(
                Transaction(
                    block_hash=item["blockHash"],
                    block_number=int(item["blockNumber"]),
                    from_addr=item["from"],
                    to_addr=item.get("to"),
                    value=int(item.get("value", 0)),
                    gas=int(item.get("gas", 0)),
                    gas_price=int(item.get("gasPrice", 0)),
                    hash=item["hash"],
                )
            )
        return txs

    # --- REST API v2 methods ---

    def get_addresses(self, page: int = 1, limit: int = 100) -> PaginatedResult:
        """Return a list of native coin holders."""
        params = {"page": page, "limit": limit}
        data = self._request_v2("/addresses", params)
        return self._paginate(data, self._parse_address)

    def get_address_info(self, address: str) -> Address:
        """Return information about an address."""
        data = self._request_v2(f"/addresses/{address}")
        return self._parse_address(data)

    def get_address_counters(self, address: str) -> AddressCounters:
        """Return counters for an address."""
        data = self._request_v2(f"/addresses/{address}/counters")
        return AddressCounters(
            transactions_count=data.get("transactions_count"),
            token_transfers_count=data.get("token_transfers_count"),
            gas_usage_count=data.get("gas_usage_count"),
            validations_count=data.get("validations_count"),
        )

    def get_address_transactions(
        self,
        address: str,
        page: int = 1,
        offset: int = 50,
    ) -> PaginatedResult:
        """Return transactions for an address."""
        params = {"page": page, "offset": offset}
        data = self._request_v2(f"/addresses/{address}/transactions", params)
        return self._paginate(data, self._parse_tx_v2)

    def get_address_token_transfers(
        self,
        address: str,
        page: int = 1,
        offset: int = 50,
    ) -> PaginatedResult:
        """Return token transfers for an address."""
        params = {"page": page, "offset": offset}
        data = self._request_v2(f"/addresses/{address}/token-transfers", params)
        return self._paginate(data, self._parse_transfer)

    def get_address_internal_transactions(
        self,
        address: str,
        page: int = 1,
        offset: int = 50,
    ) -> PaginatedResult:
        """Return internal transactions for an address."""
        params = {"page": page, "offset": offset}
        data = self._request_v2(f"/addresses/{address}/internal-transactions", params)
        return self._paginate(data, self._parse_internal_tx)

    def get_address_logs(
        self,
        address: str,
        page: int = 1,
        offset: int = 50,
    ) -> PaginatedResult:
        """Return logs for an address."""
        params = {"page": page, "offset": offset}
        data = self._request_v2(f"/addresses/{address}/logs", params)
        return self._paginate(data, self._parse_log)

    def get_blocks_validated(self, address: str) -> PaginatedResult:
        """Return blocks validated by the address."""
        data = self._request_v2(f"/addresses/{address}/blocks-validated")
        return self._paginate(data, lambda b: BlockInfo(
            hash=b.get("hash"),
            height=int(b.get("height")),
            timestamp=b.get("timestamp"),
        ))

    def get_address_token_balances(self, address: str) -> List[TokenBalance]:
        """Return all token balances for the address."""
        data = self._request_v2(f"/addresses/{address}/token-balances")
        return [
            TokenBalance(
                token=self._parse_token(item.get("token", {})),
                token_id=item.get("token_id"),
                token_instance=self._parse_nft_instance(item["token_instance"]) if item.get("token_instance") else None,
                value=item.get("value"),
            )
            for item in data
        ]

    def get_address_tokens(
        self,
        address: str,
        page: int = 1,
        offset: int = 50,
    ) -> PaginatedResult:
        """Return token balances with filtering and pagination."""
        params = {"page": page, "offset": offset}
        data = self._request_v2(f"/addresses/{address}/tokens", params)
        return self._paginate(
            data,
            lambda item: TokenBalance(
                token=self._parse_token(item.get("token", {})),
                token_id=item.get("token_id"),
                token_instance=self._parse_nft_instance(item["token_instance"]) if item.get("token_instance") else None,
                value=item.get("value"),
            ),
        )

    def get_address_coin_balance_history(
        self,
        address: str,
        page: int = 1,
        offset: int = 50,
    ) -> PaginatedResult:
        """Return coin balance history of an address."""
        params = {"page": page, "offset": offset}
        data = self._request_v2(f"/addresses/{address}/coin-balance-history", params)
        return self._paginate(
            data,
            lambda it: BalanceHistoryItem(
                block_number=int(it.get("block_number")),
                block_timestamp=it.get("block_timestamp"),
                delta=it.get("delta"),
                transaction_hash=it.get("transaction_hash"),
                value=it.get("value"),
            ),
        )

    def get_address_coin_balance_history_by_day(self, address: str) -> PaginatedResult:
        """Return daily coin balance history of an address."""
        data = self._request_v2(f"/addresses/{address}/coin-balance-history-by-day")
        return self._paginate(
            data,
            lambda it: BalanceHistoryByDay(date=it.get("date"), value=it.get("value")),
        )

    def get_address_withdrawals(
        self,
        address: str,
        page: int = 1,
        offset: int = 50,
    ) -> PaginatedResult:
        """Return withdrawals of an address."""
        params = {"page": page, "offset": offset}
        data = self._request_v2(f"/addresses/{address}/withdrawals", params)
        return self._paginate(data, self._parse_internal_tx)

    def get_address_nft_list(
        self,
        address: str,
        page: int = 1,
        offset: int = 50,
    ) -> PaginatedResult:
        """Return list of NFTs owned by the address."""
        params = {"page": page, "offset": offset}
        data = self._request_v2(f"/addresses/{address}/nft", params)
        return self._paginate(data, self._parse_nft_instance)

    def get_address_nft_collections(
        self,
        address: str,
        page: int = 1,
        offset: int = 50,
    ) -> PaginatedResult:
        """Return NFT collections owned by the address."""
        params = {"page": page, "offset": offset}
        data = self._request_v2(f"/addresses/{address}/nft/collections", params)
        return self._paginate(data, self._parse_nft_instance)

    def get_tokens(self, page: int = 1, offset: int = 50) -> PaginatedResult:
        """Return list of tokens."""
        params = {"page": page, "offset": offset}
        data = self._request_v2("/tokens", params)
        return self._paginate(data, self._parse_token)

    def get_token_info(self, address: str) -> Token:
        """Return information about a token."""
        data = self._request_v2(f"/tokens/{address}")
        return self._parse_token(data)

    def get_token_transfers(
        self,
        address: str,
        page: int = 1,
        offset: int = 50,
    ) -> PaginatedResult:
        """Return token transfers for a token."""
        params = {"page": page, "offset": offset}
        data = self._request_v2(f"/tokens/{address}/transfers", params)
        return self._paginate(data, self._parse_transfer)

    def get_token_holders(
        self,
        address: str,
        page: int = 1,
        offset: int = 50,
    ) -> PaginatedResult:
        """Return token holders."""
        params = {"page": page, "offset": offset}
        data = self._request_v2(f"/tokens/{address}/holders", params)
        return self._paginate(
            data,
            lambda it: TokenHolder(
                address=self._parse_address(it.get("address", {})),
                token_id=it.get("token_id"),
                value=it.get("value"),
            ),
        )

    def get_token_counters(self, address: str) -> AddressCounters:
        """Return token counters."""
        data = self._request_v2(f"/tokens/{address}/counters")
        return AddressCounters(
            transactions_count=data.get("transfers_count"),
            token_transfers_count=data.get("token_holders_count"),
            gas_usage_count="0",
            validations_count="0",
        )

    def get_nft_instances(
        self,
        address: str,
        page: int = 1,
        offset: int = 50,
    ) -> PaginatedResult:
        """Return NFT instances for a token."""
        params = {"page": page, "offset": offset}
        data = self._request_v2(f"/tokens/{address}/instances", params)
        return self._paginate(data, self._parse_nft_instance)

    def get_nft_instance(self, address: str, instance_id: str) -> NFTInstance:
        """Return a specific NFT instance."""
        data = self._request_v2(f"/tokens/{address}/instances/{instance_id}")
        return self._parse_nft_instance(data)

    def get_nft_instance_transfers(
        self,
        address: str,
        instance_id: str,
        page: int = 1,
        offset: int = 50,
    ) -> PaginatedResult:
        """Return transfers of an NFT instance."""
        params = {"page": page, "offset": offset}
        data = self._request_v2(
            f"/tokens/{address}/instances/{instance_id}/transfers",
            params,
        )
        return self._paginate(data, self._parse_transfer)

    def get_nft_instance_holders(
        self,
        address: str,
        instance_id: str,
        page: int = 1,
        offset: int = 50,
    ) -> PaginatedResult:
        """Return holders of an NFT instance."""
        params = {"page": page, "offset": offset}
        data = self._request_v2(
            f"/tokens/{address}/instances/{instance_id}/holders",
            params,
        )
        return self._paginate(
            data,
            lambda it: TokenHolder(
                address=self._parse_address(it.get("address", {})),
                token_id=it.get("token_id"),
                value=it.get("value"),
            ),
        )

    def get_nft_instance_transfers_count(self, address: str, instance_id: str) -> int:
        """Return transfer count of an NFT instance."""
        data = self._request_v2(
            f"/tokens/{address}/instances/{instance_id}/transfers-count"
        )
        return int(data.get("count", 0))

    def refetch_nft_metadata(self, address: str, instance_id: str) -> bool:
        """Re-fetch metadata for an NFT instance."""
        data = self._request_v2(
            f"/tokens/{address}/instances/{instance_id}/refetch-metadata",
            method="PATCH",
        )
        return data.get("ok", False)
