from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RawTraceCallAction")


@_attrs_define
class RawTraceCallAction:
    """
    Attributes:
        call_type (str):  Example: call.
        to (str):  Example: 0x162e898bd0aacb578c8d5f8d6ca588c13d2a383f.
        from_ (str):  Example: 0xf57b55b01b831e602e09674a4e5d69cbcf343f98.
        input_ (str):  Example: 0x630cea8e000000000000000000000000000000000000000000000000000000000000004000000000000000
            000000000000000000000000000000000000000000000000c000000000000000000000000000000000000000000000000000000000000000
            41c25b36779231e71769118210c3eb64c0a9c7577b925b309af3183e13acc7cf30210493d13c8c6c3c0bd337d5e39e454fece0c301f0aedb
            6c43c7a37650ac83e71c00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
            000000000000000000000000000000019500050000f0add9e5dc02faeca12e9669f045685449d6b80a000000000000744359447362798334
            d3485c64d1e4870fde2ddc0d75f0b456250dc9990662a6f25808cc74a6d1131ea9000927c001018064382ae87cdd00000000000000000000
            0000bab3cbdcbcc578445480a79ed80269c50bb5b71800000000000000000000000000000000000000000000000000000000000000c00000
            0000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000
            000000000012000000000000000000000000351af1631aa5ea1ca62ad8a4e3cd87128d4d9108000000000000000000000000000000000000
            00000000005b8decde02914ce837000000000000000000000000000000000000000000000000000000000000001e4d45444f4f5a41204563
            6f73797374656d2076322e30206f6e2078446169000000000000000000000000000000000000000000000000000000000000000000044d44
            5a41000000000000000000000000000000000000000000000000000000000000000000000000000000.
        gas (str):  Example: 0x25D3FC.
        value (str):  Example: 0x0.
    """

    call_type: str
    to: str
    from_: str
    input_: str
    gas: str
    value: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        call_type = self.call_type

        to = self.to

        from_ = self.from_

        input_ = self.input_

        gas = self.gas

        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "callType": call_type,
                "to": to,
                "from": from_,
                "input": input_,
                "gas": gas,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        call_type = d.pop("callType")

        to = d.pop("to")

        from_ = d.pop("from")

        input_ = d.pop("input")

        gas = d.pop("gas")

        value = d.pop("value")

        raw_trace_call_action = cls(
            call_type=call_type,
            to=to,
            from_=from_,
            input_=input_,
            gas=gas,
            value=value,
        )

        raw_trace_call_action.additional_properties = d
        return raw_trace_call_action

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
