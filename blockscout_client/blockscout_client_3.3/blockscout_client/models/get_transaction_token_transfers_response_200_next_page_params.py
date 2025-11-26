from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GetTransactionTokenTransfersResponse200NextPageParams")


@_attrs_define
class GetTransactionTokenTransfersResponse200NextPageParams:
    """
    Example:
        {'block_number': 27350206, 'index': 1, 'items_count': 50, 'transaction_hash':
            '0xa3b401d6f3124c9d1528cd8d4b692f523d86fd88e48c391ffe9c67e4436ae5ca'}

    """

    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        get_transaction_token_transfers_response_200_next_page_params = cls()

        get_transaction_token_transfers_response_200_next_page_params.additional_properties = d
        return get_transaction_token_transfers_response_200_next_page_params

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
