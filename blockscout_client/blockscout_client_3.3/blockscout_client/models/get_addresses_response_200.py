from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.address_with_tx_count import AddressWithTxCount
    from ..models.get_addresses_response_200_next_page_params import GetAddressesResponse200NextPageParams


T = TypeVar("T", bound="GetAddressesResponse200")


@_attrs_define
class GetAddressesResponse200:
    """
    Attributes:
        exchange_rate (str):  Example: 0.01.
        total_supply (str):  Example: 100000000.
        items (list['AddressWithTxCount']):
        next_page_params (GetAddressesResponse200NextPageParams):  Example: {'fetched_coin_balance':
            '269536604956070000000', 'hash': '0xf74769d9ffe1cd17f20b283995cf9e7fa2a262ed', 'items_count': 50}.
    """

    exchange_rate: str
    total_supply: str
    items: list["AddressWithTxCount"]
    next_page_params: "GetAddressesResponse200NextPageParams"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        exchange_rate = self.exchange_rate

        total_supply = self.total_supply

        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        next_page_params = self.next_page_params.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "exchange_rate": exchange_rate,
                "total_supply": total_supply,
                "items": items,
                "next_page_params": next_page_params,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.address_with_tx_count import AddressWithTxCount
        from ..models.get_addresses_response_200_next_page_params import GetAddressesResponse200NextPageParams

        d = dict(src_dict)
        exchange_rate = d.pop("exchange_rate")

        total_supply = d.pop("total_supply")

        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = AddressWithTxCount.from_dict(items_item_data)

            items.append(items_item)

        next_page_params = GetAddressesResponse200NextPageParams.from_dict(d.pop("next_page_params"))

        get_addresses_response_200 = cls(
            exchange_rate=exchange_rate,
            total_supply=total_supply,
            items=items,
            next_page_params=next_page_params,
        )

        get_addresses_response_200.additional_properties = d
        return get_addresses_response_200

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
