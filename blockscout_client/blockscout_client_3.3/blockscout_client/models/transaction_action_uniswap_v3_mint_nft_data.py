from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="TransactionActionUniswapV3MintNFTData")


@_attrs_define
class TransactionActionUniswapV3MintNFTData:
    """
    Example:
        {'name': 'Uniswap V3: Positions NFT', 'symbol': 'UNI-V3-POS', 'address':
            '0x1F98431c8aD98523631AE4a59f267346ea31F984', 'to': '0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9', 'ids': ['1',
            '2'], 'block_number': 1}

    """

    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        transaction_action_uniswap_v3_mint_nft_data = cls()

        transaction_action_uniswap_v3_mint_nft_data.additional_properties = d
        return transaction_action_uniswap_v3_mint_nft_data

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
