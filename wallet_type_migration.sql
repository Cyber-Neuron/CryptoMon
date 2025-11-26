-- 创建 wallet_type 表
CREATE TABLE IF NOT EXISTS public.wallet_types (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 插入预定义的 wallet types
INSERT INTO public.wallet_types (name, description) VALUES 
    ('cold', 'Cold storage wallets'),
    ('hot', 'Hot wallets for active trading'),
    ('deposit', 'Deposit wallets'),
    ('internal', 'Internal transfer wallets'),
    ('regular', 'Regular user wallets')
ON CONFLICT (name) DO NOTHING;

-- 为 wallets 表添加 wallet_type 字段
ALTER TABLE public.wallets 
ADD COLUMN IF NOT EXISTS wallet_type_id BIGINT REFERENCES public.wallet_types(id);

-- 创建索引以提高查询性能
CREATE INDEX IF NOT EXISTS idx_wallets_wallet_type ON public.wallets(wallet_type_id);

-- 更新现有钱包的 wallet_type 基于 friendly_name
UPDATE public.wallets 
SET wallet_type_id = (SELECT id FROM public.wallet_types WHERE name = 'cold')
WHERE friendly_name ILIKE '%cold%' AND wallet_type_id IS NULL;

-- 为没有设置 wallet_type 的钱包设置默认值 'regular'
UPDATE public.wallets 
SET wallet_type_id = (SELECT id FROM public.wallet_types WHERE name = 'regular')
WHERE wallet_type_id IS NULL;

-- 添加注释
COMMENT ON TABLE public.wallet_types IS 'Wallet type definitions';
COMMENT ON COLUMN public.wallets.wallet_type_id IS 'Reference to wallet type'; 