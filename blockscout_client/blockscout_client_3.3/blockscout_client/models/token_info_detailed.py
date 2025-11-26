from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="TokenInfoDetailed")


@_attrs_define
class TokenInfoDetailed:
    """
    Attributes:
        address (str): Token Address Example: 0xBEEF69Ac7870777598A04B2bd4771c71212E6aBc.
        circulating_market_cap (str): Token circulating market cap Example: 0.0.
        decimals (str): Token decimals Example: 18.
        exchange_rate (str): Token exchange rate Example: 2890.96.
        holders (str): Token holders amount Example: 2999.
        icon_url (str): Token image URL  Example:
            https://assets.coingecko.com/coins/images/39410/small/Steakhouse_logo-05.jpg?1722053893.
        name (str): Token name Example: Steakhouse Resteaking Vault.
        symbol (str): Token symbol Example: steakLRT.
        total_supply (str): Token total supply Example: 9710057205959239302188.
        type_ (str): Token type Example: ERC-20.
        volume_24h (str): Token trading volume for past 24h Example: 24298.765344836862.
    """

    address: str
    circulating_market_cap: str
    decimals: str
    exchange_rate: str
    holders: str
    icon_url: str
    name: str
    symbol: str
    total_supply: str
    type_: str
    volume_24h: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        address = self.address

        circulating_market_cap = self.circulating_market_cap

        decimals = self.decimals

        exchange_rate = self.exchange_rate

        holders = self.holders

        icon_url = self.icon_url

        name = self.name

        symbol = self.symbol

        total_supply = self.total_supply

        type_ = self.type_

        volume_24h = self.volume_24h

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "address": address,
                "circulating_market_cap": circulating_market_cap,
                "decimals": decimals,
                "exchange_rate": exchange_rate,
                "holders": holders,
                "icon_url": icon_url,
                "name": name,
                "symbol": symbol,
                "total_supply": total_supply,
                "type": type_,
                "volume_24h": volume_24h,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        address = d.pop("address")

        circulating_market_cap = d.pop("circulating_market_cap")

        decimals = d.pop("decimals")

        exchange_rate = d.pop("exchange_rate")

        holders = d.pop("holders")

        icon_url = d.pop("icon_url")

        name = d.pop("name")

        symbol = d.pop("symbol")

        total_supply = d.pop("total_supply")

        type_ = d.pop("type")

        volume_24h = d.pop("volume_24h")

        token_info_detailed = cls(
            address=address,
            circulating_market_cap=circulating_market_cap,
            decimals=decimals,
            exchange_rate=exchange_rate,
            holders=holders,
            icon_url=icon_url,
            name=name,
            symbol=symbol,
            total_supply=total_supply,
            type_=type_,
            volume_24h=volume_24h,
        )

        token_info_detailed.additional_properties = d
        return token_info_detailed

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
