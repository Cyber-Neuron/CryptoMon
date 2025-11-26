from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.address_param import AddressParam
    from ..models.reward import Reward


T = TypeVar("T", bound="Block")


@_attrs_define
class Block:
    """
    Attributes:
        base_fee_per_gas (str):  Example: 26618801760.
        burnt_fees (str):  Example: 261263193229977120.
        burnt_fees_percentage (float):  Example: 85.19028810863084.
        difficulty (str):  Example: 0.
        extra_data (str):  Example: TODO.
        gas_limit (str):  Example: 30000000.
        gas_target_percentage (float):  Example: -34.56675333333333.
        gas_used (str):  Example: 9814987.
        gas_used_percentage (float):  Example: 32.71662333333333.
        hash_ (str):  Example: 0xf569ec751152b2f814001fc730f7797aa155e4bc3ba9cb6ba24bc2c8c9468c1a.
        height (int):  Example: 17615720.
        miner (AddressParam):
        nonce (str):  Example: 0x0000000000000000.
        parent_hash (str):  Example: 0xd464e02d81e2bdf6bc5fa9b8e33f0b564c464a82d821a3e56531f8636dc00dfa.
        priority_fee (str):  Example: 45418705646601378.
        rewards (list['Reward']):
        size (int):  Example: 49997.
        state_root (str):  Example: TODO.
        timestamp (str):  Example: 2023-07-03T20:09:59.000000Z.
        total_difficulty (str):  Example: 58750003716598352816469.
        transaction_count (int):  Example: 120.
        transaction_fees (str):  Example: 306681898876578498.
        type_ (str):  Example: block.
        uncles_hashes (list[str]):
        withdrawals_count (int):  Example: 16.
    """

    base_fee_per_gas: str
    burnt_fees: str
    burnt_fees_percentage: float
    difficulty: str
    extra_data: str
    gas_limit: str
    gas_target_percentage: float
    gas_used: str
    gas_used_percentage: float
    hash_: str
    height: int
    miner: "AddressParam"
    nonce: str
    parent_hash: str
    priority_fee: str
    rewards: list["Reward"]
    size: int
    state_root: str
    timestamp: str
    total_difficulty: str
    transaction_count: int
    transaction_fees: str
    type_: str
    uncles_hashes: list[str]
    withdrawals_count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        base_fee_per_gas = self.base_fee_per_gas

        burnt_fees = self.burnt_fees

        burnt_fees_percentage = self.burnt_fees_percentage

        difficulty = self.difficulty

        extra_data = self.extra_data

        gas_limit = self.gas_limit

        gas_target_percentage = self.gas_target_percentage

        gas_used = self.gas_used

        gas_used_percentage = self.gas_used_percentage

        hash_ = self.hash_

        height = self.height

        miner = self.miner.to_dict()

        nonce = self.nonce

        parent_hash = self.parent_hash

        priority_fee = self.priority_fee

        rewards = []
        for rewards_item_data in self.rewards:
            rewards_item = rewards_item_data.to_dict()
            rewards.append(rewards_item)

        size = self.size

        state_root = self.state_root

        timestamp = self.timestamp

        total_difficulty = self.total_difficulty

        transaction_count = self.transaction_count

        transaction_fees = self.transaction_fees

        type_ = self.type_

        uncles_hashes = self.uncles_hashes

        withdrawals_count = self.withdrawals_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "base_fee_per_gas": base_fee_per_gas,
                "burnt_fees": burnt_fees,
                "burnt_fees_percentage": burnt_fees_percentage,
                "difficulty": difficulty,
                "extra_data": extra_data,
                "gas_limit": gas_limit,
                "gas_target_percentage": gas_target_percentage,
                "gas_used": gas_used,
                "gas_used_percentage": gas_used_percentage,
                "hash": hash_,
                "height": height,
                "miner": miner,
                "nonce": nonce,
                "parent_hash": parent_hash,
                "priority_fee": priority_fee,
                "rewards": rewards,
                "size": size,
                "state_root": state_root,
                "timestamp": timestamp,
                "total_difficulty": total_difficulty,
                "transaction_count": transaction_count,
                "transaction_fees": transaction_fees,
                "type": type_,
                "uncles_hashes": uncles_hashes,
                "withdrawals_count": withdrawals_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.address_param import AddressParam
        from ..models.reward import Reward

        d = dict(src_dict)
        base_fee_per_gas = d.pop("base_fee_per_gas")

        burnt_fees = d.pop("burnt_fees")

        burnt_fees_percentage = d.pop("burnt_fees_percentage")

        difficulty = d.pop("difficulty")

        extra_data = d.pop("extra_data")

        gas_limit = d.pop("gas_limit")

        gas_target_percentage = d.pop("gas_target_percentage")

        gas_used = d.pop("gas_used")

        gas_used_percentage = d.pop("gas_used_percentage")

        hash_ = d.pop("hash")

        height = d.pop("height")

        miner = AddressParam.from_dict(d.pop("miner"))

        nonce = d.pop("nonce")

        parent_hash = d.pop("parent_hash")

        priority_fee = d.pop("priority_fee")

        rewards = []
        _rewards = d.pop("rewards")
        for rewards_item_data in _rewards:
            rewards_item = Reward.from_dict(rewards_item_data)

            rewards.append(rewards_item)

        size = d.pop("size")

        state_root = d.pop("state_root")

        timestamp = d.pop("timestamp")

        total_difficulty = d.pop("total_difficulty")

        transaction_count = d.pop("transaction_count")

        transaction_fees = d.pop("transaction_fees")

        type_ = d.pop("type")

        uncles_hashes = cast(list[str], d.pop("uncles_hashes"))

        withdrawals_count = d.pop("withdrawals_count")

        block = cls(
            base_fee_per_gas=base_fee_per_gas,
            burnt_fees=burnt_fees,
            burnt_fees_percentage=burnt_fees_percentage,
            difficulty=difficulty,
            extra_data=extra_data,
            gas_limit=gas_limit,
            gas_target_percentage=gas_target_percentage,
            gas_used=gas_used,
            gas_used_percentage=gas_used_percentage,
            hash_=hash_,
            height=height,
            miner=miner,
            nonce=nonce,
            parent_hash=parent_hash,
            priority_fee=priority_fee,
            rewards=rewards,
            size=size,
            state_root=state_root,
            timestamp=timestamp,
            total_difficulty=total_difficulty,
            transaction_count=transaction_count,
            transaction_fees=transaction_fees,
            type_=type_,
            uncles_hashes=uncles_hashes,
            withdrawals_count=withdrawals_count,
        )

        block.additional_properties = d
        return block

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
