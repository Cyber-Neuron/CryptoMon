from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SearchResultRedirect")


@_attrs_define
class SearchResultRedirect:
    """
    Attributes:
        parameter (str):  Example: 0xEb533ee5687044E622C69c58B1B12329F56eD9ad.
        redirect (bool):
        type_ (str):  Example: address | block | transaction.
    """

    parameter: str
    redirect: bool
    type_: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        parameter = self.parameter

        redirect = self.redirect

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "parameter": parameter,
                "redirect": redirect,
                "type": type_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        parameter = d.pop("parameter")

        redirect = d.pop("redirect")

        type_ = d.pop("type")

        search_result_redirect = cls(
            parameter=parameter,
            redirect=redirect,
            type_=type_,
        )

        search_result_redirect.additional_properties = d
        return search_result_redirect

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
