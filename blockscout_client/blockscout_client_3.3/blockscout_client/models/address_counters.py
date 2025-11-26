from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AddressCounters")


@_attrs_define
class AddressCounters:
    """
    Attributes:
        transactions_count (str):  Example: 0.
        token_transfers_count (str):  Example: 0.
        gas_usage_count (str):  Example: 0.
        validations_count (str):  Example: 0.
    """

    transactions_count: str
    token_transfers_count: str
    gas_usage_count: str
    validations_count: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        transactions_count = self.transactions_count

        token_transfers_count = self.token_transfers_count

        gas_usage_count = self.gas_usage_count

        validations_count = self.validations_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "transactions_count": transactions_count,
                "token_transfers_count": token_transfers_count,
                "gas_usage_count": gas_usage_count,
                "validations_count": validations_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        transactions_count = d.pop("transactions_count")

        token_transfers_count = d.pop("token_transfers_count")

        gas_usage_count = d.pop("gas_usage_count")

        validations_count = d.pop("validations_count")

        address_counters = cls(
            transactions_count=transactions_count,
            token_transfers_count=token_transfers_count,
            gas_usage_count=gas_usage_count,
            validations_count=validations_count,
        )

        address_counters.additional_properties = d
        return address_counters

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
