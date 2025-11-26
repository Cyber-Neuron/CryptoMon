#!/usr/bin/env node
/* eslint-disable no-console */
import fs     from 'fs/promises';
import axios  from 'axios';
import { load } from 'cheerio';
import { Pool } from 'pg';
import * as url from 'url';
import dotenv from 'dotenv';
import { getProxyConfig } from './proxy-utils.js';
import instMap from './institution_map.json' assert { type: 'json' };

// 加载环境变量
dotenv.config();

// 验证数据库连接字符串
if (!process.env.DATABASE_URL) {
  console.error('Error: DATABASE_URL environment variable is not set');
  process.exit(1);
}

// 配置连接池
const pool = new Pool({ 
  connectionString: process.env.DATABASE_URL,
  connectionTimeoutMillis: 10000,
  idleTimeoutMillis: 30000,
  max: 20,
  min: 4,
});

// 添加连接错误处理
pool.on('error', (err, client) => {
  console.error('Unexpected error on idle client', err);
});

// 添加重试机制的查询函数
async function queryWithRetry(text, params, maxRetries = 3) {
  let lastError;
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await pool.query(text, params);
    } catch (err) {
      lastError = err;
      console.error(`Query attempt ${i + 1} failed:`, err.message);
      if (i < maxRetries - 1) {
        // 等待一段时间后重试，使用指数退避
        await new Promise(resolve => setTimeout(resolve, Math.pow(2, i) * 1000));
      }
    }
  }
  throw lastError;
}

/* -------------------------------------------------- 工具函数 -------------------------------------------------- */

/** 根据浏览器域名推断链名；必要时可扩展更多规则 */
function chainFromUrl(link) {
  const host = url.parse(link).hostname;
  if (!host) return 'Unknown';
  if (host.includes('etherscan'))        return 'Ethereum';
  if (host.includes('bscscan'))          return 'BSC';
  if (host.includes('polygonscan'))      return 'Polygon';
  if (host.includes('arbiscan'))         return 'Arbitrum';
  if (host.includes('snowtrace'))        return 'Avalanche';
  return 'Unknown';
}

/** 抓取 Etherscan 网页并解析地址 & 代币数量 */
async function parseEtherscan(link) {
  try {
    const response = await axios.get(link, getProxyConfig());
    const $ = load(response.data);

    // ① from / to
    const adrSel = $('a.hash-tag[href^="/address/"]');
    const fromAddress = $(adrSel[0]).text().trim();
    const toAddress   = $(adrSel[1]).text().trim();

    // ② token 数量
    const valueText = $('#ContentPlaceHolder1_spanValue').text().trim();
    const [amountStr] = valueText.split(' ');
    const amount = Number(amountStr.replaceAll(',', ''));

    return { fromAddress, toAddress, amount };
  } catch (error) {
    console.error(`Failed to fetch ${link}:`, error.message);
    throw error;
  }
}

/* ---------------------------- DB helper：幂等 UPSERT ---------------------------- */

async function getOrInsertInstitution(name) {
  if (!name) return null;
  const { rows } = await queryWithRetry(
    `INSERT INTO institutions(name)
       VALUES ($1)
       ON CONFLICT (name) DO NOTHING
       RETURNING id`,
    [name]
  );
  return rows.length ? rows[0].id
                     : (await queryWithRetry(
                         'SELECT id FROM institutions WHERE name=$1', [name])).rows[0].id;
}

async function getOrInsertChain(name) {
  const { rows } = await queryWithRetry(
    `INSERT INTO chains(name, native_sym)
     VALUES ($1, $2)
     ON CONFLICT (name) DO UPDATE SET native_sym = EXCLUDED.native_sym
     RETURNING id`,
    [name, name.slice(0,4).toUpperCase()]
  );
  return rows[0].id;
}

