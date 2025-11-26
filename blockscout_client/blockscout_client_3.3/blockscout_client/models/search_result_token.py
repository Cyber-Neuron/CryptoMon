from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SearchResultToken")


@_attrs_define
class SearchResultToken:
    """
    Attributes:
        address (str):  Example: 0xdAC17F958D2ee523a2206206994597C13D831ec7.
        address_url (str):  Example: /address/0xdAC17F958D2ee523a2206206994597C13D831ec7.
        exchange_rate (str):  Example: 0.999813.
        icon_url (str):  Example: https://raw.githubusercontent.com/trustwallet/assets/master/blockchains/ethereum/asset
            s/0xdAC17F958D2ee523a2206206994597C13D831ec7/logo.png.
        is_smart_contract_verified (bool):  Example: True.
        name (str):  Example: Tether USD.
        symbol (str):  Example: USDT.
        token_type (str):  Example: ERC-20.
        token_url (str):  Example: /token/0xdAC17F958D2ee523a2206206994597C13D831ec7.
        total_supply (str):  Example: 39030615894320966.
        type_ (str):  Example: token.
    """

    address: str
    address_url: str
    exchange_rate: str
    icon_url: str
    is_smart_contract_verified: bool
    name: str
    symbol: str
    token_type: str
    token_url: str
    total_supply: str
    type_: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        address = self.address

        address_url = self.address_url

        exchange_rate = self.exchange_rate

        icon_url = self.icon_url

        is_smart_contract_verified = self.is_smart_contract_verified

        name = self.name

        symbol = self.symbol

        token_type = self.token_type

        token_url = self.token_url

        total_supply = self.total_supply

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "address": address,
                "address_url": address_url,
                "exchange_rate": exchange_rate,
                "icon_url": icon_url,
                "is_smart_contract_verified": is_smart_contract_verified,
                "name": name,
                "symbol": symbol,
                "token_type": token_type,
                "token_url": token_url,
                "total_supply": total_supply,
                "type": type_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        address = d.pop("address")

        address_url = d.pop("address_url")

        exchange_rate = d.pop("exchange_rate")

        icon_url = d.pop("icon_url")

        is_smart_contract_verified = d.pop("is_smart_contract_verified")

        name = d.pop("name")

        symbol = d.pop("symbol")

        token_type = d.pop("token_type")

        token_url = d.pop("token_url")

        total_supply = d.pop("total_supply")

        type_ = d.pop("type")

        search_result_token = cls(
            address=address,
            address_url=address_url,
            exchange_rate=exchange_rate,
            icon_url=icon_url,
            is_smart_contract_verified=is_smart_contract_verified,
            name=name,
            symbol=symbol,
            token_type=token_type,
            token_url=token_url,
            total_supply=total_supply,
            type_=type_,
        )

        search_result_token.additional_properties = d
        return search_result_token

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
