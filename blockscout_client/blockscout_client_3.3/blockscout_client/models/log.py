from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.address_param import AddressParam
    from ..models.decoded_input_log import DecodedInputLog


T = TypeVar("T", bound="Log")


@_attrs_define
class Log:
    """
    Attributes:
        address (AddressParam):
        data (str):  Example: 0x000000000000000000000000000000000000000000000000006a94d74f430000.
        decoded (DecodedInputLog):
        index (int):  Example: 35.
        smart_contract (AddressParam):
        topics (list[str]):
        transaction_hash (str):  Example: 0x08ea4d75ad0abe327a7fd368733eaeac43077989e635d800530d7906ebf3bd54.
        block_hash (Union[Unset, str]):  Example: 0xf90fdff5f174f7f29ebdf203d32cad2fe95376e41880bb9e731ca5eb0eef7941.
        block_number (Union[Unset, int]):  Example: 8844586.
    """

    address: "AddressParam"
    data: str
    decoded: "DecodedInputLog"
    index: int
    smart_contract: "AddressParam"
    topics: list[str]
    transaction_hash: str
    block_hash: Union[Unset, str] = UNSET
    block_number: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        address = self.address.to_dict()

        data = self.data

        decoded = self.decoded.to_dict()

        index = self.index

        smart_contract = self.smart_contract.to_dict()

        topics = self.topics

        transaction_hash = self.transaction_hash

        block_hash = self.block_hash

        block_number = self.block_number

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "address": address,
                "data": data,
                "decoded": decoded,
                "index": index,
                "smart_contract": smart_contract,
                "topics": topics,
                "transaction_hash": transaction_hash,
            }
        )
        if block_hash is not UNSET:
            field_dict["block_hash"] = block_hash
        if block_number is not UNSET:
            field_dict["block_number"] = block_number

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.address_param import AddressParam
        from ..models.decoded_input_log import DecodedInputLog

        d = dict(src_dict)
        address = AddressParam.from_dict(d.pop("address"))

        data = d.pop("data")

        decoded = DecodedInputLog.from_dict(d.pop("decoded"))

        index = d.pop("index")

        smart_contract = AddressParam.from_dict(d.pop("smart_contract"))

        topics = cast(list[str], d.pop("topics"))

        transaction_hash = d.pop("transaction_hash")

        block_hash = d.pop("block_hash", UNSET)

        block_number = d.pop("block_number", UNSET)

        log = cls(
            address=address,
            data=data,
            decoded=decoded,
            index=index,
            smart_contract=smart_contract,
            topics=topics,
            transaction_hash=transaction_hash,
            block_hash=block_hash,
            block_number=block_number,
        )

        log.additional_properties = d
        return log

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
