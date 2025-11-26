from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v1_data import V1Data


T = TypeVar("T", bound="V1HealthCheckResponse")


@_attrs_define
class V1HealthCheckResponse:
    """
    Attributes:
        healthy (Union[Unset, bool]):
        data (Union[Unset, V1Data]):
    """

    healthy: Union[Unset, bool] = UNSET
    data: Union[Unset, "V1Data"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        healthy = self.healthy

        data: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.data, Unset):
            data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if healthy is not UNSET:
            field_dict["healthy"] = healthy
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v1_data import V1Data

        d = dict(src_dict)
        healthy = d.pop("healthy", UNSET)

        _data = d.pop("data", UNSET)
        data: Union[Unset, V1Data]
        if isinstance(_data, Unset):
            data = UNSET
        else:
            data = V1Data.from_dict(_data)

        v1_health_check_response = cls(
            healthy=healthy,
            data=data,
        )

        v1_health_check_response.additional_properties = d
        return v1_health_check_response

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
