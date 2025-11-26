from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GetTokensListResponse200NextPageParams")


@_attrs_define
class GetTokensListResponse200NextPageParams:
    """
    Example:
        {'contract_address_hash': '0x68749665ff8d2d112fa859aa293f07a622782f38', 'holder_count': 1011, 'is_name_null':
            False, 'items_count': 50, 'market_cap': '482534473.2170469', 'name': 'Tether Gold'}

    """

    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        get_tokens_list_response_200_next_page_params = cls()

        get_tokens_list_response_200_next_page_params.additional_properties = d
        return get_tokens_list_response_200_next_page_params

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
