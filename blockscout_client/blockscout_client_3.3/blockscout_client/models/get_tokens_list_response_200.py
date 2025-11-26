from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.get_tokens_list_response_200_next_page_params import GetTokensListResponse200NextPageParams
    from ..models.token_info import TokenInfo


T = TypeVar("T", bound="GetTokensListResponse200")


@_attrs_define
class GetTokensListResponse200:
    """
    Attributes:
        items (list['TokenInfo']):
        next_page_params (GetTokensListResponse200NextPageParams):  Example: {'contract_address_hash':
            '0x68749665ff8d2d112fa859aa293f07a622782f38', 'holder_count': 1011, 'is_name_null': False, 'items_count': 50,
            'market_cap': '482534473.2170469', 'name': 'Tether Gold'}.
    """

    items: list["TokenInfo"]
    next_page_params: "GetTokensListResponse200NextPageParams"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        next_page_params = self.next_page_params.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "items": items,
                "next_page_params": next_page_params,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_tokens_list_response_200_next_page_params import GetTokensListResponse200NextPageParams
        from ..models.token_info import TokenInfo

        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = TokenInfo.from_dict(items_item_data)

            items.append(items_item)

        next_page_params = GetTokensListResponse200NextPageParams.from_dict(d.pop("next_page_params"))

        get_tokens_list_response_200 = cls(
            items=items,
            next_page_params=next_page_params,
        )

        get_tokens_list_response_200.additional_properties = d
        return get_tokens_list_response_200

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
