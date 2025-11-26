from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DecodedInputLogParameter")


@_attrs_define
class DecodedInputLogParameter:
    """
    Attributes:
        name (str):  Example: signature.
        type_ (str):  Example: bytes.
        value (str):  Example: 0x0.
        indexed (bool):
    """

    name: str
    type_: str
    value: str
    indexed: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        type_ = self.type_

        value = self.value

        indexed = self.indexed

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "type": type_,
                "value": value,
                "indexed": indexed,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        type_ = d.pop("type")

        value = d.pop("value")

        indexed = d.pop("indexed")

        decoded_input_log_parameter = cls(
            name=name,
            type_=type_,
            value=value,
            indexed=indexed,
        )

        decoded_input_log_parameter.additional_properties = d
        return decoded_input_log_parameter

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
