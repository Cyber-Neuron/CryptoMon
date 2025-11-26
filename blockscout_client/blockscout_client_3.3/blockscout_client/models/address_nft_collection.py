from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.address_nft_instance_collection import AddressNFTInstanceCollection
    from ..models.token_info import TokenInfo


T = TypeVar("T", bound="AddressNFTCollection")


@_attrs_define
class AddressNFTCollection:
    """
    Attributes:
        token (TokenInfo):
        token_instances (list['AddressNFTInstanceCollection']):
        amount (Union[Unset, str]):  Example: 1.
    """

    token: "TokenInfo"
    token_instances: list["AddressNFTInstanceCollection"]
    amount: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        token = self.token.to_dict()

        token_instances = []
        for token_instances_item_data in self.token_instances:
            token_instances_item = token_instances_item_data.to_dict()
            token_instances.append(token_instances_item)

        amount = self.amount

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "token": token,
                "token_instances": token_instances,
            }
        )
        if amount is not UNSET:
            field_dict["amount"] = amount

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.address_nft_instance_collection import AddressNFTInstanceCollection
        from ..models.token_info import TokenInfo

        d = dict(src_dict)
        token = TokenInfo.from_dict(d.pop("token"))

        token_instances = []
        _token_instances = d.pop("token_instances")
        for token_instances_item_data in _token_instances:
            token_instances_item = AddressNFTInstanceCollection.from_dict(token_instances_item_data)

            token_instances.append(token_instances_item)

        amount = d.pop("amount", UNSET)

        address_nft_collection = cls(
            token=token,
            token_instances=token_instances,
            amount=amount,
        )

        address_nft_collection.additional_properties = d
        return address_nft_collection

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
