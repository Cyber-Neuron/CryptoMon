# 🎤 Google TTS Voice Alert System

## 📋 Features

- ✅ **High Quality Voice** - Uses Google TTS, natural and clear voice
- ✅ **Chinese Support** - Perfect support for Chinese voice synthesis
- ✅ **Cross Platform** - Supports Windows, macOS, Linux
- ✅ **Easy Integration** - Simple API, easy to integrate into existing systems
- ✅ **Error Handling** - Comprehensive error handling and fallback mechanism

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install gTTS
```

### 2. Basic Usage

```python
from alert import TradingAlert

# Create alert system
alert = TradingAlert()

# Issue trading alerts
alert.trading_alert("开空", "100万", "BTC")
alert.trading_alert("开多", "50万", "ETH")
alert.price_alert("BTC", "45000", "上涨")

# Custom alerts
alert.custom_alert("系统检测到异常交易")
```

## 📖 API Documentation

### TradingAlert Class

#### Initialization Parameters

```python
TradingAlert(lang='zh-cn', slow=False)
```

- `lang` (str): Language code, default Chinese `'zh-cn'`
- `slow` (bool): Whether to play slowly, default `False`

#### Main Methods

##### 1. trading_alert()

```python
trading_alert(action, amount, symbol="BTC", wait_time=2)
```

Trading alert method

- `action` (str): Trading action ("开空", "开多", "平仓", etc.)
- `amount` (str): Trading amount
- `symbol` (str): Trading pair symbol, default "BTC"
- `wait_time` (int): Wait time for playback completion (seconds)

##### 2. price_alert()

```python
price_alert(symbol, price, direction, wait_time=2)
```

Price alert method

- `symbol` (str): Trading pair symbol
- `price` (str): Price
- `direction` (str): Price direction ("上涨", "下跌", etc.)
- `wait_time` (int): Wait time

##### 3. custom_alert()

```python
custom_alert(message, wait_time=2)
```

Custom alert method

- `message` (str): Custom message
- `wait_time` (int): Wait time

## 🎯 Usage Examples

### Example 1: Basic Trading Monitoring

```python
from alert import TradingAlert
import time

alert = TradingAlert()

# Monitor large trades
def monitor_large_trades():
    # Detected short position
    alert.trading_alert("开空", "500万", "BTC")
    time.sleep(2)
    
    # Detected long position
    alert.trading_alert("开多", "300万", "ETH")
    time.sleep(2)
    
    # Price breakout
    alert.price_alert("BTC", "45000", "突破")

monitor_large_trades()
```

### Example 2: Integrate into Existing Monitoring System

```python
from alert import TradingAlert

class YourTradingMonitor:
    def __init__(self):
        self.alert = TradingAlert()
    
    def on_large_trade_detected(self, trade_data):
        """Callback when large trade detected"""
        action = trade_data['action']
        amount = trade_data['amount']
        symbol = trade_data['symbol']
        
        # Issue voice alert
        self.alert.trading_alert(action, amount, symbol)
    
    def on_price_alert(self, price_data):
        """Price alert callback"""
        symbol = price_data['symbol']
        price = price_data['price']
        direction = price_data['direction']
        
        self.alert.price_alert(symbol, price, direction)
```

### Example 3: Custom Alert Scenarios

```python
from alert import TradingAlert

alert = TradingAlert()

# System startup alert
alert.custom_alert("交易监控系统已启动")

# Risk warning
alert.custom_alert("检测到异常交易模式，请注意风险")

# System status
alert.custom_alert("系统运行正常，监控中")
```

## 🔧 Configuration Options

### Language Settings

```python
# Chinese (default)
alert = TradingAlert(lang='zh-cn')

# English
alert = TradingAlert(lang='en')

# Japanese
alert = TradingAlert(lang='ja')
```

### Speech Rate Settings

```python
# Normal speed
alert = TradingAlert(slow=False)

# Slow speed (clearer)
alert = TradingAlert(slow=True)
```

## 🛠️ Troubleshooting

### 1. Network Connection Issues

If unable to connect to Google TTS service:

```python
# System will automatically fallback to default beep
alert.custom_alert("测试消息")
# If TTS fails, will play system default beep
```

### 2. Audio Playback Issues

Ensure system has audio output device and volume is turned on.

### 3. Permission Issues

Some systems may require audio playback permissions.

## 📝 Notes

1. **Network Dependency** - Google TTS requires network connection
2. **Latency** - First playback may have brief delay (generating audio file)
3. **Temporary Files** - System automatically creates and deletes temporary audio files
4. **Concurrency** - Not recommended to play multiple audio simultaneously, may overlap

## 🎵 Supported Voice Effects

- ✅ Chinese voice (male/female)
- ✅ English voice
- ✅ Japanese voice
- ✅ Other languages supported by Google TTS

## 🔄 Integration with Existing Systems

```python
# Add to your trading monitoring code
from alert import TradingAlert

# Initialize
alert_system = TradingAlert()

# Call when important events detected
if large_trade_detected:
    alert_system.trading_alert("开空", amount, symbol)

if price_breakout:
    alert_system.price_alert(symbol, price, "突破")

if system_error:
    alert_system.custom_alert("系统出现错误")
```

Now you have a high-quality voice alert system that can be perfectly integrated into your trading monitoring program!
