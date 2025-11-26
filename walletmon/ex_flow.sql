CREATE TABLE ex_flows (
    id          BIGSERIAL   PRIMARY KEY,
    timestamp   NUMERIC     NOT NULL,
    token_id    BIGINT,
    chain_id    BIGINT,
    from_grp_name    TEXT,
    to_grp_name    TEXT,
    amount      NUMERIC,
    usd_value   NUMERIC,
    tx_hash     TEXT
);