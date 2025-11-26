from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SearchResultAddressOrContract")


@_attrs_define
class SearchResultAddressOrContract:
    """
    Attributes:
        address (str):  Example: 0xe2FBdeADC82c71C1b8bFf9CA4f9E7666224A362c.
        is_smart_contract_verified (bool):  Example: True.
        name (str):  Example: Name.
        type_ (str):  Example: address|contract.
        url (str):  Example: /xdai/mainnet/address/0xc1c1031e4A44B98707203480029e6576CB3267e3.
    """

    address: str
    is_smart_contract_verified: bool
    name: str
    type_: str
    url: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        address = self.address

        is_smart_contract_verified = self.is_smart_contract_verified

        name = self.name

        type_ = self.type_

        url = self.url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "address": address,
                "is_smart_contract_verified": is_smart_contract_verified,
                "name": name,
                "type": type_,
                "url": url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        address = d.pop("address")

        is_smart_contract_verified = d.pop("is_smart_contract_verified")

        name = d.pop("name")

        type_ = d.pop("type")

        url = d.pop("url")

        search_result_address_or_contract = cls(
            address=address,
            is_smart_contract_verified=is_smart_contract_verified,
            name=name,
            type_=type_,
            url=url,
        )

        search_result_address_or_contract.additional_properties = d
        return search_result_address_or_contract

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
