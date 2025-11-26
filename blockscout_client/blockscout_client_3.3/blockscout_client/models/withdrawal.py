from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.address_param import AddressParam


T = TypeVar("T", bound="Withdrawal")


@_attrs_define
class Withdrawal:
    """
    Attributes:
        index (int):  Example: 1.
        amount (str):  Example: 1000000000000000000.
        validator_index (int):  Example: 1.
        receiver (Union[Unset, AddressParam]):
        block_number (Union[Unset, int]):  Example: 1.
        timestamp (Union[Unset, str]):  Example: 2023-06-20T07:55:00.000000Z.
    """

    index: int
    amount: str
    validator_index: int
    receiver: Union[Unset, "AddressParam"] = UNSET
    block_number: Union[Unset, int] = UNSET
    timestamp: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        index = self.index

        amount = self.amount

        validator_index = self.validator_index

        receiver: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.receiver, Unset):
            receiver = self.receiver.to_dict()

        block_number = self.block_number

        timestamp = self.timestamp

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "index": index,
                "amount": amount,
                "validator_index": validator_index,
            }
        )
        if receiver is not UNSET:
            field_dict["receiver"] = receiver
        if block_number is not UNSET:
            field_dict["block_number"] = block_number
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.address_param import AddressParam

        d = dict(src_dict)
        index = d.pop("index")

        amount = d.pop("amount")

        validator_index = d.pop("validator_index")

        _receiver = d.pop("receiver", UNSET)
        receiver: Union[Unset, AddressParam]
        if isinstance(_receiver, Unset):
            receiver = UNSET
        else:
            receiver = AddressParam.from_dict(_receiver)

        block_number = d.pop("block_number", UNSET)

        timestamp = d.pop("timestamp", UNSET)

        withdrawal = cls(
            index=index,
            amount=amount,
            validator_index=validator_index,
            receiver=receiver,
            block_number=block_number,
            timestamp=timestamp,
        )

        withdrawal.additional_properties = d
        return withdrawal

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
