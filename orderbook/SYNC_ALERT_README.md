# 🎯 同步大单统计和语音告警功能

## 📋 功能概述

在原有的同步大单检测基础上，新增了以下功能：

1. **操作类型统计** - 统计同步大单中开多、开空、平多、平空的操作分布
2. **优势操作识别** - 自动识别占优势的操作类型
3. **价格统计分析** - 计算现货和合约的平均成交价格及价差
4. **智能语音告警** - 根据主要操作类型和价格信息发出相应的语音提醒
5. **详细统计报告** - 提供完整的操作分布和价格统计信息

## 🔧 功能特点

### 📊 统计功能
- 实时统计同步大单中的操作类型分布
- 计算各操作类型的占比
- 识别占优势的操作类型
- 支持的操作类型：开多、开空、平多、平空、未知

### 💰 价格分析
- 计算现货和合约的平均成交价格
- 分析现货与合约之间的价差
- 统计交易总量
- 识别溢价/折价情况

### 🎤 语音告警
- 根据主要操作类型发出专门的语音提醒
- 播报平均成交价格信息
- 当价差显著时播报价差信息
- 支持不同操作类型的个性化告警
- 大量同步大单时提供详细统计信息
- 使用Google TTS提供高质量中文语音

## 🚀 使用方法

### 1. 自动运行
功能已集成到 `bin_mon.py` 中，启动监控程序即可自动使用：

```bash
cd orderbook
python bin_mon.py
```

### 2. 测试功能
运行测试脚本验证功能：

```bash
cd orderbook
python test_sync_alert.py
```

## 📖 功能详解

### 操作类型判断逻辑

系统通过以下逻辑判断合约交易的操作类型：

```python
def determine_position_action_improved(is_buyer_maker, ts):
    # 基于Open Interest变化和主动方判断
    if is_buyer_maker and delta_oi > 0:  # 主动卖出 + OI增加
        return "开空"
    elif not is_buyer_maker and delta_oi > 0:  # 主动买入 + OI增加
        return "开多"
    elif delta_oi < 0:  # OI减少
        if is_buyer_maker:
            return "平多"
        else:
            return "平空"
    else:
        return "未知"
```

### 价格统计逻辑

当检测到同步大单时，系统会：

1. **收集价格数据**
   ```python
   spot_prices = []      # 现货价格列表
   futures_prices = []   # 合约价格列表
   total_spot_qty = 0    # 现货总量
   total_futures_qty = 0 # 合约总量
   ```

2. **计算统计指标**
   ```python
   avg_spot_price = sum(spot_prices) / len(spot_prices)
   avg_futures_price = sum(futures_prices) / len(futures_prices)
   price_diff = avg_futures_price - avg_spot_price
   price_diff_percent = (price_diff / avg_spot_price * 100)
   ```

3. **播报价格信息**
   ```python
   price_alert_text = f"现货均价{avg_spot_price:.0f}，合约均价{avg_futures_price:.0f}"
   if abs(price_diff_percent) > 0.5:  # 价差超过0.5%时播报
       if price_diff > 0:
           price_alert_text += f"，合约溢价{price_diff_percent:.1f}%"
       else:
           price_alert_text += f"，现货溢价{abs(price_diff_percent):.1f}%"
   ```

### 统计和告警逻辑

当检测到同步大单时，系统会：

1. **统计操作分布**
   ```python
   sync_operations = {
       "开多": 0,
       "开空": 0,
       "平多": 0,
       "平空": 0,
       "未知": 0
   }
   ```

2. **识别优势操作**
   ```python
   dominant_operation = max(sync_operations.items(), key=lambda x: x[1])
   operation_name, operation_count = dominant_operation
   percentage = (operation_count / total_matches) * 100
   ```

3. **发出语音告警**
   ```python
   if operation_name == "开多":
       warning_alert.trading_alert("开多", f"{total_matches}笔同步", "ETH")
   elif operation_name == "开空":
       warning_alert.trading_alert("开空", f"{total_matches}笔同步", "ETH")
   # ... 其他操作类型
   ```

