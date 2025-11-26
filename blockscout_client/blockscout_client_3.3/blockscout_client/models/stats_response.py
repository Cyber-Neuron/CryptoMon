from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.stats_response_gas_prices import StatsResponseGasPrices


T = TypeVar("T", bound="StatsResponse")


@_attrs_define
class StatsResponse:
    """
    Attributes:
        total_blocks (str):  Example: 508700.
        total_addresses (str):  Example: 982340.
        total_transactions (str):  Example: 1699427.
        average_block_time (float):  Example: 25000.
        coin_price (str):  Example: 0.00254957.
        total_gas_used (str):  Example: 0.
        transactions_today (str):  Example: 622.
        gas_used_today (str):  Example: 49063630.
        gas_prices (StatsResponseGasPrices):  Example: {'average': 10, 'fast': 10, 'slow': 10}.
        static_gas_price (str):  Example: 10.1.
        market_cap (str):  Example: 420471.10604559750644.
        network_utilization_percentage (float):  Example: 40.2142.
    """

    total_blocks: str
    total_addresses: str
    total_transactions: str
    average_block_time: float
    coin_price: str
    total_gas_used: str
    transactions_today: str
    gas_used_today: str
    gas_prices: "StatsResponseGasPrices"
    static_gas_price: str
    market_cap: str
    network_utilization_percentage: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total_blocks = self.total_blocks

        total_addresses = self.total_addresses

        total_transactions = self.total_transactions

        average_block_time = self.average_block_time

        coin_price = self.coin_price

        total_gas_used = self.total_gas_used

        transactions_today = self.transactions_today

        gas_used_today = self.gas_used_today

        gas_prices = self.gas_prices.to_dict()

        static_gas_price = self.static_gas_price

        market_cap = self.market_cap

        network_utilization_percentage = self.network_utilization_percentage

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total_blocks": total_blocks,
                "total_addresses": total_addresses,
                "total_transactions": total_transactions,
                "average_block_time": average_block_time,
                "coin_price": coin_price,
                "total_gas_used": total_gas_used,
                "transactions_today": transactions_today,
                "gas_used_today": gas_used_today,
                "gas_prices": gas_prices,
                "static_gas_price": static_gas_price,
                "market_cap": market_cap,
                "network_utilization_percentage": network_utilization_percentage,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.stats_response_gas_prices import StatsResponseGasPrices

        d = dict(src_dict)
        total_blocks = d.pop("total_blocks")

        total_addresses = d.pop("total_addresses")

        total_transactions = d.pop("total_transactions")

        average_block_time = d.pop("average_block_time")

        coin_price = d.pop("coin_price")

        total_gas_used = d.pop("total_gas_used")

        transactions_today = d.pop("transactions_today")

        gas_used_today = d.pop("gas_used_today")

        gas_prices = StatsResponseGasPrices.from_dict(d.pop("gas_prices"))

        static_gas_price = d.pop("static_gas_price")

        market_cap = d.pop("market_cap")

        network_utilization_percentage = d.pop("network_utilization_percentage")

        stats_response = cls(
            total_blocks=total_blocks,
            total_addresses=total_addresses,
            total_transactions=total_transactions,
            average_block_time=average_block_time,
            coin_price=coin_price,
            total_gas_used=total_gas_used,
            transactions_today=transactions_today,
            gas_used_today=gas_used_today,
            gas_prices=gas_prices,
            static_gas_price=static_gas_price,
            market_cap=market_cap,
            network_utilization_percentage=network_utilization_percentage,
        )

        stats_response.additional_properties = d
        return stats_response

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
