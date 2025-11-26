# Binance Comprehensive On-Chain/Market/Derivatives Data Collection Toolkit

## Feature Modules
- Spot depth (buy/sell walls, order book levels, trade details)
- Perpetual/Delivery contract Funding Rate, Open Interest
- Contract liquidation orders (Liquidations)
- Options chain, IV curve snapshots
- Can supplement with your own on-chain flows (e.g., Etherscan/Nansen, etc.)

## Quick Start
1. `pip install -r requirements.txt`
2. Write Binance API KEY/SECRET to `config.yaml`
3. Run individual modules, e.g.: `python binance_futures.py`
4. Batch collection: `python run_all.py`

## Description
- **Order Book/Trades:** Reflects spot order book depth/liquidity, buy/sell wall pressure, and order consumption.
- **Funding/Open Interest:** Captures long/short divergence/extreme leverage behavior.
- **Liquidations:** Liquidation map during high volatility periods, often resonating with "price spikes".
- **Options:** Complete ETH/BTC/BNB options chain overview, convenient for analyzing major volatility betting directions.
- **Supplement on-chain fund flows (e.g., large transfers)**:
  - Recommended to use [etherscan.io](https://etherscan.io/token/0x...) API to fetch ERC20 Transfers
  - Or [Nansen Query API](https://www.nansen.ai/) to supplement cross-chain transfers, stablecoin supply changes

## Extension Options
- ETF subscriptions/redemptions, leveraged tokens, and other data can refer to Binance official API documentation, or supplement with requests collection scripts.
- Account fund flows, positions, etc. require API KEY configuration, see `config.yaml` for details.

## Directory Structure

```
binance_data_collector/
├── README.md
├── requirements.txt
├── config.yaml
├── binance_spot.py
├── binance_futures.py
├── binance_options.py
└── run_all.py
```

## Database Schema

Please execute the following SQL to create tables in PostgreSQL first:

```sql
CREATE TABLE spot_order_book (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    side VARCHAR(4) NOT NULL,
    price NUMERIC(32, 12) NOT NULL,
    quantity NUMERIC(32, 12) NOT NULL,
    snapshot_time TIMESTAMP NOT NULL,
    UNIQUE(symbol, side, price, snapshot_time)
);

CREATE TABLE spot_agg_trades (
    id BIGSERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    agg_trade_id BIGINT NOT NULL,
    price NUMERIC(32, 12) NOT NULL,
    quantity NUMERIC(32, 12) NOT NULL,
    first_trade_id BIGINT,
    last_trade_id BIGINT,
    trade_time TIMESTAMP NOT NULL,
    is_buyer_maker BOOLEAN,
    snapshot_time TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE(symbol, agg_trade_id)
);

CREATE TABLE futures_funding_rate (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    funding_time TIMESTAMP NOT NULL,
    funding_rate NUMERIC(16, 8) NOT NULL,
    snapshot_time TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE(symbol, funding_time)
);

CREATE TABLE futures_open_interest (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    open_interest NUMERIC(32, 12) NOT NULL,
    snapshot_time TIMESTAMP NOT NULL,
    UNIQUE(symbol, snapshot_time)
);

CREATE TABLE futures_liquidations (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    order_id BIGINT,
    price NUMERIC(32, 12),
    quantity NUMERIC(32, 12),
    side VARCHAR(4),
    time TIMESTAMP NOT NULL,
    snapshot_time TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE options_chain (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(32) NOT NULL,
    underlying VARCHAR(20) NOT NULL,
    strike NUMERIC(32, 12) NOT NULL,
    expiry_date DATE,
    option_type VARCHAR(4) NOT NULL,
    mark_price NUMERIC(32, 12),
    bid_price NUMERIC(32, 12),
    ask_price NUMERIC(32, 12),
    iv NUMERIC(16, 8),
    volume NUMERIC(32, 12),
    open_interest NUMERIC(32, 12),
    snapshot_time TIMESTAMP NOT NULL,
    UNIQUE(symbol, expiry_date, strike, option_type, snapshot_time)
);
```
