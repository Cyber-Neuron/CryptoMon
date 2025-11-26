from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.address_param import AddressParam
    from ..models.transaction_reward_types import TransactionRewardTypes


T = TypeVar("T", bound="TransactionReward")


@_attrs_define
class TransactionReward:
    """
    Attributes:
        types (TransactionRewardTypes):  Example: ['reward'].
        emission_reward (str):  Example: 500000000000000000.
        block_hash (str):  Example: 0x3169a7e9c513462403abb40eaa4fa51c5fbe1b908606e6eeef16232e308cb464.
        from_ (AddressParam):
        to (AddressParam):
    """

    types: "TransactionRewardTypes"
    emission_reward: str
    block_hash: str
    from_: "AddressParam"
    to: "AddressParam"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        types = self.types.to_dict()

        emission_reward = self.emission_reward

        block_hash = self.block_hash

        from_ = self.from_.to_dict()

        to = self.to.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "types": types,
                "emission_reward": emission_reward,
                "block_hash": block_hash,
                "from": from_,
                "to": to,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.address_param import AddressParam
        from ..models.transaction_reward_types import TransactionRewardTypes

        d = dict(src_dict)
        types = TransactionRewardTypes.from_dict(d.pop("types"))

        emission_reward = d.pop("emission_reward")

        block_hash = d.pop("block_hash")

        from_ = AddressParam.from_dict(d.pop("from"))

        to = AddressParam.from_dict(d.pop("to"))

        transaction_reward = cls(
            types=types,
            emission_reward=emission_reward,
            block_hash=block_hash,
            from_=from_,
            to=to,
        )

        transaction_reward.additional_properties = d
        return transaction_reward

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
