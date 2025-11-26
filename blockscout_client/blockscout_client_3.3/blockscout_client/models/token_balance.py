from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.nft_instance import NFTInstance
    from ..models.token import Token


T = TypeVar("T", bound="TokenBalance")


@_attrs_define
class TokenBalance:
    """
    Attributes:
        value (str):  Example: 10000.
        token_id (str):  Example: 123.
        token (Token):
        token_instance (Union[Unset, NFTInstance]):
    """

    value: str
    token_id: str
    token: "Token"
    token_instance: Union[Unset, "NFTInstance"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        value = self.value

        token_id = self.token_id

        token = self.token.to_dict()

        token_instance: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.token_instance, Unset):
            token_instance = self.token_instance.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "value": value,
                "token_id": token_id,
                "token": token,
            }
        )
        if token_instance is not UNSET:
            field_dict["token_instance"] = token_instance

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.nft_instance import NFTInstance
        from ..models.token import Token

        d = dict(src_dict)
        value = d.pop("value")

        token_id = d.pop("token_id")

        token = Token.from_dict(d.pop("token"))

        _token_instance = d.pop("token_instance", UNSET)
        token_instance: Union[Unset, NFTInstance]
        if isinstance(_token_instance, Unset):
            token_instance = UNSET
        else:
            token_instance = NFTInstance.from_dict(_token_instance)

        token_balance = cls(
            value=value,
            token_id=token_id,
            token=token,
            token_instance=token_instance,
        )

        token_balance.additional_properties = d
        return token_balance

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
