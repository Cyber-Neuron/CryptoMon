from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.address_param import AddressParam
    from ..models.token_info import TokenInfo
    from ..models.total_erc20 import TotalERC20
    from ..models.total_erc721 import TotalERC721
    from ..models.total_erc1155 import TotalERC1155


T = TypeVar("T", bound="TokenTransfer")


@_attrs_define
class TokenTransfer:
    """
    Attributes:
        block_hash (str):  Example: 0xf569ec751152b2f814001fc730f7797aa155e4bc3ba9cb6ba24bc2c8c9468c1a.
        from_ (AddressParam):
        log_index (str):  Example: 243.
        method (str):  Example: transfer.
        timestamp (str):  Example: 2023-07-03T20:09:59.000000Z.
        to (AddressParam):
        token (TokenInfo):
        total (Union['TotalERC1155', 'TotalERC20', 'TotalERC721']):
        transaction_hash (str):  Example: 0x6662ad1ad2ea899e9e27832dc202fd2ef915a5d2816c1142e6933cff93f7c592.
        type_ (str):  Example: token_transfer.
    """

    block_hash: str
    from_: "AddressParam"
    log_index: str
    method: str
    timestamp: str
    to: "AddressParam"
    token: "TokenInfo"
    total: Union["TotalERC1155", "TotalERC20", "TotalERC721"]
    transaction_hash: str
    type_: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.total_erc20 import TotalERC20
        from ..models.total_erc721 import TotalERC721

        block_hash = self.block_hash

        from_ = self.from_.to_dict()

        log_index = self.log_index

        method = self.method

        timestamp = self.timestamp

        to = self.to.to_dict()

        token = self.token.to_dict()

        total: dict[str, Any]
        if isinstance(self.total, TotalERC20):
            total = self.total.to_dict()
        elif isinstance(self.total, TotalERC721):
            total = self.total.to_dict()
        else:
            total = self.total.to_dict()

        transaction_hash = self.transaction_hash

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "block_hash": block_hash,
                "from": from_,
                "log_index": log_index,
                "method": method,
                "timestamp": timestamp,
                "to": to,
                "token": token,
                "total": total,
                "transaction_hash": transaction_hash,
                "type": type_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.address_param import AddressParam
        from ..models.token_info import TokenInfo
        from ..models.total_erc20 import TotalERC20
        from ..models.total_erc721 import TotalERC721
        from ..models.total_erc1155 import TotalERC1155

        d = dict(src_dict)
        block_hash = d.pop("block_hash")

        from_ = AddressParam.from_dict(d.pop("from"))

        log_index = d.pop("log_index")

        method = d.pop("method")

        timestamp = d.pop("timestamp")

        to = AddressParam.from_dict(d.pop("to"))

        token = TokenInfo.from_dict(d.pop("token"))

        def _parse_total(data: object) -> Union["TotalERC1155", "TotalERC20", "TotalERC721"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                total_type_0 = TotalERC20.from_dict(data)

                return total_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                total_type_1 = TotalERC721.from_dict(data)

                return total_type_1
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            total_type_2 = TotalERC1155.from_dict(data)

            return total_type_2

        total = _parse_total(d.pop("total"))

        transaction_hash = d.pop("transaction_hash")

        type_ = d.pop("type")

        token_transfer = cls(
            block_hash=block_hash,
            from_=from_,
            log_index=log_index,
            method=method,
            timestamp=timestamp,
            to=to,
            token=token,
            total=total,
            transaction_hash=transaction_hash,
            type_=type_,
        )

        token_transfer.additional_properties = d
        return token_transfer

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
