# Futures Trading Data Analysis Program

This program is used to analyze futures trading data by calling the local Order Book API to get order quantity changes before and after trades.

## Features

- 🔄 Real-time receive Binance futures aggregated trade data
- 📊 Analyze Order Book changes before and after trades
- 🕒 Support event time and trade time analysis
- 🌐 Call local Order Book API to get historical data
- 📈 Visualize order quantity changes
- ⚙️ Configurable analysis parameters

## System Requirements

1. **Local Order Book System**: Must run `localorderbok.py` first
2. **Python Dependencies**: See `requirements.txt`
3. **Network Connection**: Need access to Binance API

## Installation and Running

### 1. Start Local Order Book System

```bash
# Method 1: Use simplified startup script (recommended)
./start_simple.sh

# Method 2: Run directly
python3 localorderbok.py
```

### 2. Start Trading Analysis Program

```bash
# Method 1: Use startup script (recommended)
./start_trade_analyzer.sh

# Method 2: Run directly
python3 future_trade_analyzer.py
```

## Configuration

Edit `trade_analyzer_config.py` to modify configuration:

```python
# API configuration
LOCAL_API_BASE_URL = "http://localhost:8000"  # Local API address
WEBSOCKET_URL = "wss://fstream.binance.com/ws/ETHUSDT@aggTrade"  # WebSocket address
SYMBOL = "ETHUSDT"  # Trading pair

# Trading analysis configuration
MIN_QUANTITY_THRESHOLD = 1.0  # Minimum trade quantity threshold
ANALYSIS_WINDOW_SECONDS = 5   # Analysis time window (seconds)
PRICE_TOLERANCE = 0.1         # Price tolerance (percentage)

# Buffer configuration
BUFFER_SIZE = 100             # Trade buffer size
ANALYSIS_INTERVAL = 1.0       # Analysis interval (seconds)
STATS_INTERVAL = 10           # Statistics print interval (seconds)

# Display configuration
ENABLE_COLORS = True          # Enable color display
SHOW_DETAILED_ANALYSIS = True # Show detailed analysis
SHOW_STATISTICS = True        # Show statistics
```

## Data Format

### Input Data Format (Binance Aggregated Trades)

```json
{
  "e": "aggTrade",      // Event type
  "E": 123456789,       // Event time (milliseconds)
  "s": "ETHUSDT",       // Trading pair
  "a": 5933014,         // Aggregated trade ID
  "p": "0.001",         // Price
  "q": "100",           // Quantity
  "f": 100,             // First trade ID
  "l": 105,             // Last trade ID
  "T": 123456785,       // Trade time (milliseconds)
  "m": true             // Is buyer maker
}
```

### Analysis Result Output

The program will display the following information:

```
============================================================
Trade Analysis Result
============================================================
Trade Information:
  Time: 18:30:15.123 (Event) / 18:30:15.120 (Trade)
  Price: $50000.00
  Quantity: 1.5000 ETHUSDT
  Type: Active Buy

Order Book Changes:
  Before Trade: Price=$50000.00, Order Quantity=10.500000
  After Trade: Price=$50000.00, Order Quantity=9.000000
  Change: -1.500000
  Order Decrease: Orders consumed
============================================================
```

## How It Works

1. **Data Reception**: Receive Binance futures aggregated trade data through WebSocket
2. **Data Filtering**: Filter out trades below threshold
3. **Time Analysis**: Use event time and trade time for analysis
4. **API Calls**: Call local Order Book API to get historical data
5. **Change Calculation**: Calculate order quantity changes before and after trades
6. **Result Display**: Display detailed analysis results

## Analysis Logic

### Trade Type Determination
- `m: true` → Active Sell (buyer is maker)
- `m: false` → Active Buy (seller is maker)

### Order Book Change Analysis
- **Order Increase**: New orders may have entered
- **Order Decrease**: Orders consumed
- **No Significant Change**: Order quantity basically unchanged

### Time Window Analysis
- Get Order Book data 1 second before trade
- Get Order Book data 1 second after trade
- Calculate order quantity difference

## Statistics

The program will periodically display statistics:

```
Statistics:
  Total Trades: 1250
  Analyzed Trades: 45
  API Calls: 90
  Errors: 2
  Buffer Size: 0
========================================
```

## Troubleshooting

### Common Issues

1. **Local API Connection Failed**
   ```
   Error: Local API connection failed, please ensure localorderbok.py is running
   ```
   **Solution**: Start local Order Book system first

2. **WebSocket Connection Disconnected**
   ```
   Warning: WebSocket connection disconnected, attempting to reconnect...
   ```
   **Solution**: Program will automatically reconnect, no manual intervention needed

3. **API Call Timeout**
   ```
   Warning: API call failed: 408
   ```
   **Solution**: Check if local API system is running normally

4. **Data Parsing Error**
   ```
   Error: JSON parsing failed
   ```
   **Solution**: Check network connection and Binance API status

### Performance Optimization

1. **Reduce API Call Frequency**
   - Increase `ANALYSIS_INTERVAL` value
   - Increase `MIN_QUANTITY_THRESHOLD` value

2. **Reduce Memory Usage**
   - Decrease `BUFFER_SIZE` value
   - Turn off detailed analysis display

3. **Improve Response Speed**
   - Decrease `API_TIMEOUT` value
   - Optimize network connection

## Extended Features

### Add More Trading Pairs
Modify `WEBSOCKET_URL` and `SYMBOL` in configuration file:

```python
# Analyze ETHUSDT
WEBSOCKET_URL = "wss://fstream.binance.com/ws/ethusdt@aggTrade"
SYMBOL = "ETHUSDT"
```

### Add Data Storage
Can extend program to save analysis results to database or files.

### Add Alert Function
Can add alert function for price anomalies or large order detection.

## Notes

1. **Data Delay**: Local Order Book system needs time to collect historical data
2. **API Limits**: Pay attention to local API call frequency limits
3. **Network Stability**: Ensure network connection is stable
4. **Time Synchronization**: Ensure system time is accurate

## Technical Support

If you encounter problems, please:

1. Check if local Order Book system is running normally
2. View program log output
3. Confirm network connection is normal
4. Check configuration file settings
