from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RawTraceCreateResult")


@_attrs_define
class RawTraceCreateResult:
    """
    Attributes:
        address (str):  Example: 0xf57b55b01b831e602e09674a4e5d69cbcf343f98.
        code (str):  Example: 0x25D3FC.
        gas_used (str):  Example: 0x25D3FC.
    """

    address: str
    code: str
    gas_used: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        address = self.address

        code = self.code

        gas_used = self.gas_used

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "address": address,
                "code": code,
                "gasUsed": gas_used,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        address = d.pop("address")

        code = d.pop("code")

        gas_used = d.pop("gasUsed")

        raw_trace_create_result = cls(
            address=address,
            code=code,
            gas_used=gas_used,
        )

        raw_trace_create_result.additional_properties = d
        return raw_trace_create_result

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
