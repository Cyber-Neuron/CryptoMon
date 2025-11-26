from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RawTraceSelfDestructAction")


@_attrs_define
class RawTraceSelfDestructAction:
    """
    Attributes:
        address (str):  Example: 0xf57b55b01b831e602e09674a4e5d69cbcf343f98.
        balance (str):  Example: 0x25D3FC.
        refund_address (str):  Example: 0x162e898bd0aacb578c8d5f8d6ca588c13d2a383f.
    """

    address: str
    balance: str
    refund_address: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        address = self.address

        balance = self.balance

        refund_address = self.refund_address

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "address": address,
                "balance": balance,
                "refundAddress": refund_address,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        address = d.pop("address")

        balance = d.pop("balance")

        refund_address = d.pop("refundAddress")

        raw_trace_self_destruct_action = cls(
            address=address,
            balance=balance,
            refund_address=refund_address,
        )

        raw_trace_self_destruct_action.additional_properties = d
        return raw_trace_self_destruct_action

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
