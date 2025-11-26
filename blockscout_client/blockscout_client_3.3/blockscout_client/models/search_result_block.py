from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SearchResultBlock")


@_attrs_define
class SearchResultBlock:
    """
    Attributes:
        block_hash (str):  Example: 0xba83e9ba0b43e8d112a07fdab08d53f473d2b7fb0e585bd437ae739933db203e.
        block_number (int):  Example: 24816691.
        timestamp (str):  Example: 2022-10-31T07:18:05.000000Z.
        type_ (str):  Example: block.
        url (str):  Example: /xdai/mainnet/block/0xba83e9ba0b43e8d112a07fdab08d53f473d2b7fb0e585bd437ae739933db203e.
    """

    block_hash: str
    block_number: int
    timestamp: str
    type_: str
    url: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        block_hash = self.block_hash

        block_number = self.block_number

        timestamp = self.timestamp

        type_ = self.type_

        url = self.url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "block_hash": block_hash,
                "block_number": block_number,
                "timestamp": timestamp,
                "type": type_,
                "url": url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        block_hash = d.pop("block_hash")

        block_number = d.pop("block_number")

        timestamp = d.pop("timestamp")

        type_ = d.pop("type")

        url = d.pop("url")

        search_result_block = cls(
            block_hash=block_hash,
            block_number=block_number,
            timestamp=timestamp,
            type_=type_,
            url=url,
        )

        search_result_block.additional_properties = d
        return search_result_block

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
