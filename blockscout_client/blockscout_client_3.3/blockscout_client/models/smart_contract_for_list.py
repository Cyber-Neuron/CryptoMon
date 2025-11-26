from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.address_param import AddressParam


T = TypeVar("T", bound="SmartContractForList")


@_attrs_define
class SmartContractForList:
    """
    Attributes:
        address (AddressParam):
        coin_balance (str):  Example: 10000.
        compiler_version (str):  Example: v0.5.10+commit.5a6ea5b1.
        language (str):  Example: vyper | yul | solidity.
        has_constructor_args (bool):
        optimization_enabled (bool):
        transaction_count (int):
        verified_at (str):  Example: 2022-03-05T11:40:29.087000Z.
        market_cap (Union[Unset, float]):  Example: 1000000000.0001.
    """

    address: "AddressParam"
    coin_balance: str
    compiler_version: str
    language: str
    has_constructor_args: bool
    optimization_enabled: bool
    transaction_count: int
    verified_at: str
    market_cap: Union[Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        address = self.address.to_dict()

        coin_balance = self.coin_balance

        compiler_version = self.compiler_version

        language = self.language

        has_constructor_args = self.has_constructor_args

        optimization_enabled = self.optimization_enabled

        transaction_count = self.transaction_count

        verified_at = self.verified_at

        market_cap = self.market_cap

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "address": address,
                "coin_balance": coin_balance,
                "compiler_version": compiler_version,
                "language": language,
                "has_constructor_args": has_constructor_args,
                "optimization_enabled": optimization_enabled,
                "transaction_count": transaction_count,
                "verified_at": verified_at,
            }
        )
        if market_cap is not UNSET:
            field_dict["market_cap"] = market_cap

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.address_param import AddressParam

        d = dict(src_dict)
        address = AddressParam.from_dict(d.pop("address"))

        coin_balance = d.pop("coin_balance")

        compiler_version = d.pop("compiler_version")

        language = d.pop("language")

        has_constructor_args = d.pop("has_constructor_args")

        optimization_enabled = d.pop("optimization_enabled")

        transaction_count = d.pop("transaction_count")

        verified_at = d.pop("verified_at")

        market_cap = d.pop("market_cap", UNSET)

        smart_contract_for_list = cls(
            address=address,
            coin_balance=coin_balance,
            compiler_version=compiler_version,
            language=language,
            has_constructor_args=has_constructor_args,
            optimization_enabled=optimization_enabled,
            transaction_count=transaction_count,
            verified_at=verified_at,
            market_cap=market_cap,
        )

        smart_contract_for_list.additional_properties = d
        return smart_contract_for_list

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
