from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.address_nft_instance_collection_metadata import AddressNFTInstanceCollectionMetadata
    from ..models.address_nft_instance_collection_token import AddressNFTInstanceCollectionToken
    from ..models.address_param import AddressParam


T = TypeVar("T", bound="AddressNFTInstanceCollection")


@_attrs_define
class AddressNFTInstanceCollection:
    """
    Attributes:
        is_unique (bool):
        id (str):  Example: 431.
        owner (AddressParam):
        token_type (str):  Example: ERC-721.
        value (str):  Example: 1.
        holder_address_hash (Union[Unset, str]):  Example: 0x394c399dbA25B99Ab7708EdB505d755B3aa29997.
        image_url (Union[Unset, str]):  Example: example.com/picture.png.
        animation_url (Union[Unset, str]):  Example: example.com/video.mp4.
        external_app_url (Union[Unset, str]):  Example: d-app.com.
        metadata (Union[Unset, AddressNFTInstanceCollectionMetadata]):  Example: {'year': 2023, 'tags': ['poap',
            'event'], 'name': 'Social Listening Committee #2 Attendees', 'image_url': 'https://assets.poap.xyz/chanel-
            poap-4c-2023-logo-1675083420470.png', 'home_url': 'https://app.poap.xyz/token/6292128', 'external_url':
            'https://api.poap.tech/metadata/99010/6292128', 'description': 'This is the POAP for attendees of the second
            Social Listening Committee.', 'attributes': [{'value': '01-Feb-2023', 'trait_type': 'startDate'}, {'value':
            '01-Feb-2023', 'trait_type': 'endDate'}, {'value': 'false', 'trait_type': 'virtualEvent'}, {'value': 'Paris',
            'trait_type': 'city'}, {'value': 'France', 'trait_type': 'country'}, {'value': 'https://www.chanel.com',
            'trait_type': 'eventURL'}]}.
        token (Union[Unset, AddressNFTInstanceCollectionToken]):
    """

    is_unique: bool
    id: str
    owner: "AddressParam"
    token_type: str
    value: str
    holder_address_hash: Union[Unset, str] = UNSET
    image_url: Union[Unset, str] = UNSET
    animation_url: Union[Unset, str] = UNSET
    external_app_url: Union[Unset, str] = UNSET
    metadata: Union[Unset, "AddressNFTInstanceCollectionMetadata"] = UNSET
    token: Union[Unset, "AddressNFTInstanceCollectionToken"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        is_unique = self.is_unique

        id = self.id

        owner = self.owner.to_dict()

        token_type = self.token_type

        value = self.value

        holder_address_hash = self.holder_address_hash

        image_url = self.image_url

        animation_url = self.animation_url

        external_app_url = self.external_app_url

        metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        token: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.token, Unset):
            token = self.token.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "is_unique": is_unique,
                "id": id,
                "owner": owner,
                "token_type": token_type,
                "value": value,
            }
        )
        if holder_address_hash is not UNSET:
            field_dict["holder_address_hash"] = holder_address_hash
        if image_url is not UNSET:
            field_dict["image_url"] = image_url
        if animation_url is not UNSET:
            field_dict["animation_url"] = animation_url
        if external_app_url is not UNSET:
            field_dict["external_app_url"] = external_app_url
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if token is not UNSET:
            field_dict["token"] = token

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.address_nft_instance_collection_metadata import AddressNFTInstanceCollectionMetadata
        from ..models.address_nft_instance_collection_token import AddressNFTInstanceCollectionToken
        from ..models.address_param import AddressParam

        d = dict(src_dict)
        is_unique = d.pop("is_unique")

        id = d.pop("id")

        owner = AddressParam.from_dict(d.pop("owner"))

        token_type = d.pop("token_type")

        value = d.pop("value")

        holder_address_hash = d.pop("holder_address_hash", UNSET)

        image_url = d.pop("image_url", UNSET)

        animation_url = d.pop("animation_url", UNSET)

        external_app_url = d.pop("external_app_url", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, AddressNFTInstanceCollectionMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = AddressNFTInstanceCollectionMetadata.from_dict(_metadata)

        _token = d.pop("token", UNSET)
        token: Union[Unset, AddressNFTInstanceCollectionToken]
        if isinstance(_token, Unset):
            token = UNSET
        else:
            token = AddressNFTInstanceCollectionToken.from_dict(_token)

        address_nft_instance_collection = cls(
            is_unique=is_unique,
            id=id,
            owner=owner,
            token_type=token_type,
            value=value,
            holder_address_hash=holder_address_hash,
            image_url=image_url,
            animation_url=animation_url,
            external_app_url=external_app_url,
            metadata=metadata,
            token=token,
        )

        address_nft_instance_collection.additional_properties = d
        return address_nft_instance_collection

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
