from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.address_param import AddressParam


T = TypeVar("T", bound="InternalTransaction")


@_attrs_define
class InternalTransaction:
    """
    Attributes:
        block_number (int):  Example: 8844586.
        created_contract (AddressParam):
        error (str):  Example: reverted.
        from_ (AddressParam):
        gas_limit (str):  Example: 351759.
        index (int):  Example: 1.
        success (bool):  Example: True.
        timestamp (str):  Example: 2023-04-17T10:37:12.000000Z.
        to (AddressParam):
        transaction_hash (str):  Example: 0x08ea4d75ad0abe327a7fd368733eaeac43077989e635d800530d7906ebf3bd54.
        type_ (str):  Example: call.
        value (str):  Example: 30000000000000000.
    """

    block_number: int
    created_contract: "AddressParam"
    error: str
    from_: "AddressParam"
    gas_limit: str
    index: int
    success: bool
    timestamp: str
    to: "AddressParam"
    transaction_hash: str
    type_: str
    value: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        block_number = self.block_number

        created_contract = self.created_contract.to_dict()

        error = self.error

        from_ = self.from_.to_dict()

        gas_limit = self.gas_limit

        index = self.index

        success = self.success

        timestamp = self.timestamp

        to = self.to.to_dict()

        transaction_hash = self.transaction_hash

        type_ = self.type_

        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "block_number": block_number,
                "created_contract": created_contract,
                "error": error,
                "from": from_,
                "gas_limit": gas_limit,
                "index": index,
                "success": success,
                "timestamp": timestamp,
                "to": to,
                "transaction_hash": transaction_hash,
                "type": type_,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.address_param import AddressParam

        d = dict(src_dict)
        block_number = d.pop("block_number")

        created_contract = AddressParam.from_dict(d.pop("created_contract"))

        error = d.pop("error")

        from_ = AddressParam.from_dict(d.pop("from"))

        gas_limit = d.pop("gas_limit")

        index = d.pop("index")

        success = d.pop("success")

        timestamp = d.pop("timestamp")

        to = AddressParam.from_dict(d.pop("to"))

        transaction_hash = d.pop("transaction_hash")

        type_ = d.pop("type")

        value = d.pop("value")

        internal_transaction = cls(
            block_number=block_number,
            created_contract=created_contract,
            error=error,
            from_=from_,
            gas_limit=gas_limit,
            index=index,
            success=success,
            timestamp=timestamp,
            to=to,
            transaction_hash=transaction_hash,
            type_=type_,
            value=value,
        )

        internal_transaction.additional_properties = d
        return internal_transaction

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
