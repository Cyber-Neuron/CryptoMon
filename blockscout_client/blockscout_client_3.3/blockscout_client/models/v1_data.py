from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="V1Data")


@_attrs_define
class V1Data:
    """
    Attributes:
        cache_latest_block_inserted_at (Union[Unset, str]):
        cache_latest_block_number (Union[Unset, str]):
        latest_block_inserted_at (Union[Unset, str]):
        latest_block_number (Union[Unset, str]):
    """

    cache_latest_block_inserted_at: Union[Unset, str] = UNSET
    cache_latest_block_number: Union[Unset, str] = UNSET
    latest_block_inserted_at: Union[Unset, str] = UNSET
    latest_block_number: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cache_latest_block_inserted_at = self.cache_latest_block_inserted_at

        cache_latest_block_number = self.cache_latest_block_number

        latest_block_inserted_at = self.latest_block_inserted_at

        latest_block_number = self.latest_block_number

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cache_latest_block_inserted_at is not UNSET:
            field_dict["cache_latest_block_inserted_at"] = cache_latest_block_inserted_at
        if cache_latest_block_number is not UNSET:
            field_dict["cache_latest_block_number"] = cache_latest_block_number
        if latest_block_inserted_at is not UNSET:
            field_dict["latest_block_inserted_at"] = latest_block_inserted_at
        if latest_block_number is not UNSET:
            field_dict["latest_block_number"] = latest_block_number

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cache_latest_block_inserted_at = d.pop("cache_latest_block_inserted_at", UNSET)

        cache_latest_block_number = d.pop("cache_latest_block_number", UNSET)

        latest_block_inserted_at = d.pop("latest_block_inserted_at", UNSET)

        latest_block_number = d.pop("latest_block_number", UNSET)

        v1_data = cls(
            cache_latest_block_inserted_at=cache_latest_block_inserted_at,
            cache_latest_block_number=cache_latest_block_number,
            latest_block_inserted_at=latest_block_inserted_at,
            latest_block_number=latest_block_number,
        )

        v1_data.additional_properties = d
        return v1_data

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
