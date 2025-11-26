# Wallet Monitor Debug 功能总结

## 概述

我已经为walletmonitor项目添加了全面的debug功能，让您可以观察逐条交易的处理细节。这些功能包括详细的日志记录、可配置的debug选项、以及专门的debug工具。

## 新增的文件

### 1. 配置文件
- **`debug_config.py`** - Debug专用配置类，继承自Config
- **`config.py`** - 已更新，添加了debug相关配置选项

### 2. 主程序文件
- **`debug_main.py`** - Debug版本的主程序，提供最大程度的调试信息
- **`main.py`** - 已更新，支持debug模式

### 3. 核心处理文件
- **`block_processor.py`** - 已更新，添加了详细的交易处理debug信息

### 4. 工具和脚本
- **`start_debug.sh`** - Debug模式启动脚本
- **`test_debug.py`** - Debug功能测试脚本
- **`DEBUG_README.md`** - 详细的使用说明文档

## 主要功能特性

### 1. 可配置的Debug选项

```python
# 在config.py中新增的配置项
DEBUG_MODE: bool = True                    # 启用debug模式
DEBUG_TRANSACTION_DETAILS: bool = True     # 显示交易处理详情
DEBUG_WALLET_INFO: bool = True             # 显示钱包信息提取详情
```

### 2. 环境变量支持

```bash
export DEBUG_MODE=true
export DEBUG_TRANSACTION_DETAILS=true
export DEBUG_WALLET_INFO=true
export LOG_LEVEL=DEBUG
export MIN_ETH=1.0
export POLL_INTERVAL_SEC=30
```

### 3. 详细的日志记录

#### 区块处理日志
```
Fetching recent blocks from last 10 minutes...
Current block number: 18500000
Current timestamp: 1703123456
Target timestamp: 1703122856 (looking back 10 minutes)
  Checking block 18500000 (1/100)
    Block 18500000 timestamp: 1703123456
    Added block 18500000 with 150 transactions
```

#### 交易处理日志
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

#### ERC20转账日志
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

#### 钱包信息提取日志
```
Extracting wallet info for address: 0x1234...
Arkham API response for 0x1234...: {'arkhamEntity': {'name': 'Binance Hot Wallet', 'id': 'BINANCE', 'type': 'exchange'}}
Created wallet info: Binance Hot Wallet (BINANCE) for 0x1234...
```

### 4. 多种启动方式

#### 方式1: 使用Debug启动脚本（推荐）
```bash
./start_debug.sh
```

#### 方式2: 直接运行debug主程序
```bash
python3 debug_main.py
```

#### 方式3: 使用普通主程序但启用debug
```bash
export DEBUG_MODE=true
export DEBUG_TRANSACTION_DETAILS=true
export DEBUG_WALLET_INFO=true
export LOG_LEVEL=DEBUG
python3 main.py
```

### 5. 日志文件管理

- Debug模式会同时输出到控制台和`debug.log`文件
- 每次启动时自动备份旧的日志文件为`debug.log.bak`
- 支持实时查看和持久保存

### 6. 性能优化选项

```bash
# 降低日志详细程度
export DEBUG_WALLET_INFO=false
export LOG_LEVEL=INFO

# 调整监控参数
export MIN_ETH=10.0
export POLL_INTERVAL_SEC=60
```

## 调试信息覆盖范围

### 1. 启动阶段
- 配置信息显示
- 组件初始化状态
- 连接测试结果

### 2. 监控地址获取
- 数据库查询详情
- 地址过滤过程
- 钱包信息显示

### 3. 区块处理
- 区块获取过程
- 时间范围计算
- 交易数量统计

### 4. 交易处理
- 每笔交易的详细分析
- ETH转账识别和处理
- ERC20转账解析
- 金额转换和阈值检查
- 钱包信息提取

### 5. 数据存储
- 数据库操作详情
- 交易和流数据统计
- 存储结果确认

### 6. 错误处理
- 异常详细信息
- 堆栈跟踪
- 错误恢复过程

## 使用建议

### 开发/测试环境
- 使用debug模式进行开发和测试
- 设置较低的`MIN_ETH`阈值以看到更多交易
- 使用较短的轮询间隔获得快速反馈

### 生产环境
- 使用INFO级别的日志
- 关闭debug选项以提高性能
- 定期检查日志文件大小

### 性能调优
- 根据实际需求调整debug选项
- 监控内存和CPU使用情况
- 定期清理日志文件

## 测试验证

运行测试脚本验证debug功能：
```bash
python3 test_debug.py
```

测试内容包括：
- 配置加载测试
- 日志功能测试
- 环境变量测试
- 钱包信息提取测试

## 总结

通过这些debug功能，您现在可以：

1. **观察逐条交易处理** - 每笔交易都有详细的处理日志
2. **监控钱包信息提取** - 了解Arkham API的调用和响应
3. **跟踪区块处理过程** - 查看区块获取和解析的详细过程
4. **分析性能瓶颈** - 通过详细日志识别性能问题
5. **调试配置问题** - 验证配置是否正确加载
6. **排查错误原因** - 获得完整的错误信息和堆栈跟踪

这些功能将帮助您深入了解walletmonitor的工作机制，并能够快速定位和解决问题。 