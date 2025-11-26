from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v1_entry_point_indexer_status import V1EntryPointIndexerStatus


T = TypeVar("T", bound="V1IndexerStatus")


@_attrs_define
class V1IndexerStatus:
    """
    Attributes:
        finished_past_indexing (Union[Unset, bool]):
        v06 (Union[Unset, V1EntryPointIndexerStatus]):
        v07 (Union[Unset, V1EntryPointIndexerStatus]):
    """

    finished_past_indexing: Union[Unset, bool] = UNSET
    v06: Union[Unset, "V1EntryPointIndexerStatus"] = UNSET
    v07: Union[Unset, "V1EntryPointIndexerStatus"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        finished_past_indexing = self.finished_past_indexing

        v06: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.v06, Unset):
            v06 = self.v06.to_dict()

        v07: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.v07, Unset):
            v07 = self.v07.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if finished_past_indexing is not UNSET:
            field_dict["finished_past_indexing"] = finished_past_indexing
        if v06 is not UNSET:
            field_dict["v06"] = v06
        if v07 is not UNSET:
            field_dict["v07"] = v07

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v1_entry_point_indexer_status import V1EntryPointIndexerStatus

        d = dict(src_dict)
        finished_past_indexing = d.pop("finished_past_indexing", UNSET)

        _v06 = d.pop("v06", UNSET)
        v06: Union[Unset, V1EntryPointIndexerStatus]
        if isinstance(_v06, Unset):
            v06 = UNSET
        else:
            v06 = V1EntryPointIndexerStatus.from_dict(_v06)

        _v07 = d.pop("v07", UNSET)
        v07: Union[Unset, V1EntryPointIndexerStatus]
        if isinstance(_v07, Unset):
            v07 = UNSET
        else:
            v07 = V1EntryPointIndexerStatus.from_dict(_v07)

        v1_indexer_status = cls(
            finished_past_indexing=finished_past_indexing,
            v06=v06,
            v07=v07,
        )

        v1_indexer_status.additional_properties = d
        return v1_indexer_status

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
