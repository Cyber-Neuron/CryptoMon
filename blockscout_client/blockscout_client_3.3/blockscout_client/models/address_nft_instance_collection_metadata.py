from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AddressNFTInstanceCollectionMetadata")


@_attrs_define
class AddressNFTInstanceCollectionMetadata:
    """
    Example:
        {'year': 2023, 'tags': ['poap', 'event'], 'name': 'Social Listening Committee #2 Attendees', 'image_url':
            'https://assets.poap.xyz/chanel-poap-4c-2023-logo-1675083420470.png', 'home_url':
            'https://app.poap.xyz/token/6292128', 'external_url': 'https://api.poap.tech/metadata/99010/6292128',
            'description': 'This is the POAP for attendees of the second Social Listening Committee.', 'attributes':
            [{'value': '01-Feb-2023', 'trait_type': 'startDate'}, {'value': '01-Feb-2023', 'trait_type': 'endDate'},
            {'value': 'false', 'trait_type': 'virtualEvent'}, {'value': 'Paris', 'trait_type': 'city'}, {'value': 'France',
            'trait_type': 'country'}, {'value': 'https://www.chanel.com', 'trait_type': 'eventURL'}]}

    """

    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        address_nft_instance_collection_metadata = cls()

        address_nft_instance_collection_metadata.additional_properties = d
        return address_nft_instance_collection_metadata

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
