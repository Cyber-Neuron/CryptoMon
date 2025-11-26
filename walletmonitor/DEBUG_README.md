# Wallet Monitor Debug Mode

这个文档说明如何使用walletmonitor的debug模式来观察逐条交易的处理细节。

## 概述

Debug模式提供了详细的日志信息，让您可以观察：
- 每个区块的处理过程
- 每笔交易的详细分析
- ETH和ERC20代币转账的识别
- 钱包信息的提取过程
- 数据库存储操作

## 快速开始

### 方法1: 使用Debug启动脚本（推荐）

```bash
# 进入walletmonitor目录
cd walletmonitor

# 运行debug启动脚本
./start_debug.sh
```

### 方法2: 直接运行debug主程序

```bash
# 设置环境变量
export DEBUG_MODE=true
export DEBUG_TRANSACTION_DETAILS=true
export DEBUG_WALLET_INFO=true
export LOG_LEVEL=DEBUG
export MIN_ETH=1.0
export POLL_INTERVAL_SEC=30

# 运行debug程序
python3 debug_main.py
```

### 方法3: 使用普通主程序但启用debug

```bash
# 设置debug环境变量
export DEBUG_MODE=true
export DEBUG_TRANSACTION_DETAILS=true
export DEBUG_WALLET_INFO=true
export LOG_LEVEL=DEBUG

# 运行普通主程序
python3 main.py
```

## Debug配置选项

### 环境变量

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `DEBUG_MODE` | `true` | 启用debug模式 |
| `DEBUG_TRANSACTION_DETAILS` | `true` | 显示交易处理详情 |
| `DEBUG_WALLET_INFO` | `true` | 显示钱包信息提取详情 |
| `LOG_LEVEL` | `DEBUG` | 日志级别 |
| `MIN_ETH` | `1.0` | 最小ETH阈值（降低以看到更多交易） |
| `POLL_INTERVAL_SEC` | `30` | 轮询间隔（秒） |

### 配置文件

- `debug_config.py` - Debug专用配置
- `config.py` - 标准配置（已添加debug选项）

## Debug日志详解

### 1. 启动信息

```
====================================================================================================
DEBUG WALLET MONITOR STARTING
====================================================================================================
Logging level: DEBUG
Debug mode: True
Debug transaction details: True
Debug wallet info: True
Minimum ETH threshold: 1.0
Poll interval: 30 seconds
====================================================================================================
```

### 2. 监控地址获取

```
============================================================
FETCHING WATCH ADDRESSES
============================================================
Retrieved 10 total wallets from database
WATCH ADDRESSES:
  0x1234... -> Binance Hot Wallet (BINANCE)
  0x5678... -> Coinbase Hot Wallet (COINBASE)
============================================================
```

### 3. 区块处理

```
Fetching recent blocks from last 10 minutes...
Current block number: 18500000
Current timestamp: 1703123456
Target timestamp: 1703122856 (looking back 10 minutes)
  Checking block 18500000 (1/100)
    Block 18500000 timestamp: 1703123456
    Added block 18500000 with 150 transactions
```

### 4. 交易处理详情

#### ETH转账

```
Processing ETH transfer: 0xabcd...
  From: 0x1234...
  To: 0x5678...
  Value: 1000000000000000000 wei
  ETH amount: 1.0 ETH
  Minimum required: 1.0 ETH
  Processing from address: 0x1234...
  Processing to address: 0x5678...
  From address not in watch list, extracting info...
  To address not in watch list, extracting info...
  Created ETH transaction: 0xabcd...
    From: Binance Hot Wallet (0x1234...)
    To: Unknown Wallet (0x5678...)
    Amount: 1.0 ETH ($2500.00)
```

#### ERC20转账

```
Processing ERC20 transfers for tx: 0xefgh...
  Number of logs: 3
  Processing log 1/3
    Contract: 0xdAC17F958D2ee523a2206206994597C13D831ec7
    Topic0: 0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef
    Found USDT transfer
    From: 0x1234...
    To: 0x5678...
    Raw amount: 1000000
    Converted amount: 1.0 USDT
    Minimum required: 2500.0 USD
    Skipping: Amount below minimum threshold
```

### 5. 钱包信息提取

```
Extracting wallet info for address: 0x1234...
Arkham API response for 0x1234...: {'arkhamEntity': {'name': 'Binance Hot Wallet', 'id': 'BINANCE', 'type': 'exchange'}}
Created wallet info: Binance Hot Wallet (BINANCE) for 0x1234...
```

### 6. 处理总结

```
Processing 5 blocks with 10 watch addresses
ETH price: $2500.00
Minimum ETH threshold: 1.0 ETH
Processing block 18500000 (1/5) with 150 transactions
  Block timestamp: 1703123456
  Block hash: 18500000
    Processing transaction 1/150: 0xabcd...
    Found 1 relevant transactions
  Block 18500000 summary: 1 relevant transactions

Creating exchange flows from transactions...
  Creating flow 1/3 for tx: 0xabcd...
    Created flow: Binance Hot Wallet -> Unknown Wallet

Transaction summary:
  0xabcd...: Binance Hot Wallet -> Unknown Wallet (1.0 ETH)
  0xefgh...: Coinbase Hot Wallet -> Binance Hot Wallet (5000.0 USDT)
```

## 日志文件

Debug模式会同时输出到：
- 控制台（实时查看）
- `debug.log` 文件（持久保存）

每次启动时会自动备份旧的 `debug.log` 为 `debug.log.bak`。

## 性能调优

### 降低日志详细程度

如果日志太多影响性能，可以调整：

```bash
# 只显示交易详情，不显示钱包信息
export DEBUG_WALLET_INFO=false

# 只显示基本信息
export LOG_LEVEL=INFO
export DEBUG_MODE=false
```

### 调整监控参数

```bash
# 提高最小阈值，减少处理的交易数量
export MIN_ETH=10.0

# 增加轮询间隔，减少处理频率
export POLL_INTERVAL_SEC=60
```

## 故障排除

### 常见问题

1. **日志文件过大**
   - 定期清理 `debug.log` 文件
   - 调整日志级别为 INFO

2. **处理速度慢**
   - 提高 `MIN_ETH` 阈值
   - 减少 `DEBUG_WALLET_INFO` 输出
   - 增加 `POLL_INTERVAL_SEC`

3. **内存使用过高**
   - 减少处理的区块数量
   - 关闭不必要的debug选项

### 监控建议

- 在开发/测试环境使用debug模式
- 生产环境建议使用INFO级别
- 定期检查日志文件大小
- 根据实际需求调整debug选项

## 示例输出

完整的debug输出示例请查看 `debug.log` 文件，其中包含：
- 每个处理步骤的详细信息
- 交易数据的完整解析
- 钱包信息的提取过程
- 数据库操作的详情
- 错误和异常的完整堆栈跟踪 