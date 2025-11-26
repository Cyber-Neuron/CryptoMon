from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.search_response_200_next_page_params import SearchResponse200NextPageParams
    from ..models.search_result_address_or_contract import SearchResultAddressOrContract
    from ..models.search_result_block import SearchResultBlock
    from ..models.search_result_token import SearchResultToken
    from ..models.search_result_transaction import SearchResultTransaction


T = TypeVar("T", bound="SearchResponse200")


@_attrs_define
class SearchResponse200:
    """
    Attributes:
        items (list[Union['SearchResultAddressOrContract', 'SearchResultBlock', 'SearchResultToken',
            'SearchResultTransaction']]):
        next_page_params (SearchResponse200NextPageParams):  Example: {'address_hash':
            '0x052Ad78E3aA0b0F2D3912FD3b50a9a289CF2f7Aa', 'block_hash': None, 'holder_count': 548, 'inserted_at':
            '2021-12-07T08:39:01.062253Z', 'item_type': 'token', 'items_count': 50, 'name': 'RealToken S 13245 Monica St
            Detroit MI', 'q': '1', 'transaction_hash': None}.
    """

    items: list[
        Union["SearchResultAddressOrContract", "SearchResultBlock", "SearchResultToken", "SearchResultTransaction"]
    ]
    next_page_params: "SearchResponse200NextPageParams"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.search_result_address_or_contract import SearchResultAddressOrContract
        from ..models.search_result_block import SearchResultBlock
        from ..models.search_result_token import SearchResultToken

        items = []
        for items_item_data in self.items:
            items_item: dict[str, Any]
            if isinstance(items_item_data, SearchResultToken):
                items_item = items_item_data.to_dict()
            elif isinstance(items_item_data, SearchResultAddressOrContract):
                items_item = items_item_data.to_dict()
            elif isinstance(items_item_data, SearchResultBlock):
                items_item = items_item_data.to_dict()
            else:
                items_item = items_item_data.to_dict()

            items.append(items_item)

        next_page_params = self.next_page_params.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "items": items,
                "next_page_params": next_page_params,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.search_response_200_next_page_params import SearchResponse200NextPageParams
        from ..models.search_result_address_or_contract import SearchResultAddressOrContract
        from ..models.search_result_block import SearchResultBlock
        from ..models.search_result_token import SearchResultToken
        from ..models.search_result_transaction import SearchResultTransaction

        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in _items:

            def _parse_items_item(
                data: object,
            ) -> Union[
                "SearchResultAddressOrContract", "SearchResultBlock", "SearchResultToken", "SearchResultTransaction"
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    items_item_type_0 = SearchResultToken.from_dict(data)

                    return items_item_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    items_item_type_1 = SearchResultAddressOrContract.from_dict(data)

                    return items_item_type_1
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    items_item_type_2 = SearchResultBlock.from_dict(data)

                    return items_item_type_2
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                items_item_type_3 = SearchResultTransaction.from_dict(data)

                return items_item_type_3

            items_item = _parse_items_item(items_item_data)

            items.append(items_item)

        next_page_params = SearchResponse200NextPageParams.from_dict(d.pop("next_page_params"))

        search_response_200 = cls(
            items=items,
            next_page_params=next_page_params,
        )

        search_response_200.additional_properties = d
        return search_response_200

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
