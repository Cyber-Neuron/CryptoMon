from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.transaction_action_aave_v3bswrf_data import TransactionActionAaveV3BSWRFData


T = TypeVar("T", bound="TransactionActionAaveV3BSWRF")


@_attrs_define
class TransactionActionAaveV3BSWRF:
    """
    Attributes:
        data (TransactionActionAaveV3BSWRFData):  Example: {'amount': '1.289548595490270429', 'symbol': 'AAVE',
            'address': '0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9', 'block_number': 1}.
        protocol (str):  Example: aave_v3.
        type_ (str):  Example: borrow | supply | withdraw | repay | flash_loan.
    """

    data: "TransactionActionAaveV3BSWRFData"
    protocol: str
    type_: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

        protocol = self.protocol

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
                "protocol": protocol,
                "type": type_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.transaction_action_aave_v3bswrf_data import TransactionActionAaveV3BSWRFData

        d = dict(src_dict)
        data = TransactionActionAaveV3BSWRFData.from_dict(d.pop("data"))

        protocol = d.pop("protocol")

        type_ = d.pop("type")

        transaction_action_aave_v3bswrf = cls(
            data=data,
            protocol=protocol,
            type_=type_,
        )

        transaction_action_aave_v3bswrf.additional_properties = d
        return transaction_action_aave_v3bswrf

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
