from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SmartContractCompilerSettings")


@_attrs_define
class SmartContractCompilerSettings:
    """
    Example:
        {'compilationTarget': {'@openzeppelin/contracts/proxy/ERC1967/ERC1967Proxy.sol': 'ERC1967Proxy'}, 'evmVersion':
            'london', 'libraries': {}, 'metadata': {'bytecodeHash': 'ipfs'}, 'optimizer': {'enabled': True, 'runs': 200},
            'remappings': []}

    """

    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        smart_contract_compiler_settings = cls()

        smart_contract_compiler_settings.additional_properties = d
        return smart_contract_compiler_settings

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
