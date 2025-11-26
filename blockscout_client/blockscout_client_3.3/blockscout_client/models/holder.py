from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.address_param import AddressParam
    from ..models.token_info import TokenInfo


T = TypeVar("T", bound="Holder")


@_attrs_define
class Holder:
    """
    Attributes:
        address (AddressParam):
        value (str):  Example: 10000.
        token (TokenInfo):
        token_id (Union[Unset, str]):  Example: 10000.
    """

    address: "AddressParam"
    value: str
    token: "TokenInfo"
    token_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        address = self.address.to_dict()

        value = self.value

        token = self.token.to_dict()

        token_id = self.token_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "address": address,
                "value": value,
                "token": token,
            }
        )
        if token_id is not UNSET:
            field_dict["token_id"] = token_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.address_param import AddressParam
        from ..models.token_info import TokenInfo

        d = dict(src_dict)
        address = AddressParam.from_dict(d.pop("address"))

        value = d.pop("value")

        token = TokenInfo.from_dict(d.pop("token"))

        token_id = d.pop("token_id", UNSET)

        holder = cls(
            address=address,
            value=value,
            token=token,
            token_id=token_id,
        )

        holder.additional_properties = d
        return holder

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