## 📊 输出示例

### 控制台输出
```
=== [检测到疑似同步大单] ===
[现货] 14:30:25.123 qty=15.50 price=2450.50 买单
[合约] 14:30:25.456 qty=20.00 price=2450.75 开多
时间间隔: 0.333秒

📊 同步大单统计: 总计3笔, 开多2笔, 开空1笔
🎯 主要操作: 开多 (66.7%)
💰 价格统计:
   现货平均价格: $2450.85
   合约平均价格: $2451.20
   价差: $+0.35 (+0.014%)
   现货总量: 45.20 ETH
   合约总量: 58.40 ETH
```

### 语音告警
- **操作告警**: "发现大额开多，ETH，金额3笔同步"
- **价格告警**: "现货均价2451，合约均价2451"
- **价差告警**: "现货均价2451，合约均价2451，合约溢价0.1%"
- **详细统计**: "同步大单详情: 开多占67%，共3笔"

## 🎯 应用场景

### 1. 趋势判断
- **开多占优势**: 可能预示上涨趋势
- **开空占优势**: 可能预示下跌趋势
- **平多占优势**: 可能预示获利了结
- **平空占优势**: 可能预示空头回补

### 2. 价格分析
- **合约溢价**: 可能预示看涨情绪
- **现货溢价**: 可能预示看跌情绪
- **价差扩大**: 可能预示市场波动加剧
- **价差收窄**: 可能预示市场趋于稳定

### 3. 风险监控
- 大量同步大单可能预示市场异常
- 特定操作类型集中可能预示操纵行为
- 时间间隔过短可能预示程序化交易
- 价差异常可能预示套利机会或风险

### 4. 交易决策
- 根据优势操作类型调整交易策略
- 结合价差信息进行套利决策
- 设置相应的风险控制措施
- 优化交易时机和价格

## ⚙️ 配置参数

### 主要参数
```python
SPOT_THRESHOLD = 5      # 现货大单阈值
FUTURES_THRESHOLD = 20  # 合约大单阈值
MATCH_INTERVAL = 4      # 匹配时间窗口（秒）
OI_WINDOW = 4          # OI对比窗口（秒）
```

### 告警阈值
- **基础告警**: 检测到任何同步大单
- **详细统计**: 同步大单数量 ≥ 3笔
- **价差告警**: 价差绝对值 > 0.5%
- **高频告警**: 可根据需要调整告警频率

## 🔍 故障排除

### 1. 语音告警不工作
- 检查网络连接（Google TTS需要网络）
- 确认音频设备正常工作
- 检查音量设置

### 2. 统计不准确
- 检查OI数据是否正常更新
- 确认时间窗口设置合理
- 验证操作类型判断逻辑
- 检查价格数据完整性

### 3. 告警过于频繁
- 调整大单阈值
- 增加匹配时间窗口
- 设置告警冷却时间
- 调整价差告警阈值

## 📈 性能优化

### 1. 内存优化
- 使用deque限制队列长度
- 定期清理过期数据
- 优化数据结构

### 2. CPU优化
- 减少不必要的计算
- 优化匹配算法
- 使用缓存减少重复计算

### 3. 网络优化
- 批量处理API请求
- 使用连接池
- 实现重试机制

## 🔮 未来扩展

### 1. 机器学习集成
- 使用ML模型预测操作类型
- 自动识别异常模式
- 智能告警阈值调整
- 价格趋势预测

### 2. 多市场支持
- 扩展到其他交易对
- 支持多交易所
- 跨市场分析
- 套利机会识别

### 3. 高级分析
- 历史数据回测
- 模式识别
- 风险评估
- 价格相关性分析

现在你的同步大单监控系统具备了智能统计、价格分析和语音告警功能，可以更好地分析市场动态并做出及时响应！ 