-- 1.1 链
CREATE TABLE chains (
    id          BIGSERIAL PRIMARY KEY,
    name        TEXT NOT NULL UNIQUE,           -- Ethereum、BSC、Solana…
    native_sym  TEXT NOT NULL
);

-- 1.2 代币
CREATE TABLE tokens (
    id        BIGSERIAL PRIMARY KEY,
    symbol    TEXT    NOT NULL,
    contract  TEXT,                             -- EVM 合约地址；非 EVM 链可空
    chain_id  BIGINT  NOT NULL,
    decimals  SMALLINT NOT NULL DEFAULT 18,
    UNIQUE(symbol, chain_id)                    -- 同一链上同名代币唯一
);

-- 1.3 钱包地址
CREATE TABLE wallets (
    id            BIGSERIAL PRIMARY KEY,
    address       TEXT   NOT NULL,
    chain_id      BIGINT NOT NULL,
    friendly_name TEXT,
    grp_type      TEXT,
    grp_name      TEXT,
    UNIQUE(address, chain_id)                   -- 地址在本链唯一
);

-- 1.4 交易流水
CREATE TABLE transactions (
    id              BIGSERIAL  PRIMARY KEY,
    tx_hash         TEXT       NOT NULL,
    chain_id        BIGINT     NOT NULL,
    block_height    BIGINT,
    from_wallet_id  BIGINT     NOT NULL,
    to_wallet_id    BIGINT     NOT NULL,
    token_id        BIGINT     NOT NULL,
    amount          NUMERIC(78,0) NOT NULL,     -- 原生单位
    usd_value       NUMERIC(38,10),
    ts              TIMESTAMPTZ NOT NULL,
    raw_remark      JSONB,
    UNIQUE(tx_hash, token_id)                   -- 避免重复写入
);

--------------------------------------------------------------------
-- ★ 常用索引（满足“给定钱包/代币/链 + 时间”组合筛选）
--------------------------------------------------------------------
CREATE INDEX idx_tx_from_wallet   ON transactions(from_wallet_id, ts DESC);
CREATE INDEX idx_tx_to_wallet     ON transactions(to_wallet_id,   ts DESC);

CREATE INDEX idx_tx_from_wallet_token ON transactions(from_wallet_id, token_id, ts DESC);
CREATE INDEX idx_tx_to_wallet_token   ON transactions(to_wallet_id,   token_id, ts DESC);

CREATE INDEX idx_wallet_address_chain ON wallets(address, chain_id);
CREATE INDEX idx_token_symbol_chain   ON tokens(symbol,  chain_id);

-- （可选）分区示例：
-- ALTER TABLE transactions PARTITION BY LIST (chain_id);
-- CREATE TABLE transactions_eth PARTITION OF transactions FOR VALUES IN ( (SELECT id FROM chains WHERE name='Ethereum') );


/* ============================================================
   钱包余额历史记录表
   ============================================================ */
CREATE TABLE wallet_balances (
    id              BIGSERIAL PRIMARY KEY,
    wallet_id       BIGINT NOT NULL,           -- 关联 wallets 表
    token_id        BIGINT NOT NULL,           -- 关联 tokens 表
    chain_id        BIGINT NOT NULL,           -- 关联 chains 表
    amount          NUMERIC(78,0) NOT NULL,    -- 原生单位余额
    usd_value       NUMERIC(38,10),            -- 美元价值
    block_height    BIGINT,                    -- 区块高度
    ts              TIMESTAMPTZ NOT NULL,      -- 时间戳
    raw_remark      JSONB,                     -- 原始数据
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- 约束
    FOREIGN KEY (wallet_id) REFERENCES wallets(id),
    FOREIGN KEY (token_id) REFERENCES tokens(id),
    FOREIGN KEY (chain_id) REFERENCES chains(id),
    
    -- 同一钱包同一代币同一区块只能有一条记录
    UNIQUE(wallet_id, token_id, block_height)
);

/* 高频查询索引 */
CREATE INDEX idx_wallet_balance_wallet_token ON wallet_balances(wallet_id, token_id, ts DESC);
CREATE INDEX idx_wallet_balance_ts ON wallet_balances(ts DESC);
CREATE INDEX idx_wallet_balance_chain ON wallet_balances(chain_id);

/* 可选: 按链和时间分区 */
-- ALTER TABLE wallet_balances
--   PARTITION BY LIST (chain_id);
-- 
-- -- Ethereum 分区
-- CREATE TABLE wallet_balances_eth
--   PARTITION OF wallet_balances
--   FOR VALUES IN ( (SELECT id FROM chains WHERE name='Ethereum') )
--   PARTITION BY RANGE (ts);
-- 
-- CREATE TABLE wallet_balances_eth_2025_06
--   PARTITION OF wallet_balances_eth
--   FOR VALUES FROM ('2025-06-01') TO ('2025-07-01');