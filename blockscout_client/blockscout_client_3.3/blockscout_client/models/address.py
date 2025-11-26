from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.address_tag import AddressTag
    from ..models.token_info import TokenInfo
    from ..models.watchlist_name import WatchlistName


T = TypeVar("T", bound="Address")


@_attrs_define
class Address:
    """
    Attributes:
        hash_ (str):  Example: 0xEb533ee5687044E622C69c58B1B12329F56eD9ad.
        creator_address_hash (Union[Unset, str]):  Example: 0xEb533ee5687044E622C69c58B1B12329F56eD9ad.
        creation_transaction_hash (Union[Unset, str]):  Example:
            0x1f610ff9c1efad6b5a8bb6afcc0786cd7343f03f9a61e2544fcff908cedee924.
        token (Union[Unset, TokenInfo]):
        coin_balance (Union[Unset, str]):  Example: 10000000.
        exchange_rate (Union[Unset, str]):  Example: 1.01.
        implementation_address (Union[Unset, str]):  Example: 0xEb533ee5687044E622C69c58B1B12329F56eD9ad.
        block_number_balance_updated_at (Union[Unset, int]):  Example: 27656552.
        implementation_name (Union[Unset, str]):  Example: implementationName.
        name (Union[Unset, str]):  Example: contractName.
        is_contract (Union[Unset, bool]):
        private_tags (Union[Unset, list['AddressTag']]):
        watchlist_names (Union[Unset, list['WatchlistName']]):
        public_tags (Union[Unset, list['AddressTag']]):
        is_verified (Union[Unset, bool]):
        has_beacon_chain_withdrawals (Union[Unset, bool]):
        has_custom_methods_read (Union[Unset, bool]):
        has_custom_methods_write (Union[Unset, bool]):
        has_decompiled_code (Union[Unset, bool]):
        has_logs (Union[Unset, bool]):
        has_methods_read (Union[Unset, bool]):
        has_methods_write (Union[Unset, bool]):
        has_methods_read_proxy (Union[Unset, bool]):
        has_methods_write_proxy (Union[Unset, bool]):
        has_token_transfers (Union[Unset, bool]):
        has_tokens (Union[Unset, bool]):
        has_validated_blocks (Union[Unset, bool]):
    """

    hash_: str
    creator_address_hash: Union[Unset, str] = UNSET
    creation_transaction_hash: Union[Unset, str] = UNSET
    token: Union[Unset, "TokenInfo"] = UNSET
    coin_balance: Union[Unset, str] = UNSET
    exchange_rate: Union[Unset, str] = UNSET
    implementation_address: Union[Unset, str] = UNSET
    block_number_balance_updated_at: Union[Unset, int] = UNSET
    implementation_name: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    is_contract: Union[Unset, bool] = UNSET
    private_tags: Union[Unset, list["AddressTag"]] = UNSET
    watchlist_names: Union[Unset, list["WatchlistName"]] = UNSET
    public_tags: Union[Unset, list["AddressTag"]] = UNSET
    is_verified: Union[Unset, bool] = UNSET
    has_beacon_chain_withdrawals: Union[Unset, bool] = UNSET
    has_custom_methods_read: Union[Unset, bool] = UNSET
    has_custom_methods_write: Union[Unset, bool] = UNSET
    has_decompiled_code: Union[Unset, bool] = UNSET
    has_logs: Union[Unset, bool] = UNSET
    has_methods_read: Union[Unset, bool] = UNSET
    has_methods_write: Union[Unset, bool] = UNSET
    has_methods_read_proxy: Union[Unset, bool] = UNSET
    has_methods_write_proxy: Union[Unset, bool] = UNSET
    has_token_transfers: Union[Unset, bool] = UNSET
    has_tokens: Union[Unset, bool] = UNSET
    has_validated_blocks: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        hash_ = self.hash_

        creator_address_hash = self.creator_address_hash

        creation_transaction_hash = self.creation_transaction_hash

        token: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.token, Unset):
            token = self.token.to_dict()

        coin_balance = self.coin_balance

        exchange_rate = self.exchange_rate

        implementation_address = self.implementation_address

        block_number_balance_updated_at = self.block_number_balance_updated_at

        implementation_name = self.implementation_name

        name = self.name

        is_contract = self.is_contract

        private_tags: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.private_tags, Unset):
            private_tags = []
            for private_tags_item_data in self.private_tags:
                private_tags_item = private_tags_item_data.to_dict()
                private_tags.append(private_tags_item)

        watchlist_names: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.watchlist_names, Unset):
            watchlist_names = []
            for watchlist_names_item_data in self.watchlist_names:
                watchlist_names_item = watchlist_names_item_data.to_dict()
                watchlist_names.append(watchlist_names_item)

        public_tags: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.public_tags, Unset):
            public_tags = []
            for public_tags_item_data in self.public_tags:
                public_tags_item = public_tags_item_data.to_dict()
                public_tags.append(public_tags_item)

        is_verified = self.is_verified

        has_beacon_chain_withdrawals = self.has_beacon_chain_withdrawals

        has_custom_methods_read = self.has_custom_methods_read

        has_custom_methods_write = self.has_custom_methods_write

        has_decompiled_code = self.has_decompiled_code

        has_logs = self.has_logs

        has_methods_read = self.has_methods_read

        has_methods_write = self.has_methods_write

        has_methods_read_proxy = self.has_methods_read_proxy

        has_methods_write_proxy = self.has_methods_write_proxy

        has_token_transfers = self.has_token_transfers

        has_tokens = self.has_tokens

        has_validated_blocks = self.has_validated_blocks

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "hash": hash_,
            }
        )
        if creator_address_hash is not UNSET:
            field_dict["creator_address_hash"] = creator_address_hash
        if creation_transaction_hash is not UNSET:
            field_dict["creation_transaction_hash"] = creation_transaction_hash
        if token is not UNSET:
            field_dict["token"] = token
        if coin_balance is not UNSET:
            field_dict["coin_balance"] = coin_balance
        if exchange_rate is not UNSET:
            field_dict["exchange_rate"] = exchange_rate
        if implementation_address is not UNSET:
            field_dict["implementation_address"] = implementation_address
        if block_number_balance_updated_at is not UNSET:
            field_dict["block_number_balance_updated_at"] = block_number_balance_updated_at
        if implementation_name is not UNSET:
            field_dict["implementation_name"] = implementation_name
        if name is not UNSET:
            field_dict["name"] = name
        if is_contract is not UNSET:
            field_dict["is_contract"] = is_contract
        if private_tags is not UNSET:
            field_dict["private_tags"] = private_tags
        if watchlist_names is not UNSET:
            field_dict["watchlist_names"] = watchlist_names
        if public_tags is not UNSET:
            field_dict["public_tags"] = public_tags
        if is_verified is not UNSET:
            field_dict["is_verified"] = is_verified
        if has_beacon_chain_withdrawals is not UNSET:
            field_dict["has_beacon_chain_withdrawals"] = has_beacon_chain_withdrawals
        if has_custom_methods_read is not UNSET:
            field_dict["has_custom_methods_read"] = has_custom_methods_read
        if has_custom_methods_write is not UNSET:
            field_dict["has_custom_methods_write"] = has_custom_methods_write
        if has_decompiled_code is not UNSET:
            field_dict["has_decompiled_code"] = has_decompiled_code
        if has_logs is not UNSET:
            field_dict["has_logs"] = has_logs
        if has_methods_read is not UNSET:
            field_dict["has_methods_read"] = has_methods_read
        if has_methods_write is not UNSET:
            field_dict["has_methods_write"] = has_methods_write
        if has_methods_read_proxy is not UNSET:
            field_dict["has_methods_read_proxy"] = has_methods_read_proxy
        if has_methods_write_proxy is not UNSET:
            field_dict["has_methods_write_proxy"] = has_methods_write_proxy
        if has_token_transfers is not UNSET:
            field_dict["has_token_transfers"] = has_token_transfers
        if has_tokens is not UNSET:
            field_dict["has_tokens"] = has_tokens
        if has_validated_blocks is not UNSET:
            field_dict["has_validated_blocks"] = has_validated_blocks

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.address_tag import AddressTag
        from ..models.token_info import TokenInfo
        from ..models.watchlist_name import WatchlistName

        d = dict(src_dict)
        hash_ = d.pop("hash")

        creator_address_hash = d.pop("creator_address_hash", UNSET)

        creation_transaction_hash = d.pop("creation_transaction_hash", UNSET)

        _token = d.pop("token", UNSET)
        token: Union[Unset, TokenInfo]
        if isinstance(_token, Unset):
            token = UNSET
        else:
            token = TokenInfo.from_dict(_token)

        coin_balance = d.pop("coin_balance", UNSET)

        exchange_rate = d.pop("exchange_rate", UNSET)

        implementation_address = d.pop("implementation_address", UNSET)

        block_number_balance_updated_at = d.pop("block_number_balance_updated_at", UNSET)

        implementation_name = d.pop("implementation_name", UNSET)

        name = d.pop("name", UNSET)

        is_contract = d.pop("is_contract", UNSET)

        private_tags = []
        _private_tags = d.pop("private_tags", UNSET)
        for private_tags_item_data in _private_tags or []:
            private_tags_item = AddressTag.from_dict(private_tags_item_data)

            private_tags.append(private_tags_item)

        watchlist_names = []
        _watchlist_names = d.pop("watchlist_names", UNSET)
        for watchlist_names_item_data in _watchlist_names or []:
            watchlist_names_item = WatchlistName.from_dict(watchlist_names_item_data)

            watchlist_names.append(watchlist_names_item)

        public_tags = []
        _public_tags = d.pop("public_tags", UNSET)
        for public_tags_item_data in _public_tags or []:
            public_tags_item = AddressTag.from_dict(public_tags_item_data)

            public_tags.append(public_tags_item)

        is_verified = d.pop("is_verified", UNSET)

        has_beacon_chain_withdrawals = d.pop("has_beacon_chain_withdrawals", UNSET)

        has_custom_methods_read = d.pop("has_custom_methods_read", UNSET)

        has_custom_methods_write = d.pop("has_custom_methods_write", UNSET)

        has_decompiled_code = d.pop("has_decompiled_code", UNSET)

        has_logs = d.pop("has_logs", UNSET)

        has_methods_read = d.pop("has_methods_read", UNSET)

        has_methods_write = d.pop("has_methods_write", UNSET)

        has_methods_read_proxy = d.pop("has_methods_read_proxy", UNSET)

        has_methods_write_proxy = d.pop("has_methods_write_proxy", UNSET)

        has_token_transfers = d.pop("has_token_transfers", UNSET)

        has_tokens = d.pop("has_tokens", UNSET)

        has_validated_blocks = d.pop("has_validated_blocks", UNSET)

        address = cls(
            hash_=hash_,
            creator_address_hash=creator_address_hash,
            creation_transaction_hash=creation_transaction_hash,
            token=token,
            coin_balance=coin_balance,
            exchange_rate=exchange_rate,
            implementation_address=implementation_address,
            block_number_balance_updated_at=block_number_balance_updated_at,
            implementation_name=implementation_name,
            name=name,
            is_contract=is_contract,
            private_tags=private_tags,
            watchlist_names=watchlist_names,
            public_tags=public_tags,
            is_verified=is_verified,
            has_beacon_chain_withdrawals=has_beacon_chain_withdrawals,
            has_custom_methods_read=has_custom_methods_read,
            has_custom_methods_write=has_custom_methods_write,
            has_decompiled_code=has_decompiled_code,
            has_logs=has_logs,
            has_methods_read=has_methods_read,
            has_methods_write=has_methods_write,
            has_methods_read_proxy=has_methods_read_proxy,
            has_methods_write_proxy=has_methods_write_proxy,
            has_token_transfers=has_token_transfers,
            has_tokens=has_tokens,
            has_validated_blocks=has_validated_blocks,
        )

        address.additional_properties = d
        return address

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
