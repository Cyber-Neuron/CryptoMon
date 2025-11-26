from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AddressTag")


@_attrs_define
class AddressTag:
    """
    Attributes:
        address_hash (str):  Example: 0xEb533ee5687044E622C69c58B1B12329F56eD9ad.
        display_name (str):  Example: name to show.
        label (str):  Example: label.
    """

    address_hash: str
    display_name: str
    label: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        address_hash = self.address_hash

        display_name = self.display_name

        label = self.label

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "address_hash": address_hash,
                "display_name": display_name,
                "label": label,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        address_hash = d.pop("address_hash")

        display_name = d.pop("display_name")

        label = d.pop("label")

        address_tag = cls(
            address_hash=address_hash,
            display_name=display_name,
            label=label,
        )

        address_tag.additional_properties = d
        return address_tag

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
