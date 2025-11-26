from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.address_param import AddressParam
    from ..models.decoded_input import DecodedInput
    from ..models.fee import Fee
    from ..models.token_transfer import TokenTransfer
    from ..models.transaction_action_aave_v3_enable_disable_collateral import (
        TransactionActionAaveV3EnableDisableCollateral,
    )
    from ..models.transaction_action_aave_v3_liquidation_call import (
        TransactionActionAaveV3LiquidationCall,
    )
    from ..models.transaction_action_aave_v3bswrf import TransactionActionAaveV3BSWRF
    from ..models.transaction_action_uniswap_v3_mint_nft import (
        TransactionActionUniswapV3MintNFT,
    )
    from ..models.transaction_action_uniswap_v3bcs import TransactionActionUniswapV3BCS
    from ..models.transaction_confirmation_duration import (
        TransactionConfirmationDuration,
    )


T = TypeVar("T", bound="Transaction")


@_attrs_define
class Transaction:
    """
    Attributes:
        timestamp (str):  Example: 2022-08-02T07:18:05.000000Z.
        fee (Fee):
        gas_limit (int):
        block_number (int):  Example: 23484035.
        status (str):  Example: ok | error.
        method (str):  Example: transferFrom.
        confirmations (int):  Example: 1035.
        type_ (int):  Example: 2.
        exchange_rate (str):  Example: 1866.51.
        to (AddressParam):
        transaction_burnt_fee (str):  Example: 1099596081903840.
        max_fee_per_gas (str):  Example: 55357460102.
        result (str):  Example: Error: (Awaiting internal transactions for reason).
        hash_ (str):  Example: 0x5d90a9da2b8da402b11bc92c8011ec8a62a2d59da5c7ac4ae0f73ec51bb73368.
        gas_price (str):  Example: 26668595172.
        priority_fee (str):  Example: 2056916056308.
        base_fee_per_gas (str):  Example: 26618801760.
        from_ (AddressParam):
        token_transfers (list['TokenTransfer']):
        transaction_types (list[str]):  Example: ['token_transfer', 'contract_creation', 'contract_call',
            'token_creation', 'coin_transfer'].
        gas_used (str):  Example: 41309.
        created_contract (AddressParam):
        position (int):  Example: 117.
        nonce (int):  Example: 115.
        has_error_in_internal_transactions (bool):
        actions (list[Union['TransactionActionAaveV3BSWRF', 'TransactionActionAaveV3EnableDisableCollateral',
            'TransactionActionAaveV3LiquidationCall', 'TransactionActionUniswapV3BCS',
            'TransactionActionUniswapV3MintNFT']]):
        decoded_input (DecodedInput):
        token_transfers_overflow (bool):
        raw_input (str):  Example: 0xa9059cbb000000000000000000000000ef8801eaf234ff82801821ffe2d78d60a0237f9700000000000
            0000000000000000000000000000000000000000000003178cb80.
        value (str):  Example: 0.
        max_priority_fee_per_gas (str):  Example: 49793412.
        revert_reason (str):  Example: Error: (Awaiting internal transactions for reason).
        confirmation_duration (TransactionConfirmationDuration):  Example: [0, 17479].
        transaction_tag (str):  Example: private_transaction_tag.
    """

    timestamp: str
    fee: "Fee"
    gas_limit: int
    block_number: int
    status: str
    method: str
    confirmations: int
    type_: int
    exchange_rate: str
    to: "AddressParam"
    transaction_burnt_fee: str
    max_fee_per_gas: str
    result: str
    hash_: str
    gas_price: str
    priority_fee: str
    base_fee_per_gas: str
    from_: "AddressParam"
    token_transfers: list["TokenTransfer"]
    transaction_types: list[str]
    gas_used: str
    created_contract: "AddressParam"
    position: int
    nonce: int
    has_error_in_internal_transactions: bool
    actions: list[
        Union[
            "TransactionActionAaveV3BSWRF",
            "TransactionActionAaveV3EnableDisableCollateral",
            "TransactionActionAaveV3LiquidationCall",
            "TransactionActionUniswapV3BCS",
            "TransactionActionUniswapV3MintNFT",
        ]
    ]
    decoded_input: "DecodedInput"
    token_transfers_overflow: bool
    raw_input: str
    value: str
    max_priority_fee_per_gas: str
    revert_reason: str
    confirmation_duration: "TransactionConfirmationDuration"
    transaction_tag: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.transaction_action_aave_v3_enable_disable_collateral import (
            TransactionActionAaveV3EnableDisableCollateral,
        )
        from ..models.transaction_action_aave_v3_liquidation_call import (
            TransactionActionAaveV3LiquidationCall,
        )
        from ..models.transaction_action_aave_v3bswrf import (
            TransactionActionAaveV3BSWRF,
        )
        from ..models.transaction_action_uniswap_v3_mint_nft import (
            TransactionActionUniswapV3MintNFT,
        )

        timestamp = self.timestamp

        fee = self.fee.to_dict()

        gas_limit = self.gas_limit

        block_number = self.block_number

        status = self.status

        method = self.method

        confirmations = self.confirmations

        type_ = self.type_

        exchange_rate = self.exchange_rate

        to = self.to.to_dict()

        transaction_burnt_fee = self.transaction_burnt_fee

        max_fee_per_gas = self.max_fee_per_gas

        result = self.result

        hash_ = self.hash_

        gas_price = self.gas_price

        priority_fee = self.priority_fee

        base_fee_per_gas = self.base_fee_per_gas

        from_ = self.from_.to_dict()

        token_transfers = []
        for token_transfers_item_data in self.token_transfers:
            token_transfers_item = token_transfers_item_data.to_dict()
            token_transfers.append(token_transfers_item)

        transaction_types = self.transaction_types

        gas_used = self.gas_used

        created_contract = self.created_contract.to_dict()

        position = self.position

        nonce = self.nonce

        has_error_in_internal_transactions = self.has_error_in_internal_transactions

        actions = []
        for actions_item_data in self.actions:
            actions_item: dict[str, Any]
            if isinstance(actions_item_data, TransactionActionAaveV3LiquidationCall):
                actions_item = actions_item_data.to_dict()
            elif isinstance(actions_item_data, TransactionActionAaveV3BSWRF):
                actions_item = actions_item_data.to_dict()
            elif isinstance(
                actions_item_data, TransactionActionAaveV3EnableDisableCollateral
            ):
                actions_item = actions_item_data.to_dict()
            elif isinstance(actions_item_data, TransactionActionUniswapV3MintNFT):
                actions_item = actions_item_data.to_dict()
            else:
                actions_item = actions_item_data.to_dict()

            actions.append(actions_item)

        decoded_input = self.decoded_input.to_dict()

        token_transfers_overflow = self.token_transfers_overflow

        raw_input = self.raw_input

        value = self.value

        max_priority_fee_per_gas = self.max_priority_fee_per_gas

        revert_reason = self.revert_reason

        confirmation_duration = self.confirmation_duration.to_dict()

        transaction_tag = self.transaction_tag

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "timestamp": timestamp,
                "fee": fee,
                "gas_limit": gas_limit,
                "block_number": block_number,
                "status": status,
                "method": method,
                "confirmations": confirmations,
                "type": type_,
                "exchange_rate": exchange_rate,
                "to": to,
                "transaction_burnt_fee": transaction_burnt_fee,
                "max_fee_per_gas": max_fee_per_gas,
                "result": result,
                "hash": hash_,
                "gas_price": gas_price,
                "priority_fee": priority_fee,
                "base_fee_per_gas": base_fee_per_gas,
                "from": from_,
                "token_transfers": token_transfers,
                "transaction_types": transaction_types,
                "gas_used": gas_used,
                "created_contract": created_contract,
                "position": position,
                "nonce": nonce,
                "has_error_in_internal_transactions": has_error_in_internal_transactions,
                "actions": actions,
                "decoded_input": decoded_input,
                "token_transfers_overflow": token_transfers_overflow,
                "raw_input": raw_input,
                "value": value,
                "max_priority_fee_per_gas": max_priority_fee_per_gas,
                "revert_reason": revert_reason,
                "confirmation_duration": confirmation_duration,
                "transaction_tag": transaction_tag,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.address_param import AddressParam
        from ..models.decoded_input import DecodedInput
        from ..models.fee import Fee
        from ..models.token_transfer import TokenTransfer
        from ..models.transaction_action_aave_v3_enable_disable_collateral import (
            TransactionActionAaveV3EnableDisableCollateral,
        )
        from ..models.transaction_action_aave_v3_liquidation_call import (
            TransactionActionAaveV3LiquidationCall,
        )
        from ..models.transaction_action_aave_v3bswrf import (
            TransactionActionAaveV3BSWRF,
        )
        from ..models.transaction_action_uniswap_v3_mint_nft import (
            TransactionActionUniswapV3MintNFT,
        )
        from ..models.transaction_action_uniswap_v3bcs import (
            TransactionActionUniswapV3BCS,
        )
        from ..models.transaction_confirmation_duration import (
            TransactionConfirmationDuration,
        )

        d = dict(src_dict)
        timestamp = d.pop("timestamp")

        fee = Fee.from_dict(d.pop("fee"))

        gas_limit = d.pop("gas_limit")

        block_number = d.pop("block_number")

        status = d.pop("status")

        method = d.pop("method")

        confirmations = d.pop("confirmations")

        type_ = d.pop("type")

        exchange_rate = d.pop("exchange_rate")

        to = AddressParam.from_dict(d.pop("to"))

        transaction_burnt_fee = d.pop("transaction_burnt_fee")

        max_fee_per_gas = d.pop("max_fee_per_gas")

        result = d.pop("result")

        hash_ = d.pop("hash")

        gas_price = d.pop("gas_price")

        priority_fee = d.pop("priority_fee")

        base_fee_per_gas = d.pop("base_fee_per_gas")

        from_ = AddressParam.from_dict(d.pop("from"))

        token_transfers = []
        _token_transfers = d.pop("token_transfers")
        for token_transfers_item_data in _token_transfers:
            token_transfers_item = TokenTransfer.from_dict(token_transfers_item_data)

            token_transfers.append(token_transfers_item)

        transaction_types = cast(list[str], d.pop("transaction_types"))

        gas_used = d.pop("gas_used")

        created_contract = AddressParam.from_dict(d.pop("created_contract", None))

        position = d.pop("position")

        nonce = d.pop("nonce")

        has_error_in_internal_transactions = d.pop("has_error_in_internal_transactions")

        actions = []
        _actions = d.pop("actions")
        for actions_item_data in _actions:

            def _parse_actions_item(
                data: object,
            ) -> Union[
                "TransactionActionAaveV3BSWRF",
                "TransactionActionAaveV3EnableDisableCollateral",
                "TransactionActionAaveV3LiquidationCall",
                "TransactionActionUniswapV3BCS",
                "TransactionActionUniswapV3MintNFT",
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_transaction_action_type_0 = (
                        TransactionActionAaveV3LiquidationCall.from_dict(data)
                    )

                    return componentsschemas_transaction_action_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_transaction_action_type_1 = (
                        TransactionActionAaveV3BSWRF.from_dict(data)
                    )

                    return componentsschemas_transaction_action_type_1
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_transaction_action_type_2 = (
                        TransactionActionAaveV3EnableDisableCollateral.from_dict(data)
                    )

                    return componentsschemas_transaction_action_type_2
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_transaction_action_type_3 = (
                        TransactionActionUniswapV3MintNFT.from_dict(data)
                    )

                    return componentsschemas_transaction_action_type_3
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_transaction_action_type_4 = (
                    TransactionActionUniswapV3BCS.from_dict(data)
                )

                return componentsschemas_transaction_action_type_4

            actions_item = _parse_actions_item(actions_item_data)

            actions.append(actions_item)

        decoded_input = DecodedInput.from_dict(d.pop("decoded_input"))

        token_transfers_overflow = d.pop("token_transfers_overflow")

        raw_input = d.pop("raw_input")

        value = d.pop("value")

        max_priority_fee_per_gas = d.pop("max_priority_fee_per_gas")

        revert_reason = d.pop("revert_reason")

        confirmation_duration = TransactionConfirmationDuration.from_dict(
            d.pop("confirmation_duration")
        )

        transaction_tag = d.pop("transaction_tag")

        transaction = cls(
            timestamp=timestamp,
            fee=fee,
            gas_limit=gas_limit,
            block_number=block_number,
            status=status,
            method=method,
            confirmations=confirmations,
            type_=type_,
            exchange_rate=exchange_rate,
            to=to,
            transaction_burnt_fee=transaction_burnt_fee,
            max_fee_per_gas=max_fee_per_gas,
            result=result,
            hash_=hash_,
            gas_price=gas_price,
            priority_fee=priority_fee,
            base_fee_per_gas=base_fee_per_gas,
            from_=from_,
            token_transfers=token_transfers,
            transaction_types=transaction_types,
            gas_used=gas_used,
            created_contract=created_contract,
            position=position,
            nonce=nonce,
            has_error_in_internal_transactions=has_error_in_internal_transactions,
            actions=actions,
            decoded_input=decoded_input,
            token_transfers_overflow=token_transfers_overflow,
            raw_input=raw_input,
            value=value,
            max_priority_fee_per_gas=max_priority_fee_per_gas,
            revert_reason=revert_reason,
            confirmation_duration=confirmation_duration,
            transaction_tag=transaction_tag,
        )

        transaction.additional_properties = d
        return transaction

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
