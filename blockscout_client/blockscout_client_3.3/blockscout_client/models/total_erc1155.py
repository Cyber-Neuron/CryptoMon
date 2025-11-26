from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.nft_instance import NFTInstance


T = TypeVar("T", bound="TotalERC1155")


@_attrs_define
class TotalERC1155:
    """
    Attributes:
        token_id (str):  Example: 1.
        decimals (str):
        value (str):  Example: 1000.
        token_instance (Union[Unset, NFTInstance]):
    """

    token_id: str
    decimals: str
    value: str
    token_instance: Union[Unset, "NFTInstance"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        token_id = self.token_id

        decimals = self.decimals

        value = self.value

        token_instance: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.token_instance, Unset):
            token_instance = self.token_instance.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "token_id": token_id,
                "decimals": decimals,
                "value": value,
            }
        )
        if token_instance is not UNSET:
            field_dict["token_instance"] = token_instance

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.nft_instance import NFTInstance

        d = dict(src_dict)
        token_id = d.pop("token_id")

        decimals = d.pop("decimals")

        value = d.pop("value")

        _token_instance = d.pop("token_instance", UNSET)
        token_instance: Union[Unset, NFTInstance]
        if isinstance(_token_instance, Unset):
            token_instance = UNSET
        else:
            token_instance = NFTInstance.from_dict(_token_instance)

        total_erc1155 = cls(
            token_id=token_id,
            decimals=decimals,
            value=value,
            token_instance=token_instance,
        )

        total_erc1155.additional_properties = d
        return total_erc1155

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
