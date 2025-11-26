-- 删除 ex_flows 表及其相关索引
-- 注意：这会永久删除所有 ex_flows 数据

-- 删除索引
DROP INDEX IF EXISTS idx_ex_flows_timestamp;
DROP INDEX IF EXISTS idx_ex_flows_from_grp;
DROP INDEX IF EXISTS idx_ex_flows_to_grp;
DROP INDEX IF EXISTS idx_ex_flows_tx_hash;

-- 删除表
DROP TABLE IF EXISTS ex_flows;

-- 删除序列（如果存在）
DROP SEQUENCE IF EXISTS ex_flows_id_seq;

-- 验证删除
SELECT 'ex_flows table removed successfully' as status; 