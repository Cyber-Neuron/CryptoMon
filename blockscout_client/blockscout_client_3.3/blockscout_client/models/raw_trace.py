from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.raw_trace_call_action import RawTraceCallAction
    from ..models.raw_trace_call_result import RawTraceCallResult
    from ..models.raw_trace_create_action import RawTraceCreateAction
    from ..models.raw_trace_create_result import RawTraceCreateResult
    from ..models.raw_trace_self_destruct_action import RawTraceSelfDestructAction


T = TypeVar("T", bound="RawTrace")


@_attrs_define
class RawTrace:
    """
    Attributes:
        action (Union['RawTraceCallAction', 'RawTraceCreateAction', 'RawTraceSelfDestructAction']):
        subtraces (int):
        trace_address (list[int]):  Example: [0, 0].
        type_ (str):  Example: call.
        error (Union[Unset, str]):  Example: Reverted.
        result (Union['RawTraceCallResult', 'RawTraceCreateResult', Unset]):
    """

    action: Union["RawTraceCallAction", "RawTraceCreateAction", "RawTraceSelfDestructAction"]
    subtraces: int
    trace_address: list[int]
    type_: str
    error: Union[Unset, str] = UNSET
    result: Union["RawTraceCallResult", "RawTraceCreateResult", Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.raw_trace_call_action import RawTraceCallAction
        from ..models.raw_trace_call_result import RawTraceCallResult
        from ..models.raw_trace_create_action import RawTraceCreateAction

        action: dict[str, Any]
        if isinstance(self.action, RawTraceCallAction):
            action = self.action.to_dict()
        elif isinstance(self.action, RawTraceCreateAction):
            action = self.action.to_dict()
        else:
            action = self.action.to_dict()

        subtraces = self.subtraces

        trace_address = self.trace_address

        type_ = self.type_

        error = self.error

        result: Union[Unset, dict[str, Any]]
        if isinstance(self.result, Unset):
            result = UNSET
        elif isinstance(self.result, RawTraceCallResult):
            result = self.result.to_dict()
        else:
            result = self.result.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "action": action,
                "subtraces": subtraces,
                "traceAddress": trace_address,
                "type": type_,
            }
        )
        if error is not UNSET:
            field_dict["error"] = error
        if result is not UNSET:
            field_dict["result"] = result

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.raw_trace_call_action import RawTraceCallAction
        from ..models.raw_trace_call_result import RawTraceCallResult
        from ..models.raw_trace_create_action import RawTraceCreateAction
        from ..models.raw_trace_create_result import RawTraceCreateResult
        from ..models.raw_trace_self_destruct_action import RawTraceSelfDestructAction

        d = dict(src_dict)

        def _parse_action(
            data: object,
        ) -> Union["RawTraceCallAction", "RawTraceCreateAction", "RawTraceSelfDestructAction"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                action_type_0 = RawTraceCallAction.from_dict(data)

                return action_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                action_type_1 = RawTraceCreateAction.from_dict(data)

                return action_type_1
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            action_type_2 = RawTraceSelfDestructAction.from_dict(data)

            return action_type_2

        action = _parse_action(d.pop("action"))

        subtraces = d.pop("subtraces")

        trace_address = cast(list[int], d.pop("traceAddress"))

        type_ = d.pop("type")

        error = d.pop("error", UNSET)

        def _parse_result(data: object) -> Union["RawTraceCallResult", "RawTraceCreateResult", Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                result_type_0 = RawTraceCallResult.from_dict(data)

                return result_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            result_type_1 = RawTraceCreateResult.from_dict(data)

            return result_type_1

        result = _parse_result(d.pop("result", UNSET))

        raw_trace = cls(
            action=action,
            subtraces=subtraces,
            trace_address=trace_address,
            type_=type_,
            error=error,
            result=result,
        )

        raw_trace.additional_properties = d
        return raw_trace

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
