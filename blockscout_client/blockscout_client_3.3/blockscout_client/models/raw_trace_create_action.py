from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RawTraceCreateAction")


@_attrs_define
class RawTraceCreateAction:
    """
    Attributes:
        from_ (str):  Example: 0xf57b55b01b831e602e09674a4e5d69cbcf343f98.
        gas (str):  Example: 0x25D3FC.
        init (str):  Example: 0x630cea8e00000000000000000000000000000000000000000000000000000000000000400000000000000000
            0000000000000000000000000000000000000000000000c00000000000000000000000000000000000000000000000000000000000000041
            c25b36779231e71769118210c3eb64c0a9c7577b925b309af3183e13acc7cf30210493d13c8c6c3c0bd337d5e39e454fece0c301f0aedb6c
            43c7a37650ac83e71c0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
            0000000000000000000000000000019500050000f0add9e5dc02faeca12e9669f045685449d6b80a000000000000744359447362798334d3
            485c64d1e4870fde2ddc0d75f0b456250dc9990662a6f25808cc74a6d1131ea9000927c001018064382ae87cdd0000000000000000000000
            00bab3cbdcbcc578445480a79ed80269c50bb5b71800000000000000000000000000000000000000000000000000000000000000c0000000
            0000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000
            0000000012000000000000000000000000351af1631aa5ea1ca62ad8a4e3cd87128d4d910800000000000000000000000000000000000000
            000000005b8decde02914ce837000000000000000000000000000000000000000000000000000000000000001e4d45444f4f5a412045636f
            73797374656d2076322e30206f6e2078446169000000000000000000000000000000000000000000000000000000000000000000044d445a
            41000000000000000000000000000000000000000000000000000000000000000000000000000000.
        value (str):  Example: 0x0.
    """

    from_: str
    gas: str
    init: str
    value: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from_ = self.from_

        gas = self.gas

        init = self.init

        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "from": from_,
                "gas": gas,
                "init": init,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        from_ = d.pop("from")

        gas = d.pop("gas")

        init = d.pop("init")

        value = d.pop("value")

        raw_trace_create_action = cls(
            from_=from_,
            gas=gas,
            init=init,
            value=value,
        )

        raw_trace_create_action.additional_properties = d
        return raw_trace_create_action

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
