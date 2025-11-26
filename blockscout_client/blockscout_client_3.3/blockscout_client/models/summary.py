from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.summary_template_variables import SummaryTemplateVariables


T = TypeVar("T", bound="Summary")


@_attrs_define
class Summary:
    """
    Attributes:
        summary_template (str): Summary template Example: {action_type} of {amount} {token}.
        summary_template_variables (SummaryTemplateVariables):
    """

    summary_template: str
    summary_template_variables: "SummaryTemplateVariables"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        summary_template = self.summary_template

        summary_template_variables = self.summary_template_variables.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "summary_template": summary_template,
                "summary_template_variables": summary_template_variables,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.summary_template_variables import SummaryTemplateVariables

        d = dict(src_dict)
        summary_template = d.pop("summary_template")

        summary_template_variables = SummaryTemplateVariables.from_dict(d.pop("summary_template_variables"))

        summary = cls(
            summary_template=summary_template,
            summary_template_variables=summary_template_variables,
        )

        summary.additional_properties = d
        return summary

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
