from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="IndexingStatus")


@_attrs_define
class IndexingStatus:
    """
    Attributes:
        finished_indexing (bool):
        finished_indexing_blocks (bool):
        indexed_blocks_ratio (str):  Example: 1.0.
        indexed_internal_transactions_ratio (Union[None, str]):  Example: 1.0.
    """

    finished_indexing: bool
    finished_indexing_blocks: bool
    indexed_blocks_ratio: str
    indexed_internal_transactions_ratio: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        finished_indexing = self.finished_indexing

        finished_indexing_blocks = self.finished_indexing_blocks

        indexed_blocks_ratio = self.indexed_blocks_ratio

        indexed_internal_transactions_ratio: Union[None, str]
        indexed_internal_transactions_ratio = self.indexed_internal_transactions_ratio

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "finished_indexing": finished_indexing,
                "finished_indexing_blocks": finished_indexing_blocks,
                "indexed_blocks_ratio": indexed_blocks_ratio,
                "indexed_internal_transactions_ratio": indexed_internal_transactions_ratio,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        finished_indexing = d.pop("finished_indexing")

        finished_indexing_blocks = d.pop("finished_indexing_blocks")

        indexed_blocks_ratio = d.pop("indexed_blocks_ratio")

        def _parse_indexed_internal_transactions_ratio(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        indexed_internal_transactions_ratio = _parse_indexed_internal_transactions_ratio(
            d.pop("indexed_internal_transactions_ratio")
        )

        indexing_status = cls(
            finished_indexing=finished_indexing,
            finished_indexing_blocks=finished_indexing_blocks,
            indexed_blocks_ratio=indexed_blocks_ratio,
            indexed_internal_transactions_ratio=indexed_internal_transactions_ratio,
        )

        indexing_status.additional_properties = d
        return indexing_status

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
