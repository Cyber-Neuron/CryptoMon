from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.transaction_chart_item import TransactionChartItem


T = TypeVar("T", bound="GetTxsChartResponse200")


@_attrs_define
class GetTxsChartResponse200:
    """
    Attributes:
        chart_data (list['TransactionChartItem']):
    """

    chart_data: list["TransactionChartItem"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        chart_data = []
        for chart_data_item_data in self.chart_data:
            chart_data_item = chart_data_item_data.to_dict()
            chart_data.append(chart_data_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "chart_data": chart_data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.transaction_chart_item import TransactionChartItem

        d = dict(src_dict)
        chart_data = []
        _chart_data = d.pop("chart_data")
        for chart_data_item_data in _chart_data:
            chart_data_item = TransactionChartItem.from_dict(chart_data_item_data)

            chart_data.append(chart_data_item)

        get_txs_chart_response_200 = cls(
            chart_data=chart_data,
        )

        get_txs_chart_response_200.additional_properties = d
        return get_txs_chart_response_200

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