async function getOrInsertToken(symbol, chainId) {
  const { rows } = await queryWithRetry(
    `INSERT INTO tokens(symbol, chain_id)
     VALUES ($1, $2)
     ON CONFLICT (symbol, chain_id) DO NOTHING
     RETURNING id`,
    [symbol, chainId]
  );
  return rows.length ? rows[0].id
                     : (await queryWithRetry(
                         'SELECT id FROM tokens WHERE symbol=$1 AND chain_id=$2',
                         [symbol, chainId])).rows[0].id;
}

async function getOrInsertWallet(address, chainId, institutionName = null) {
  let institutionId = null;
  if (institutionName) {
    institutionId = await getOrInsertInstitution(institutionName);
  }

  /* upsert wallets(address,chain) —— 若已存在则仅在缺少机构时补充 */
  const { rows } = await queryWithRetry(
    `INSERT INTO wallets(address, chain_id, institution_id)
       VALUES ($1,$2,$3)
       ON CONFLICT (address, chain_id) DO UPDATE
           SET institution_id = COALESCE(wallets.institution_id, EXCLUDED.institution_id)
       RETURNING id`,
    [address, chainId, institutionId]
  );
  return rows[0].id;
}

async function insertTx(tx) {
  const {
    txHash, chainId, blockHeight = null,
    fromWalletId, toWalletId, tokenId,
    amount, usdValue, ts, rawRemark
  } = tx;

  await queryWithRetry(
    `INSERT INTO transactions
       (tx_hash, chain_id, block_height,
        from_wallet_id, to_wallet_id, token_id,
        amount, usd_value, ts, raw_remark)
     VALUES
       ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10)
     ON CONFLICT (tx_hash, token_id) DO NOTHING`,
    [txHash, chainId, blockHeight,
     fromWalletId, toWalletId, tokenId,
     amount, usdValue, ts, rawRemark]);
}

/* -------------------------------------------------- 主流程 -------------------------------------------------- */

async function main() {
  const raw = await fs.readFile('result.json', 'utf8');
  const days = JSON.parse(raw);

  for (const day of days) {
    for (const item of day.list) {
      const remark = JSON.parse(item.remark);    // 解析 remark 字段
      const webUrl = remark.web;                 // 交易浏览器页面
      const txHash = remark.hash;                // 交易哈希
      const symbol = item.symbol;                // 代币符号
      const ts     = new Date(item.createTime);  // 创建时间

      // 1) 链
      const chainName = chainFromUrl(webUrl);
      const chainId   = await getOrInsertChain(chainName);

      // 2) 代币
      const tokenId   = await getOrInsertToken(symbol, chainId);

      // 3) 抓网页取 from / to / amount
      let parsed = { 
        fromAddress: remark.from === 'unknown' ? '0x0' : remark.from, 
        toAddress: remark.to === 'unknown' ? '0x0' : remark.to, 
        amount: Number(item.price) 
      };
      try {
        if (chainName === 'Ethereum') parsed = await parseEtherscan(webUrl);
        // 其他链可写各自 parseXxx 函数
      } catch (e) {
        console.error(`Parse failed ${webUrl}`, e.message);
      }

      // 4) 钱包
      const fromInst = instMap[parsed.fromAddress.toLowerCase()];
      const toInst   = instMap[parsed.toAddress.toLowerCase()];

      const fromWalletId = await getOrInsertWallet(parsed.fromAddress, chainId, fromInst);
      const toWalletId   = await getOrInsertWallet(parsed.toAddress,   chainId, toInst);

      // 5) 写交易
      await insertTx({
        txHash,
        chainId,
        fromWalletId,
        toWalletId,
        tokenId,
        amount   : parsed.amount,
        usdValue : item.volUsd,
        ts,
        rawRemark: remark
      });

      console.log(`✔  ${txHash.slice(0,10)}… stored`);
    }
  }

  await pool.end();
}

main().catch(e => {
  console.error(e);
  process.exit(1);
});
