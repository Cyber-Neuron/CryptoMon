-- 导入 Wintermute 热钱包数据
-- 创建表结构（如果不存在）
CREATE TABLE IF NOT EXISTS wintermute_wallets (
    id SERIAL PRIMARY KEY,
    address VARCHAR(255) NOT NULL,
    chain_id INTEGER NOT NULL,
    friendly_name VARCHAR(255),
    grp_type VARCHAR(50),
    grp_name VARCHAR(100),
    updated BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 清空现有数据（可选，如果需要重新导入）
-- TRUNCATE TABLE wintermute_wallets;

-- 插入数据
INSERT INTO wallets (address, chain_id, friendly_name, grp_type, grp_name, updated) VALUES
('2cDLqiWcj8xT3SRYUTTVCTwT7rtCoDtVrTX8u5u5aSWT', 1, 'Wintermute Hot Wallet', 'Hot', 'wintermute', FALSE),
('6wLHQkJa4eCW9oXu4KLZZ3VuxpD9HkAXMucskri2EZHP', 1, 'Wintermute Binance Deposit', 'Hot', 'binance', FALSE),
('5JsFdeXAgy11EmWoqLpiKBzmpyhjAN32F6H4o3n4wKRB', 1, 'Wintermute Binance Deposit', 'Hot', 'binance', FALSE),
('9bUURPfwDStZzXtEGxEarAhwL9q3d57SGWpp7PPoa14', 1, 'Wintermute ', 'Hot', 'wintermute', FALSE),
('2r8YuYUpdNgB6pEQrcgXQWF6SyoQayNFwEH4ncTCyHKx', 1, 'Wintermute ', 'Hot', 'wintermute', FALSE),
('8VYWdU14V78rcDepwmNt54bb1aam5qVUMUpEtW8oCn1E', 1, 'Wintermute ', 'Hot', 'wintermute', FALSE),
('0x225a38bc71102999Dd13478BFaBD7c4d53f2DC17', 1, 'Rizzolver (Wintermute) UniswapX', 'Hot', 'wintermute', FALSE),
('0xA8C1C98aAF99A5DfC907d61b892b2aD624901185', 1, 'Rizzolver (Wintermute) 1inch', 'Hot', 'wintermute', FALSE),
('0x51C72848c68a965f66FA7a88855F9f7784502a7F', 1, 'Wintermute Market Maker', 'Hot', 'wintermute', TRUE),
('0x84b38Bc60f3bD82640EceFa320dAB2bE62e2Da15', 1, 'Wintermute Kraken Deposit', 'Hot', 'kraken', TRUE),
('0xf8191D98ae98d2f7aBDFB63A9b0b812b93C873AA', 1, 'Wintermute Hot Wallet', 'Hot', 'wintermute', TRUE),
('0x32d4703e5834F1b474B17DFdB0aC32Cc22575145', 1, 'Wintermute Crypto.com Deposit', 'Hot', 'crypto.com', TRUE),
('0x4594467601ce92B0d94fc5112722131A535Ef0c7', 1, 'Wintermute Coinbase Deposit', 'Hot', 'coinbase', TRUE),
('0xe401A6A38024d8f5aB88f1B08cad476cCaCA45E8', 1, 'Wintermute Bybit Deposit', 'Hot', 'bybit', TRUE),
('0x77F7B398a23eF4CAb31Dd5503fd8446c4480C70b', 1, 'Wintermute Bitfinex Deposit', 'Hot', 'bitfinex', TRUE),
('0xEae7380dD4CeF6fbD1144F49E4D1e6964258A4F4', 1, 'Wintermute Binance Deposit', 'Hot', 'binance', TRUE);

-- 验证导入结果
SELECT COUNT(*) as total_wallets FROM wintermute_wallets;
SELECT grp_name, COUNT(*) as wallet_count FROM wintermute_wallets GROUP BY grp_name ORDER BY wallet_count DESC; 