from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="Token")


@_attrs_define
class Token:
    """
    Attributes:
        name (str):  Example: Tether USD.
        decimals (str):  Example: 16.
        symbol (str):  Example: USDT.
        address (str):  Example: 0x394c399dbA25B99Ab7708EdB505d755B3aa29997.
        type_ (str):  Example: ERC-20.
        holders (int):  Example: 837494234523.
        exchange_rate (str):  Example: 0.99.
        total_supply (str):  Example: 10000000.
    """

    name: str
    decimals: str
    symbol: str
    address: str
    type_: str
    holders: int
    exchange_rate: str
    total_supply: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        decimals = self.decimals

        symbol = self.symbol

        address = self.address

        type_ = self.type_

        holders = self.holders

        exchange_rate = self.exchange_rate

        total_supply = self.total_supply

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "decimals": decimals,
                "symbol": symbol,
                "address": address,
                "type": type_,
                "holders": holders,
                "exchange_rate": exchange_rate,
                "total_supply": total_supply,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        decimals = d.pop("decimals")

        symbol = d.pop("symbol")

        address = d.pop("address")

        type_ = d.pop("type")

        holders = d.pop("holders")

        exchange_rate = d.pop("exchange_rate")

        total_supply = d.pop("total_supply")

        token = cls(
            name=name,
            decimals=decimals,
            symbol=symbol,
            address=address,
            type_=type_,
            holders=holders,
            exchange_rate=exchange_rate,
            total_supply=total_supply,
        )

        token.additional_properties = d
        return token

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
