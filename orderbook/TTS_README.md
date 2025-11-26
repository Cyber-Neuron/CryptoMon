# 🎤 Google TTS 语音提醒系统

## 📋 功能特点

- ✅ **高质量语音** - 使用Google TTS，声音自然清晰
- ✅ **中文支持** - 完美支持中文语音合成
- ✅ **跨平台** - 支持Windows、macOS、Linux
- ✅ **易于集成** - 简单的API，易于集成到现有系统
- ✅ **错误处理** - 完善的错误处理和回退机制

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install gTTS
```

### 2. 基本使用

```python
from alert import TradingAlert

# 创建提醒系统
alert = TradingAlert()

# 发出交易提醒
alert.trading_alert("开空", "100万", "BTC")
alert.trading_alert("开多", "50万", "ETH")
alert.price_alert("BTC", "45000", "上涨")

# 自定义提醒
alert.custom_alert("系统检测到异常交易")
```

## 📖 API 文档

### TradingAlert 类

#### 初始化参数

```python
TradingAlert(lang='zh-cn', slow=False)
```

- `lang` (str): 语言代码，默认中文 `'zh-cn'`
- `slow` (bool): 是否慢速播放，默认 `False`

#### 主要方法

##### 1. trading_alert()

```python
trading_alert(action, amount, symbol="BTC", wait_time=2)
```

交易提醒方法

- `action` (str): 交易动作（"开空"、"开多"、"平仓"等）
- `amount` (str): 交易金额
- `symbol` (str): 交易对符号，默认"BTC"
- `wait_time` (int): 等待播放完成的时间（秒）

##### 2. price_alert()

```python
price_alert(symbol, price, direction, wait_time=2)
```

价格提醒方法

- `symbol` (str): 交易对符号
- `price` (str): 价格
- `direction` (str): 价格方向（"上涨"、"下跌"等）
- `wait_time` (int): 等待时间

##### 3. custom_alert()

```python
custom_alert(message, wait_time=2)
```

自定义提醒方法

- `message` (str): 自定义消息
- `wait_time` (int): 等待时间

## 🎯 使用示例

### 示例1：基本交易监控

```python
from alert import TradingAlert
import time

alert = TradingAlert()

# 监控大额交易
def monitor_large_trades():
    # 检测到开空
    alert.trading_alert("开空", "500万", "BTC")
    time.sleep(2)
    
    # 检测到开多
    alert.trading_alert("开多", "300万", "ETH")
    time.sleep(2)
    
    # 价格突破
    alert.price_alert("BTC", "45000", "突破")

monitor_large_trades()
```

### 示例2：集成到现有监控系统

```python
from alert import TradingAlert

class YourTradingMonitor:
    def __init__(self):
        self.alert = TradingAlert()
    
    def on_large_trade_detected(self, trade_data):
        """检测到大额交易时的回调"""
        action = trade_data['action']
        amount = trade_data['amount']
        symbol = trade_data['symbol']
        
        # 发出语音提醒
        self.alert.trading_alert(action, amount, symbol)
    
    def on_price_alert(self, price_data):
        """价格提醒回调"""
        symbol = price_data['symbol']
        price = price_data['price']
        direction = price_data['direction']
        
        self.alert.price_alert(symbol, price, direction)
```

### 示例3：自定义提醒场景

```python
from alert import TradingAlert

alert = TradingAlert()

# 系统启动提醒
alert.custom_alert("交易监控系统已启动")

# 风险警告
alert.custom_alert("检测到异常交易模式，请注意风险")

# 系统状态
alert.custom_alert("系统运行正常，监控中")
```

## 🔧 配置选项

### 语言设置

```python
# 中文（默认）
alert = TradingAlert(lang='zh-cn')

# 英文
alert = TradingAlert(lang='en')

# 日文
alert = TradingAlert(lang='ja')
```

### 语速设置

```python
# 正常语速
alert = TradingAlert(slow=False)

# 慢速（更清晰）
alert = TradingAlert(slow=True)
```

## 🛠️ 故障排除

### 1. 网络连接问题

如果无法连接到Google TTS服务：

```python
# 系统会自动回退到默认叮声
alert.custom_alert("测试消息")
# 如果TTS失败，会播放系统默认的叮声
```

### 2. 音频播放问题

确保系统有音频输出设备，并且音量已开启。

### 3. 权限问题

在某些系统上可能需要音频播放权限。

## 📝 注意事项

1. **网络依赖** - Google TTS需要网络连接
2. **延迟** - 首次播放可能有短暂延迟（生成音频文件）
3. **临时文件** - 系统会自动创建和删除临时音频文件
4. **并发** - 不建议同时播放多个音频，可能会重叠

## 🎵 支持的语音效果

- ✅ 中文语音（男声/女声）
- ✅ 英文语音
- ✅ 日文语音
- ✅ 其他Google TTS支持的语言

## 🔄 与现有系统集成

```python
# 在你的交易监控代码中添加
from alert import TradingAlert

# 初始化
alert_system = TradingAlert()

# 在检测到重要事件时调用
if large_trade_detected:
    alert_system.trading_alert("开空", amount, symbol)

if price_breakout:
    alert_system.price_alert(symbol, price, "突破")

if system_error:
    alert_system.custom_alert("系统出现错误")
```

现在你有了一个高质量的语音提醒系统，可以完美地集成到你的交易监控程序中！ 