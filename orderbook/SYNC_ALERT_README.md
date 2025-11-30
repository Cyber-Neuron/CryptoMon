# 🎯 Synchronized Large Order Statistics and Voice Alert Feature

## 📋 Feature Overview

Based on the original synchronized large order detection, the following features have been added:

1. **Operation Type Statistics** - Statistics on the distribution of long, short, close long, and close short operations in synchronized large orders
2. **Dominant Operation Identification** - Automatically identifies the dominant operation type
3. **Price Statistical Analysis** - Calculates average transaction prices for spot and futures, and price differences
4. **Smart Voice Alerts** - Issues corresponding voice alerts based on main operation type and price information
5. **Detailed Statistics Reports** - Provides complete operation distribution and price statistics

## 🔧 Features

### 📊 Statistics Function
- Real-time statistics on operation type distribution in synchronized large orders
- Calculates percentage of each operation type
- Identifies dominant operation type
- Supported operation types: Long, Short, Close Long, Close Short, Unknown

### 💰 Price Analysis
- Calculates average transaction prices for spot and futures
- Analyzes price differences between spot and futures
- Statistics on total trading volume
- Identifies premium/discount situations

### 🎤 Voice Alerts
- Issues specialized voice alerts based on main operation type
- Broadcasts average transaction price information
- Broadcasts price difference information when significant
- Supports personalized alerts for different operation types
- Provides detailed statistics when large synchronized orders detected
- Uses Google TTS for high-quality Chinese voice

## 🚀 Usage

### 1. Automatic Operation
Feature is integrated into `bin_mon.py`, start monitoring program to automatically use:

```bash
cd orderbook
python bin_mon.py
```

### 2. Test Functionality
Run test script to verify functionality:

```bash
cd orderbook
python test_sync_alert.py
```

## 📖 Feature Details

### Operation Type Determination Logic

The system determines futures trading operation types through the following logic:

```python
def determine_position_action_improved(is_buyer_maker, ts):
    # Based on Open Interest changes and active party determination
    if is_buyer_maker and delta_oi > 0:  # Active sell + OI increase
        return "开空"
    elif not is_buyer_maker and delta_oi > 0:  # Active buy + OI increase
        return "开多"
    elif delta_oi < 0:  # OI decrease
        if is_buyer_maker:
            return "平多"
        else:
            return "平空"
    else:
        return "未知"
```

### Price Statistics Logic

When synchronized large orders are detected, the system will:

1. **Collect Price Data**
   ```python
   spot_prices = []      # Spot price list
   futures_prices = []   # Futures price list
   total_spot_qty = 0    # Spot total volume
   total_futures_qty = 0 # Futures total volume
   ```

2. **Calculate Statistics**
   ```python
   avg_spot_price = sum(spot_prices) / len(spot_prices)
   avg_futures_price = sum(futures_prices) / len(futures_prices)
   price_diff = avg_futures_price - avg_spot_price
   price_diff_percent = (price_diff / avg_spot_price * 100)
   ```

3. **Broadcast Price Information**
   ```python
   price_alert_text = f"现货均价{avg_spot_price:.0f}，合约均价{avg_futures_price:.0f}"
   if abs(price_diff_percent) > 0.5:  # Broadcast when difference exceeds 0.5%
       if price_diff > 0:
           price_alert_text += f"，合约溢价{price_diff_percent:.1f}%"
       else:
           price_alert_text += f"，现货溢价{abs(price_diff_percent):.1f}%"
   ```

### Statistics and Alert Logic

When synchronized large orders are detected, the system will:

1. **Statistics on Operation Distribution**
   ```python
   sync_operations = {
       "开多": 0,
       "开空": 0,
       "平多": 0,
       "平空": 0,
       "未知": 0
   }
   ```

2. **Identify Dominant Operation**
   ```python
   dominant_operation = max(sync_operations.items(), key=lambda x: x[1])
   operation_name, operation_count = dominant_operation
   percentage = (operation_count / total_matches) * 100
   ```

3. **Issue Voice Alerts**
   ```python
   if operation_name == "开多":
       warning_alert.trading_alert("开多", f"{total_matches}笔同步", "ETH")
   elif operation_name == "开空":
       warning_alert.trading_alert("开空", f"{total_matches}笔同步", "ETH")
   # ... other operation types
   ```

