from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ContractSource")


@_attrs_define
class ContractSource:
    r"""
    Attributes:
        file_path (Union[Unset, str]):  Example: contracts/erc-20.sol.
        source_code (Union[Unset, str]):  Example: pragma solidity ^0.8.0; \n contract A {}.
    """

    file_path: Union[Unset, str] = UNSET
    source_code: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        file_path = self.file_path

        source_code = self.source_code

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if file_path is not UNSET:
            field_dict["file_path"] = file_path
        if source_code is not UNSET:
            field_dict["source_code"] = source_code

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        file_path = d.pop("file_path", UNSET)

        source_code = d.pop("source_code", UNSET)

        contract_source = cls(
            file_path=file_path,
            source_code=source_code,
        )

        contract_source.additional_properties = d
        return contract_source

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
