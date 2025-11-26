from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.address_param import AddressParam
    from ..models.nft_change import NFTChange
    from ..models.token_info import TokenInfo


T = TypeVar("T", bound="StateChange")


@_attrs_define
class StateChange:
    """
    Attributes:
        type_ (str):  Example: coin | token.
        is_miner (bool):
        address (AddressParam):
        token (Union[Unset, TokenInfo]):
        balance_before (Union[Unset, str]):  Example: 100000000.
        balance_after (Union[Unset, str]):  Example: 100000000.
        token_id (Union[Unset, str]):
        change (Union[Unset, list['NFTChange'], str]):
    """

    type_: str
    is_miner: bool
    address: "AddressParam"
    token: Union[Unset, "TokenInfo"] = UNSET
    balance_before: Union[Unset, str] = UNSET
    balance_after: Union[Unset, str] = UNSET
    token_id: Union[Unset, str] = UNSET
    change: Union[Unset, list["NFTChange"], str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        is_miner = self.is_miner

        address = self.address.to_dict()

        token: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.token, Unset):
            token = self.token.to_dict()

        balance_before = self.balance_before

        balance_after = self.balance_after

        token_id = self.token_id

        change: Union[Unset, list[dict[str, Any]], str]
        if isinstance(self.change, Unset):
            change = UNSET
        elif isinstance(self.change, list):
            change = []
            for componentsschemas_nft_changes_array_item_data in self.change:
                componentsschemas_nft_changes_array_item = componentsschemas_nft_changes_array_item_data.to_dict()
                change.append(componentsschemas_nft_changes_array_item)

        else:
            change = self.change

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "is_miner": is_miner,
                "address": address,
            }
        )
        if token is not UNSET:
            field_dict["token"] = token
        if balance_before is not UNSET:
            field_dict["balance_before"] = balance_before
        if balance_after is not UNSET:
            field_dict["balance_after"] = balance_after
        if token_id is not UNSET:
            field_dict["token_id"] = token_id
        if change is not UNSET:
            field_dict["change"] = change

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.address_param import AddressParam
        from ..models.nft_change import NFTChange
        from ..models.token_info import TokenInfo

        d = dict(src_dict)
        type_ = d.pop("type")

        is_miner = d.pop("is_miner")

        address = AddressParam.from_dict(d.pop("address"))

        _token = d.pop("token", UNSET)
        token: Union[Unset, TokenInfo]
        if isinstance(_token, Unset):
            token = UNSET
        else:
            token = TokenInfo.from_dict(_token)

        balance_before = d.pop("balance_before", UNSET)

        balance_after = d.pop("balance_after", UNSET)

        token_id = d.pop("token_id", UNSET)

        def _parse_change(data: object) -> Union[Unset, list["NFTChange"], str]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                change_type_0 = []
                _change_type_0 = data
                for componentsschemas_nft_changes_array_item_data in _change_type_0:
                    componentsschemas_nft_changes_array_item = NFTChange.from_dict(
                        componentsschemas_nft_changes_array_item_data
                    )

                    change_type_0.append(componentsschemas_nft_changes_array_item)

                return change_type_0
            except:  # noqa: E722
                pass
            return cast(Union[Unset, list["NFTChange"], str], data)

        change = _parse_change(d.pop("change", UNSET))

        state_change = cls(
            type_=type_,
            is_miner=is_miner,
            address=address,
            token=token,
            balance_before=balance_before,
            balance_after=balance_after,
            token_id=token_id,
            change=change,
        )

        state_change.additional_properties = d
        return state_change

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
