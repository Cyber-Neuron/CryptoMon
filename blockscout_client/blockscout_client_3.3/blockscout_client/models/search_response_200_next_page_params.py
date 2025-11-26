from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SearchResponse200NextPageParams")


@_attrs_define
class SearchResponse200NextPageParams:
    """
    Example:
        {'address_hash': '0x052Ad78E3aA0b0F2D3912FD3b50a9a289CF2f7Aa', 'block_hash': None, 'holder_count': 548,
            'inserted_at': '2021-12-07T08:39:01.062253Z', 'item_type': 'token', 'items_count': 50, 'name': 'RealToken S
            13245 Monica St Detroit MI', 'q': '1', 'transaction_hash': None}

    """

    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        search_response_200_next_page_params = cls()

        search_response_200_next_page_params.additional_properties = d
        return search_response_200_next_page_params

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
