from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.code_and_message import CodeAndMessage
    from ..models.decoded_input import DecodedInput
    from ..models.error import Error
    from ..models.extended_revert_reason_as_map import ExtendedRevertReasonAsMap
    from ..models.output_and_names import OutputAndNames


T = TypeVar("T", bound="ReadMethodResponse")


@_attrs_define
class ReadMethodResponse:
    """
    Attributes:
        is_error (bool):
        result (Union['CodeAndMessage', 'DecodedInput', 'Error', 'ExtendedRevertReasonAsMap', 'OutputAndNames']):
    """

    is_error: bool
    result: Union["CodeAndMessage", "DecodedInput", "Error", "ExtendedRevertReasonAsMap", "OutputAndNames"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.code_and_message import CodeAndMessage
        from ..models.decoded_input import DecodedInput
        from ..models.error import Error
        from ..models.extended_revert_reason_as_map import ExtendedRevertReasonAsMap

        is_error = self.is_error

        result: dict[str, Any]
        if isinstance(self.result, ExtendedRevertReasonAsMap):
            result = self.result.to_dict()
        elif isinstance(self.result, Error):
            result = self.result.to_dict()
        elif isinstance(self.result, DecodedInput):
            result = self.result.to_dict()
        elif isinstance(self.result, CodeAndMessage):
            result = self.result.to_dict()
        else:
            result = self.result.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "is_error": is_error,
                "result": result,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.code_and_message import CodeAndMessage
        from ..models.decoded_input import DecodedInput
        from ..models.error import Error
        from ..models.extended_revert_reason_as_map import ExtendedRevertReasonAsMap
        from ..models.output_and_names import OutputAndNames

        d = dict(src_dict)
        is_error = d.pop("is_error")

        def _parse_result(
            data: object,
        ) -> Union["CodeAndMessage", "DecodedInput", "Error", "ExtendedRevertReasonAsMap", "OutputAndNames"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                result_type_0 = ExtendedRevertReasonAsMap.from_dict(data)

                return result_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                result_type_1 = Error.from_dict(data)

                return result_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                result_type_2 = DecodedInput.from_dict(data)

                return result_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                result_type_3 = CodeAndMessage.from_dict(data)

                return result_type_3
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            result_type_4 = OutputAndNames.from_dict(data)

            return result_type_4

        result = _parse_result(d.pop("result"))

        read_method_response = cls(
            is_error=is_error,
            result=result,
        )

        read_method_response.additional_properties = d
        return read_method_response

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
