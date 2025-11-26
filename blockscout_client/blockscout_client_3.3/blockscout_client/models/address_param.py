from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.address_param_metadata import AddressParamMetadata
    from ..models.address_tag import AddressTag
    from ..models.watchlist_name import WatchlistName


T = TypeVar("T", bound="AddressParam")


@_attrs_define
class AddressParam:
    """
    Attributes:
        hash_ (str):  Example: 0xEb533ee5687044E622C69c58B1B12329F56eD9ad.
        implementation_name (str):  Example: implementationName.
        name (str):  Example: contractName.
        is_contract (bool):
        private_tags (list['AddressTag']):
        watchlist_names (list['WatchlistName']):
        public_tags (list['AddressTag']):
        is_verified (bool):
        ens_domain_name (Union[Unset, str]):  Example: domain.eth.
        metadata (Union[Unset, AddressParamMetadata]):  Example: {'slug': 'tag_slug', 'name': 'Tag name', 'tagType':
            'name', 'ordinal': 0, 'meta': {}}.
    """

    hash_: str
    implementation_name: str
    name: str
    is_contract: bool
    private_tags: list["AddressTag"]
    watchlist_names: list["WatchlistName"]
    public_tags: list["AddressTag"]
    is_verified: bool
    ens_domain_name: Union[Unset, str] = UNSET
    metadata: Union[Unset, "AddressParamMetadata"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        hash_ = self.hash_

        implementation_name = self.implementation_name

        name = self.name

        is_contract = self.is_contract

        private_tags = []
        for private_tags_item_data in self.private_tags:
            private_tags_item = private_tags_item_data.to_dict()
            private_tags.append(private_tags_item)

        watchlist_names = []
        for watchlist_names_item_data in self.watchlist_names:
            watchlist_names_item = watchlist_names_item_data.to_dict()
            watchlist_names.append(watchlist_names_item)

        public_tags = []
        for public_tags_item_data in self.public_tags:
            public_tags_item = public_tags_item_data.to_dict()
            public_tags.append(public_tags_item)

        is_verified = self.is_verified

        ens_domain_name = self.ens_domain_name

        metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "hash": hash_,
                "implementation_name": implementation_name,
                "name": name,
                "is_contract": is_contract,
                "private_tags": private_tags,
                "watchlist_names": watchlist_names,
                "public_tags": public_tags,
                "is_verified": is_verified,
            }
        )
        if ens_domain_name is not UNSET:
            field_dict["ens_domain_name"] = ens_domain_name
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.address_param_metadata import AddressParamMetadata
        from ..models.address_tag import AddressTag
        from ..models.watchlist_name import WatchlistName

        if src_dict is None:
            return None

        d = dict(src_dict)
        hash_ = d.pop("hash")

        implementation_name = d.pop("implementation_name", UNSET)

        name = d.pop("name", UNSET)

        is_contract = d.pop("is_contract", UNSET)

        private_tags = []
        _private_tags = d.pop("private_tags", UNSET)
        for private_tags_item_data in _private_tags:
            private_tags_item = AddressTag.from_dict(private_tags_item_data)

            private_tags.append(private_tags_item)

        watchlist_names = []
        _watchlist_names = d.pop("watchlist_names", UNSET)
        for watchlist_names_item_data in _watchlist_names:
            watchlist_names_item = WatchlistName.from_dict(watchlist_names_item_data)

            watchlist_names.append(watchlist_names_item)

        public_tags = []
        _public_tags = d.pop("public_tags", UNSET)
        for public_tags_item_data in _public_tags:
            public_tags_item = AddressTag.from_dict(public_tags_item_data)

            public_tags.append(public_tags_item)

        is_verified = d.pop("is_verified", UNSET)

        ens_domain_name = d.pop("ens_domain_name", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, AddressParamMetadata]
        if isinstance(_metadata, Unset) or _metadata is None:
            metadata = UNSET
        else:
            metadata = AddressParamMetadata.from_dict(_metadata)

        address_param = cls(
            hash_=hash_,
            implementation_name=implementation_name,
            name=name,
            is_contract=is_contract,
            private_tags=private_tags,
            watchlist_names=watchlist_names,
            public_tags=public_tags,
            is_verified=is_verified,
            ens_domain_name=ens_domain_name,
            metadata=metadata,
        )

        address_param.additional_properties = d
        return address_param

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
