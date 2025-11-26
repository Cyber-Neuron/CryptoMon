from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.summary_variable import SummaryVariable
    from ..models.summary_variable_currency import SummaryVariableCurrency
    from ..models.summary_variable_token import SummaryVariableToken


T = TypeVar("T", bound="SummaryTemplateVariables")


@_attrs_define
class SummaryTemplateVariables:
    """
    Attributes:
        action_type (SummaryVariable):
        amount (SummaryVariableCurrency):
        token (SummaryVariableToken):
    """

    action_type: "SummaryVariable"
    amount: "SummaryVariableCurrency"
    token: "SummaryVariableToken"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        action_type = self.action_type.to_dict()

        amount = self.amount.to_dict()

        token = self.token.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "action_type": action_type,
                "amount": amount,
                "token": token,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.summary_variable import SummaryVariable
        from ..models.summary_variable_currency import SummaryVariableCurrency
        from ..models.summary_variable_token import SummaryVariableToken

        d = dict(src_dict)
        action_type = SummaryVariable.from_dict(d.pop("action_type"))

        amount = SummaryVariableCurrency.from_dict(d.pop("amount"))

        token = SummaryVariableToken.from_dict(d.pop("token"))

        summary_template_variables = cls(
            action_type=action_type,
            amount=amount,
            token=token,
        )

        summary_template_variables.additional_properties = d
        return summary_template_variables

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
