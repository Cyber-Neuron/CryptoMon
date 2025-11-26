from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.summary import Summary


T = TypeVar("T", bound="TransactionSummaryObj")


@_attrs_define
class TransactionSummaryObj:
    """
    Attributes:
        summaries (Union[Unset, list['Summary']]):
    """

    summaries: Union[Unset, list["Summary"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        summaries: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.summaries, Unset):
            summaries = []
            for summaries_item_data in self.summaries:
                summaries_item = summaries_item_data.to_dict()
                summaries.append(summaries_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if summaries is not UNSET:
            field_dict["summaries"] = summaries

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.summary import Summary

        d = dict(src_dict)
        summaries = []
        _summaries = d.pop("summaries", UNSET)
        for summaries_item_data in _summaries or []:
            summaries_item = Summary.from_dict(summaries_item_data)

            summaries.append(summaries_item)

        transaction_summary_obj = cls(
            summaries=summaries,
        )

        transaction_summary_obj.additional_properties = d
        return transaction_summary_obj

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
