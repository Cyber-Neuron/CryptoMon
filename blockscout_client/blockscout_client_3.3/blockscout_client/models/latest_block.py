from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.latest_block_cache import LatestBlockCache
    from ..models.latest_block_db import LatestBlockDb


T = TypeVar("T", bound="LatestBlock")


@_attrs_define
class LatestBlock:
    """
    Attributes:
        cache (Union[Unset, LatestBlockCache]):
        db (Union[Unset, LatestBlockDb]):
    """

    cache: Union[Unset, "LatestBlockCache"] = UNSET
    db: Union[Unset, "LatestBlockDb"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cache: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.cache, Unset):
            cache = self.cache.to_dict()

        db: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.db, Unset):
            db = self.db.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cache is not UNSET:
            field_dict["cache"] = cache
        if db is not UNSET:
            field_dict["db"] = db

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.latest_block_cache import LatestBlockCache
        from ..models.latest_block_db import LatestBlockDb

        d = dict(src_dict)
        _cache = d.pop("cache", UNSET)
        cache: Union[Unset, LatestBlockCache]
        if isinstance(_cache, Unset):
            cache = UNSET
        else:
            cache = LatestBlockCache.from_dict(_cache)

        _db = d.pop("db", UNSET)
        db: Union[Unset, LatestBlockDb]
        if isinstance(_db, Unset):
            db = UNSET
        else:
            db = LatestBlockDb.from_dict(_db)

        latest_block = cls(
            cache=cache,
            db=db,
        )

        latest_block.additional_properties = d
        return latest_block

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
