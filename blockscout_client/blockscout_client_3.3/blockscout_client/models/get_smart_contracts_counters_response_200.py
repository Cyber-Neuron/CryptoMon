from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GetSmartContractsCountersResponse200")


@_attrs_define
class GetSmartContractsCountersResponse200:
    """
    Attributes:
        new_smart_contracts_24h (str):  Example: 12.
        new_verified_smart_contracts_24h (str):  Example: 11.
        smart_contracts (str):  Example: 20.
        verified_smart_contracts (str):  Example: 15.
    """

    new_smart_contracts_24h: str
    new_verified_smart_contracts_24h: str
    smart_contracts: str
    verified_smart_contracts: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        new_smart_contracts_24h = self.new_smart_contracts_24h

        new_verified_smart_contracts_24h = self.new_verified_smart_contracts_24h

        smart_contracts = self.smart_contracts

        verified_smart_contracts = self.verified_smart_contracts

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "new_smart_contracts_24h": new_smart_contracts_24h,
                "new_verified_smart_contracts_24h": new_verified_smart_contracts_24h,
                "smart_contracts": smart_contracts,
                "verified_smart_contracts": verified_smart_contracts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        new_smart_contracts_24h = d.pop("new_smart_contracts_24h")

        new_verified_smart_contracts_24h = d.pop("new_verified_smart_contracts_24h")

        smart_contracts = d.pop("smart_contracts")

        verified_smart_contracts = d.pop("verified_smart_contracts")

        get_smart_contracts_counters_response_200 = cls(
            new_smart_contracts_24h=new_smart_contracts_24h,
            new_verified_smart_contracts_24h=new_verified_smart_contracts_24h,
            smart_contracts=smart_contracts,
            verified_smart_contracts=verified_smart_contracts,
        )

        get_smart_contracts_counters_response_200.additional_properties = d
        return get_smart_contracts_counters_response_200

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
