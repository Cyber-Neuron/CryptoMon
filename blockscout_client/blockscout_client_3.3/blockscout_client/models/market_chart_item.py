from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MarketChartItem")


@_attrs_define
class MarketChartItem:
    """
    Attributes:
        date (str):  Example: 2022-10-31.
        closing_price (str):  Example: 0.00254915.
        market_cap (str):  Example: 420471.10604559750644.
    """

    date: str
    closing_price: str
    market_cap: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        date = self.date

        closing_price = self.closing_price

        market_cap = self.market_cap

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "date": date,
                "closing_price": closing_price,
                "market_cap": market_cap,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        date = d.pop("date")

        closing_price = d.pop("closing_price")

        market_cap = d.pop("market_cap")

        market_chart_item = cls(
            date=date,
            closing_price=closing_price,
            market_cap=market_cap,
        )

        market_chart_item.additional_properties = d
        return market_chart_item

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
