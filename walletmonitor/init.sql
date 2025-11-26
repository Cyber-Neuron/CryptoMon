-- Database initialization script for wallet monitoring system

-- Create database if not exists (this will be done by Docker)
-- CREATE DATABASE walletmonitor;

-- Connect to the database
\c walletmonitor;

-- Chains table
CREATE TABLE IF NOT EXISTS chains (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    native_sym VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tokens table
CREATE TABLE IF NOT EXISTS tokens (
    id BIGSERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    chain_id BIGINT REFERENCES chains(id),
    decimals INTEGER DEFAULT 18,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(symbol, chain_id)
);

-- Wallets table
CREATE TABLE IF NOT EXISTS wallets (
    id BIGSERIAL PRIMARY KEY,
    address VARCHAR(42) NOT NULL,
    chain_id BIGINT REFERENCES chains(id),
    friendly_name VARCHAR(255),
    grp_type VARCHAR(50),
    grp_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(address, chain_id)
);

-- Transactions table
CREATE TABLE IF NOT EXISTS transactions (
    id BIGSERIAL PRIMARY KEY,
    hash VARCHAR(66) UNIQUE NOT NULL,
    block_number BIGINT NOT NULL,
    from_wallet_id BIGINT REFERENCES wallets(id),
    to_wallet_id BIGINT REFERENCES wallets(id),
    token_id BIGINT REFERENCES tokens(id),
    amount NUMERIC(30, 18) NOT NULL,
    timestamp BIGINT NOT NULL,
    chain_id BIGINT REFERENCES chains(id),
    usd_value NUMERIC(30, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE transactions
ADD COLUMN from_balance NUMERIC(30, 18),
ADD COLUMN to_balance   NUMERIC(30, 18);

-- Indexes for better performance
CREATE INDEX IF NOT EXISTS idx_wallets_address ON wallets(address);
CREATE INDEX IF NOT EXISTS idx_wallets_grp_name ON wallets(grp_name);
CREATE INDEX IF NOT EXISTS idx_wallets_grp_type ON wallets(grp_type);
CREATE INDEX IF NOT EXISTS idx_transactions_hash ON transactions(hash);
CREATE INDEX IF NOT EXISTS idx_transactions_block_number ON transactions(block_number);
CREATE INDEX IF NOT EXISTS idx_transactions_timestamp ON transactions(timestamp);
CREATE INDEX IF NOT EXISTS idx_transactions_from_wallet ON transactions(from_wallet_id);
CREATE INDEX IF NOT EXISTS idx_transactions_to_wallet ON transactions(to_wallet_id);

-- Insert default chain
INSERT INTO chains (name, native_sym) VALUES ('ethereum', 'ETH') 
ON CONFLICT (name) DO NOTHING;

-- Insert default tokens
INSERT INTO tokens (symbol, chain_id, decimals) VALUES 
    ('ETH', (SELECT id FROM chains WHERE name = 'ethereum'), 18),
    ('USDT', (SELECT id FROM chains WHERE name = 'ethereum'), 6),
    ('USDC', (SELECT id FROM chains WHERE name = 'ethereum'), 6),
    ('WETH', (SELECT id FROM chains WHERE name = 'ethereum'), 18),
    ('DAI', (SELECT id FROM chains WHERE name = 'ethereum'), 18)
ON CONFLICT (symbol, chain_id) DO NOTHING;

-- Insert some sample hot wallets for testing
INSERT INTO wallets (address, chain_id, friendly_name, grp_type, grp_name) VALUES 
    ('0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6', (SELECT id FROM chains WHERE name = 'ethereum'), 'Binance Hot Wallet 1', 'Hot', 'binance'),
    ('0xB38e8c17e38363aF6EbdCb3dAE12e0243582891D', (SELECT id FROM chains WHERE name = 'ethereum'), 'Binance Hot Wallet 2', 'Hot', 'binance'),
    ('0xA090e606E30bD747d4E6245a1517EbE430F0057e', (SELECT id FROM chains WHERE name = 'ethereum'), 'Coinbase Hot Wallet', 'Hot', 'coinbase'),
    ('0x28C6c06298d514Db089934071355E5743bf21d60', (SELECT id FROM chains WHERE name = 'ethereum'), 'Binance Hot Wallet 3', 'Hot', 'binance')
ON CONFLICT (address, chain_id) DO NOTHING;

-- Create a function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger for wallets table
CREATE TRIGGER update_wallets_updated_at BEFORE UPDATE ON wallets
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO walletmonitor;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO walletmonitor; 