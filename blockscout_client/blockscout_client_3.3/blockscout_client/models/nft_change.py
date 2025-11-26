from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.total_erc721 import TotalERC721


T = TypeVar("T", bound="NFTChange")


@_attrs_define
class NFTChange:
    """
    Attributes:
        direction (str):  Example: from | to.
        total (TotalERC721):
    """

    direction: str
    total: "TotalERC721"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        direction = self.direction

        total = self.total.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "direction": direction,
                "total": total,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.total_erc721 import TotalERC721

        d = dict(src_dict)
        direction = d.pop("direction")

        total = TotalERC721.from_dict(d.pop("total"))

        nft_change = cls(
            direction=direction,
            total=total,
        )

        nft_change.additional_properties = d
        return nft_change

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
