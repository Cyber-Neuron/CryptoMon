from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RawTraceCallResult")


@_attrs_define
class RawTraceCallResult:
    """
    Attributes:
        gas_used (str):  Example: 0x25D3FC.
        output (str):  Example: 0x0.
    """

    gas_used: str
    output: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        gas_used = self.gas_used

        output = self.output

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "gasUsed": gas_used,
                "output": output,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        gas_used = d.pop("gasUsed")

        output = d.pop("output")

        raw_trace_call_result = cls(
            gas_used=gas_used,
            output=output,
        )

        raw_trace_call_result.additional_properties = d
        return raw_trace_call_result

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
