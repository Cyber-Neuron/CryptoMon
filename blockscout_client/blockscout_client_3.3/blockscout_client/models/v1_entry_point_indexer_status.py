from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="V1EntryPointIndexerStatus")


@_attrs_define
class V1EntryPointIndexerStatus:
    """
    Attributes:
        enabled (Union[Unset, bool]):
        live (Union[Unset, bool]):
        past_db_logs_indexing_finished (Union[Unset, bool]):
        past_rpc_logs_indexing_finished (Union[Unset, bool]):
    """

    enabled: Union[Unset, bool] = UNSET
    live: Union[Unset, bool] = UNSET
    past_db_logs_indexing_finished: Union[Unset, bool] = UNSET
    past_rpc_logs_indexing_finished: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        live = self.live

        past_db_logs_indexing_finished = self.past_db_logs_indexing_finished

        past_rpc_logs_indexing_finished = self.past_rpc_logs_indexing_finished

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if live is not UNSET:
            field_dict["live"] = live
        if past_db_logs_indexing_finished is not UNSET:
            field_dict["past_db_logs_indexing_finished"] = past_db_logs_indexing_finished
        if past_rpc_logs_indexing_finished is not UNSET:
            field_dict["past_rpc_logs_indexing_finished"] = past_rpc_logs_indexing_finished

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        enabled = d.pop("enabled", UNSET)

        live = d.pop("live", UNSET)

        past_db_logs_indexing_finished = d.pop("past_db_logs_indexing_finished", UNSET)

        past_rpc_logs_indexing_finished = d.pop("past_rpc_logs_indexing_finished", UNSET)

        v1_entry_point_indexer_status = cls(
            enabled=enabled,
            live=live,
            past_db_logs_indexing_finished=past_db_logs_indexing_finished,
            past_rpc_logs_indexing_finished=past_rpc_logs_indexing_finished,
        )

        v1_entry_point_indexer_status.additional_properties = d
        return v1_entry_point_indexer_status

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
