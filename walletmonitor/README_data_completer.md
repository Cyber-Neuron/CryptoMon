# 数据补齐程序使用说明

## 概述

数据补齐程序 (`data_completer.py`) 用于补充数据库中缺失的钱包信息。该程序会查找 `transactions` 表中 `from_wallet_id` 或 `to_wallet_id` 为空的记录，通过 Web3 接口获取交易的详细信息，然后使用 `extract_wallet_info` 方法获取钱包信息并更新数据库。

## 功能特性

- 🔍 **自动检测缺失数据**: 自动查找数据库中缺失钱包信息的交易记录
- 🌐 **Web3 集成**: 通过以太坊节点获取交易详细信息
- 🏷️ **钱包信息提取**: 使用 Arkham API 获取钱包标签和分组信息
- 📊 **批量处理**: 支持批量处理大量交易记录
- 📝 **详细日志**: 提供详细的处理日志和错误信息
- 🔄 **事务安全**: 使用数据库事务确保数据一致性
- 🖥️ **命令行工具**: 提供便捷的命令行界面

## 使用方法

### 1. 命令行工具（推荐）

```bash
# 检查不完整的交易数量
python cli_completer.py --check

# 运行数据补齐（默认批处理大小100）
python cli_completer.py --run

# 运行数据补齐（批处理大小50）
python cli_completer.py --run --batch-size 50

# 测试单个交易
python cli_completer.py --test-tx 0x1234567890abcdef...

# 详细日志
python cli_completer.py --run --verbose

# 调试模式
python cli_completer.py --run --debug

# 试运行模式（不实际更新数据库）
python cli_completer.py --run --dry-run
```

### 2. 直接运行程序

```bash
# 运行数据补齐程序
python data_completer.py
```

### 3. 测试功能

```bash
# 运行测试脚本
python test_data_completer.py
```

### 4. 在代码中使用

```python
from data_completer import DataCompleter
from config import load_config

# 加载配置
config = load_config()

# 创建数据补齐器
completer = DataCompleter(config)

# 运行数据补齐（默认批处理大小为100）
completer.run(batch_size=50)
```

## 命令行工具详细说明

### 参数说明

- `--check`: 检查不完整的交易数量，不进行实际处理
- `--run`: 运行数据补齐程序
- `--test-tx HASH`: 测试处理单个交易
- `--batch-size N`: 设置批处理大小（默认：100）
- `--verbose, -v`: 详细日志输出
- `--debug, -d`: 调试模式（最详细的日志）
- `--dry-run`: 试运行模式（不实际更新数据库）

### 使用场景

1. **首次使用**：
   ```bash
   # 先检查有多少不完整的交易
   python cli_completer.py --check
   
   # 试运行，确认程序正常工作
   python cli_completer.py --run --dry-run --verbose
   
   # 正式运行
   python cli_completer.py --run --batch-size 50
   ```

2. **测试特定交易**：
   ```bash
   # 测试处理单个交易
   python cli_completer.py --test-tx 0x1234567890abcdef... --verbose
   ```

3. **调试问题**：
   ```bash
   # 启用调试模式获取最详细的信息
   python cli_completer.py --run --debug
   ```

## 配置要求

确保以下配置正确设置：

1. **数据库连接**: `DATABASE_URL` 环境变量或配置文件中的数据库连接字符串
2. **以太坊节点**: `PUBLICNODE_URL` 配置项，指向可用的以太坊 RPC 节点
3. **Arkham API**: 可选的 `ARKHAM_API_KEY` 用于获取钱包标签信息

## 程序流程

1. **初始化**: 连接数据库和以太坊节点
2. **查找缺失数据**: 查询数据库中 `from_wallet_id` 或 `to_wallet_id` 为空的交易
3. **获取交易详情**: 通过 Web3 获取每个交易的 `from` 和 `to` 地址
4. **处理钱包地址**: 对每个地址调用 `extract_wallet_info` 获取钱包信息
5. **更新数据库**: 将获取到的钱包ID更新到交易记录中
6. **批量处理**: 按批次处理，提供进度信息

## 输出示例

### 命令行工具输出

```
$ python cli_completer.py --check
Found 150 transactions with missing wallet info

First 5 incomplete transactions:
  1. ID: 123, Hash: 0xabc123...
  2. ID: 124, Hash: 0xdef456...
  3. ID: 125, Hash: 0xghi789...
  4. ID: 126, Hash: 0xjkl012...
  5. ID: 127, Hash: 0xmno345...
  ... and 145 more

$ python cli_completer.py --run --batch-size 50
🚀 开始运行数据补齐程序...
2024-01-15 10:30:00 - data_completer - INFO - DataCompleter initialized successfully
2024-01-15 10:30:01 - data_completer - INFO - Found 150 transactions with missing wallet info
2024-01-15 10:30:01 - data_completer - INFO - Processing batch 1/3
...
2024-01-15 10:35:00 - data_completer - INFO - Data completion process finished:
2024-01-15 10:35:00 - data_completer - INFO -   Successfully processed: 145
2024-01-15 10:35:00 - data_completer - INFO -   Failed: 5
2024-01-15 10:35:00 - data_completer - INFO -   Total: 150
✅ 数据补齐程序运行完成
```

### 测试单个交易输出

```
$ python cli_completer.py --test-tx 0x1234567890abcdef... --verbose
Testing transaction: 0x1234567890abcdef...
✅ Transaction details retrieved:
  From: 0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6
  To: 0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b7
  Block: 12345678
  From wallet ID: 42
  To wallet ID: 43
```

## 错误处理

程序包含完善的错误处理机制：

- **网络错误**: 自动重试和错误日志记录
- **数据库错误**: 事务回滚和详细错误信息
- **API 限制**: 处理 Arkham API 调用限制
- **无效数据**: 跳过无效的交易哈希或地址

## 性能优化

- **批量处理**: 默认批处理大小为100，可根据需要调整
- **缓存机制**: 利用数据库管理器的钱包缓存
- **连接池**: 使用数据库连接池提高性能
- **进度跟踪**: 实时显示处理进度

## 注意事项

1. **API 限制**: 注意 Arkham API 的调用频率限制
2. **网络稳定性**: 确保以太坊节点连接稳定
3. **数据库备份**: 建议在运行前备份数据库
4. **监控资源**: 大量数据处理时注意内存和CPU使用情况
5. **日志文件**: 程序会自动创建 `data_completer.log` 日志文件

## 故障排除

### 常见问题

1. **连接失败**: 检查 `PUBLICNODE_URL` 配置
2. **数据库错误**: 验证 `DATABASE_URL` 和数据库权限
3. **API 错误**: 检查 Arkham API 密钥和网络连接
4. **内存不足**: 减少批处理大小

### 调试模式

启用调试日志以获取更详细的信息：

```bash
python cli_completer.py --run --debug
```

或者：

```python
import logging
logging.getLogger().setLevel(logging.DEBUG)
```

## 扩展功能

可以根据需要扩展以下功能：

- **多链支持**: 支持其他区块链网络
- **自定义过滤器**: 添加交易过滤条件
- **并行处理**: 使用多线程提高处理速度
- **Web 界面**: 添加 Web 管理界面
- **定时任务**: 集成到定时任务系统中 