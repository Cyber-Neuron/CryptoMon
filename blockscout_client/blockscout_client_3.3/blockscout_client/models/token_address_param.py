from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.address_tag import AddressTag
    from ..models.watchlist_name import WatchlistName


T = TypeVar("T", bound="TokenAddressParam")


@_attrs_define
class TokenAddressParam:
    """
    Attributes:
        hash_ (str):  Example: 0xEb533ee5687044E622C69c58B1B12329F56eD9ad.
        implementation_name (str):  Example: implementationName.
        name (str):  Example: contractName.
        is_contract (bool):
        is_verified (bool):
        private_tags (list['AddressTag']):
        public_tags (list['AddressTag']):
        watchlist_names (list['WatchlistName']):
        address (Union[Unset, str]): Address Example: 0x123abc....
    """

    hash_: str
    implementation_name: str
    name: str
    is_contract: bool
    is_verified: bool
    private_tags: list["AddressTag"]
    public_tags: list["AddressTag"]
    watchlist_names: list["WatchlistName"]
    address: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        hash_ = self.hash_

        implementation_name = self.implementation_name

        name = self.name

        is_contract = self.is_contract

        is_verified = self.is_verified

        private_tags = []
        for private_tags_item_data in self.private_tags:
            private_tags_item = private_tags_item_data.to_dict()
            private_tags.append(private_tags_item)

        public_tags = []
        for public_tags_item_data in self.public_tags:
            public_tags_item = public_tags_item_data.to_dict()
            public_tags.append(public_tags_item)

        watchlist_names = []
        for watchlist_names_item_data in self.watchlist_names:
            watchlist_names_item = watchlist_names_item_data.to_dict()
            watchlist_names.append(watchlist_names_item)

        address = self.address

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "hash": hash_,
                "implementation_name": implementation_name,
                "name": name,
                "is_contract": is_contract,
                "is_verified": is_verified,
                "private_tags": private_tags,
                "public_tags": public_tags,
                "watchlist_names": watchlist_names,
            }
        )
        if address is not UNSET:
            field_dict["address"] = address

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.address_tag import AddressTag
        from ..models.watchlist_name import WatchlistName

        d = dict(src_dict)
        hash_ = d.pop("hash")

        implementation_name = d.pop("implementation_name")

        name = d.pop("name")

        is_contract = d.pop("is_contract")

        is_verified = d.pop("is_verified")

        private_tags = []
        _private_tags = d.pop("private_tags")
        for private_tags_item_data in _private_tags:
            private_tags_item = AddressTag.from_dict(private_tags_item_data)

            private_tags.append(private_tags_item)

        public_tags = []
        _public_tags = d.pop("public_tags")
        for public_tags_item_data in _public_tags:
            public_tags_item = AddressTag.from_dict(public_tags_item_data)

            public_tags.append(public_tags_item)

        watchlist_names = []
        _watchlist_names = d.pop("watchlist_names")
        for watchlist_names_item_data in _watchlist_names:
            watchlist_names_item = WatchlistName.from_dict(watchlist_names_item_data)

            watchlist_names.append(watchlist_names_item)

        address = d.pop("address", UNSET)

        token_address_param = cls(
            hash_=hash_,
            implementation_name=implementation_name,
            name=name,
            is_contract=is_contract,
            is_verified=is_verified,
            private_tags=private_tags,
            public_tags=public_tags,
            watchlist_names=watchlist_names,
            address=address,
        )

        token_address_param.additional_properties = d
        return token_address_param

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
