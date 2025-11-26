from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SearchResultTransaction")


@_attrs_define
class SearchResultTransaction:
    """
    Attributes:
        timestamp (str):  Example: 2022-10-31T07:18:05.000000Z.
        transaction_hash (str):  Example: 0xe38c6772f33edfbd218f59853befe18391cb786f911fb6c0b00ed6dd72ef6e69.
        type_ (str):  Example: transaction.
        url (str):  Example: /xdai/mainnet/tx/0xe38c6772f33edfbd218f59853befe18391cb786f911fb6c0b00ed6dd72ef6e69.
    """

    timestamp: str
    transaction_hash: str
    type_: str
    url: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        timestamp = self.timestamp

        transaction_hash = self.transaction_hash

        type_ = self.type_

        url = self.url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "timestamp": timestamp,
                "transaction_hash": transaction_hash,
                "type": type_,
                "url": url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        timestamp = d.pop("timestamp")

        transaction_hash = d.pop("transaction_hash")

        type_ = d.pop("type")

        url = d.pop("url")

        search_result_transaction = cls(
            timestamp=timestamp,
            transaction_hash=transaction_hash,
            type_=type_,
            url=url,
        )

        search_result_transaction.additional_properties = d
        return search_result_transaction

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
