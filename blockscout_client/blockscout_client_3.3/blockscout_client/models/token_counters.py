from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="TokenCounters")


@_attrs_define
class TokenCounters:
    """
    Attributes:
        token_holders_count (str):  Example: 100.
        transfers_count (str):  Example: 1000.
    """

    token_holders_count: str
    transfers_count: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        token_holders_count = self.token_holders_count

        transfers_count = self.transfers_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "token_holders_count": token_holders_count,
                "transfers_count": transfers_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        token_holders_count = d.pop("token_holders_count")

        transfers_count = d.pop("transfers_count")

        token_counters = cls(
            token_holders_count=token_holders_count,
            transfers_count=transfers_count,
        )

        token_counters.additional_properties = d
        return token_counters

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
