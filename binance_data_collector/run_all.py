from binance_futures import store_funding_rate, store_liquidations, store_open_interest
from binance_options import store_option_chain
from binance_spot import store_agg_trades, store_order_book


def main():
    print("==== Spot Depth ====")
    print(store_order_book().head())

    print("==== Agg Trades ====")
    print(store_agg_trades().head())

    print("==== Futures ====")
    print(store_funding_rate().head())
    print(store_open_interest().head())
    print(store_liquidations().head())

    print("==== Option Chain ====")
    print(store_option_chain().head())


if __name__ == "__main__":
    main()
