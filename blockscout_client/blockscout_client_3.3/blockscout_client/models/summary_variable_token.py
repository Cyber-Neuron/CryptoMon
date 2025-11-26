from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.token_info_detailed import TokenInfoDetailed


T = TypeVar("T", bound="SummaryVariableToken")


@_attrs_define
class SummaryVariableToken:
    """
    Attributes:
        type_ (str): Type Example: token.
        value (TokenInfoDetailed):
    """

    type_: str
    value: "TokenInfoDetailed"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        value = self.value.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.token_info_detailed import TokenInfoDetailed

        d = dict(src_dict)
        type_ = d.pop("type")

        value = TokenInfoDetailed.from_dict(d.pop("value"))

        summary_variable_token = cls(
            type_=type_,
            value=value,
        )

        summary_variable_token.additional_properties = d
        return summary_variable_token

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
