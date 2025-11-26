from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.market_chart_item import MarketChartItem


T = TypeVar("T", bound="GetMarketChartResponse200")


@_attrs_define
class GetMarketChartResponse200:
    """
    Attributes:
        available_supply (str):  Example: 164918857.718061.
        chart_data (list['MarketChartItem']):
    """

    available_supply: str
    chart_data: list["MarketChartItem"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        available_supply = self.available_supply

        chart_data = []
        for chart_data_item_data in self.chart_data:
            chart_data_item = chart_data_item_data.to_dict()
            chart_data.append(chart_data_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "available_supply": available_supply,
                "chart_data": chart_data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.market_chart_item import MarketChartItem

        d = dict(src_dict)
        available_supply = d.pop("available_supply")

        chart_data = []
        _chart_data = d.pop("chart_data")
        for chart_data_item_data in _chart_data:
            chart_data_item = MarketChartItem.from_dict(chart_data_item_data)

            chart_data.append(chart_data_item)

        get_market_chart_response_200 = cls(
            available_supply=available_supply,
            chart_data=chart_data,
        )

        get_market_chart_response_200.additional_properties = d
        return get_market_chart_response_200

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