## 📊 Output Examples

### Console Output
```
=== [Detected Suspected Synchronized Large Orders] ===
[Spot] 14:30:25.123 qty=15.50 price=2450.50 Buy Order
[Futures] 14:30:25.456 qty=20.00 price=2450.75 Long
Time Interval: 0.333 seconds

📊 Synchronized Large Order Statistics: Total 3 orders, Long 2, Short 1
🎯 Main Operation: Long (66.7%)
💰 Price Statistics:
   Spot Average Price: $2450.85
   Futures Average Price: $2451.20
   Price Difference: $+0.35 (+0.014%)
   Spot Total Volume: 45.20 ETH
   Futures Total Volume: 58.40 ETH
```

### Voice Alerts
- **Operation Alert**: "发现大额开多，ETH，金额3笔同步"
- **Price Alert**: "现货均价2451，合约均价2451"
- **Price Difference Alert**: "现货均价2451，合约均价2451，合约溢价0.1%"
- **Detailed Statistics**: "同步大单详情: 开多占67%，共3笔"

## 🎯 Application Scenarios

### 1. Trend Judgment
- **Long Dominant**: May indicate upward trend
- **Short Dominant**: May indicate downward trend
- **Close Long Dominant**: May indicate profit taking
- **Close Short Dominant**: May indicate short covering

### 2. Price Analysis
- **Futures Premium**: May indicate bullish sentiment
- **Spot Premium**: May indicate bearish sentiment
- **Price Difference Widening**: May indicate increased market volatility
- **Price Difference Narrowing**: May indicate market stabilization

### 3. Risk Monitoring
- Large synchronized orders may indicate market anomalies
- Concentration of specific operation types may indicate manipulation
- Very short time intervals may indicate algorithmic trading
- Abnormal price differences may indicate arbitrage opportunities or risks

### 4. Trading Decisions
- Adjust trading strategies based on dominant operation types
- Make arbitrage decisions based on price difference information
- Set corresponding risk control measures
- Optimize trading timing and prices

## ⚙️ Configuration Parameters

### Main Parameters
```python
SPOT_THRESHOLD = 5      # Spot large order threshold
FUTURES_THRESHOLD = 20  # Futures large order threshold
MATCH_INTERVAL = 4      # Matching time window (seconds)
OI_WINDOW = 4          # OI comparison window (seconds)
```

### Alert Thresholds
- **Basic Alert**: Detects any synchronized large orders
- **Detailed Statistics**: Synchronized large orders ≥ 3
- **Price Difference Alert**: Price difference absolute value > 0.5%
- **High Frequency Alert**: Can adjust alert frequency as needed

## 🔍 Troubleshooting

### 1. Voice Alerts Not Working
- Check network connection (Google TTS requires network)
- Confirm audio device working normally
- Check volume settings

### 2. Statistics Inaccurate
- Check if OI data is updating normally
- Confirm time window settings are reasonable
- Verify operation type determination logic
- Check price data completeness

### 3. Alerts Too Frequent
- Adjust large order threshold
- Increase matching time window
- Set alert cooldown time
- Adjust price difference alert threshold

## 📈 Performance Optimization

### 1. Memory Optimization
- Use deque to limit queue length
- Regularly clean expired data
- Optimize data structures

### 2. CPU Optimization
- Reduce unnecessary calculations
- Optimize matching algorithms
- Use caching to reduce repeated calculations

### 3. Network Optimization
- Batch process API requests
- Use connection pools
- Implement retry mechanisms

## 🔮 Future Extensions

### 1. Machine Learning Integration
- Use ML models to predict operation types
- Automatically identify abnormal patterns
- Smart alert threshold adjustment
- Price trend prediction

### 2. Multi-Market Support
- Extend to other trading pairs
- Support multiple exchanges
- Cross-market analysis
- Arbitrage opportunity identification

### 3. Advanced Analysis
- Historical data backtesting
- Pattern recognition
- Risk assessment
- Price correlation analysis

Now your synchronized large order monitoring system has intelligent statistics, price analysis, and voice alert features, allowing you to better analyze market dynamics and respond promptly!
