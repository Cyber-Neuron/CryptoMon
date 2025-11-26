from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.get_block_txs_response_200_next_page_params import GetBlockTxsResponse200NextPageParams
    from ..models.transaction import Transaction


T = TypeVar("T", bound="GetBlockTxsResponse200")


@_attrs_define
class GetBlockTxsResponse200:
    """
    Attributes:
        items (list['Transaction']):
        next_page_params (GetBlockTxsResponse200NextPageParams):  Example: {'block_number': 27736955, 'index': 4,
            'items_count': 50}.
    """

    items: list["Transaction"]
    next_page_params: "GetBlockTxsResponse200NextPageParams"
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
        from ..models.get_block_txs_response_200_next_page_params import GetBlockTxsResponse200NextPageParams
        from ..models.transaction import Transaction

        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = Transaction.from_dict(items_item_data)

            items.append(items_item)

        next_page_params = GetBlockTxsResponse200NextPageParams.from_dict(d.pop("next_page_params"))

        get_block_txs_response_200 = cls(
            items=items,
            next_page_params=next_page_params,
        )

        get_block_txs_response_200.additional_properties = d
        return get_block_txs_response_200

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
