from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CoinBalanceHistoryEntry")


@_attrs_define
class CoinBalanceHistoryEntry:
    """
    Attributes:
        block_number (int):  Example: 1584930.
        block_timestamp (str):  Example: 2022-08-02T07:18:05.000000Z.
        delta (str):  Example: -234959404.
        value (str):  Example: 100232323.
        transaction_hash (Union[Unset, str]):  Example:
            0x1f610ff9c1efad6b5a8bb6afcc0786cd7343f03f9a61e2544fcff908cedee924.
    """

    block_number: int
    block_timestamp: str
    delta: str
    value: str
    transaction_hash: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        block_number = self.block_number

        block_timestamp = self.block_timestamp

        delta = self.delta

        value = self.value

        transaction_hash = self.transaction_hash

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "block_number": block_number,
                "block_timestamp": block_timestamp,
                "delta": delta,
                "value": value,
            }
        )
        if transaction_hash is not UNSET:
            field_dict["transaction_hash"] = transaction_hash

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        block_number = d.pop("block_number")

        block_timestamp = d.pop("block_timestamp")

        delta = d.pop("delta")

        value = d.pop("value")

        transaction_hash = d.pop("transaction_hash", UNSET)

        coin_balance_history_entry = cls(
            block_number=block_number,
            block_timestamp=block_timestamp,
            delta=delta,
            value=value,
            transaction_hash=transaction_hash,
        )

        coin_balance_history_entry.additional_properties = d
        return coin_balance_history_entry

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
