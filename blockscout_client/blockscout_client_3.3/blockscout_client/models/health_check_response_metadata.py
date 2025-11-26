from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.latest_block import LatestBlock


T = TypeVar("T", bound="HealthCheckResponseMetadata")


@_attrs_define
class HealthCheckResponseMetadata:
    """
    Attributes:
        latest_block (Union[Unset, LatestBlock]):
    """

    latest_block: Union[Unset, "LatestBlock"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        latest_block: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.latest_block, Unset):
            latest_block = self.latest_block.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if latest_block is not UNSET:
            field_dict["latest_block"] = latest_block

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.latest_block import LatestBlock

        d = dict(src_dict)
        _latest_block = d.pop("latest_block", UNSET)
        latest_block: Union[Unset, LatestBlock]
        if isinstance(_latest_block, Unset):
            latest_block = UNSET
        else:
            latest_block = LatestBlock.from_dict(_latest_block)

        health_check_response_metadata = cls(
            latest_block=latest_block,
        )

        health_check_response_metadata.additional_properties = d
        return health_check_response_metadata

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
