# Local Order Book Maintenance System

This is a local order book maintenance system based on Binance Futures WebSocket API, providing REST API to query position quantity differences at specific prices and time points.

## Features

- 🔄 Real-time connection to Binance Futures WebSocket to get depth data
- 📊 Maintain local order book snapshots
- 🕒 Save historical data (last 24 hours)
- 🌐 Provide REST API query interface
- 📈 Support querying position quantity differences at any time point

## System Architecture

According to [Binance official documentation](https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams/How-to-manage-a-local-order-book-correctly), the system implements the following steps:

1. Connect to WebSocket stream: `wss://fstream.binance.com/stream?streams=ETHUSDT@depth`
2. Buffer received events
3. Get depth snapshot: `https://fapi.binance.com/fapi/v1/depth?symbol=ETHUSDT&limit=1000`
4. Discard events where u < lastUpdateId
5. First event satisfies: U ≤ lastUpdateId AND u ≥ lastUpdateId
6. Check event sequence continuity
7. Update local order book
8. Handle price levels with quantity 0 (remove)

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run System

### Method 1: Use simplified startup script (recommended)
```bash
./start_simple.sh
```

### Method 2: Use full startup script
```bash
./start.sh
```

### Method 3: Run directly
```bash
python localorderbok.py
```

After system startup:
1. Connect to Binance WebSocket
2. Get initial depth snapshot
3. Start FastAPI server (port 8000)
4. Begin maintaining local order book

## API Interface

### 1. System Status
```
GET /status
```
Returns system running status, including connection status, order book information, etc.

### 2. Current Order Book
```
GET /orderbook
```
Returns current complete order book data.

### 3. Query Position Quantity
```
POST /quantity
Content-Type: application/json

# Query historical data (with timestamp)
{
    "price": 50000.0,
    "timestamp": 1703123456
}

# Query nearest level (without timestamp)
{
    "price": 50000.0
}
```
Returns position quantity at specified price and time point, and the difference from 1 second ago. If timestamp is not provided, returns the nearest price level and quantity to the target price.

### 4. Nearest Level Query
```
GET /nearest-level/{price}
```
Get the nearest price level and quantity to the specified price.

### 5. Historical Data Information
```
GET /history
```
Returns statistical information about historical data.

## Usage Examples

### Start System
```bash
# Terminal 1: Start main program
python localorderbok.py
```

### Test API
```bash
# Terminal 2: Run test script
python test_orderbook.py
```

### Manual Query Examples
```bash
# Query position quantity at specific price for current time (nearest level)
curl -X POST "http://localhost:8000/quantity" \
     -H "Content-Type: application/json" \
     -d '{"price": 50000.0}'

# Query position quantity at specific price for historical time
curl -X POST "http://localhost:8000/quantity" \
     -H "Content-Type: application/json" \
     -d '{"price": 50000.0, "timestamp": 1703123456}'

# Get nearest level information
curl "http://localhost:8000/nearest-level/50000.0"

# Get system status
curl "http://localhost:8000/status"

# Get current order book
curl "http://localhost:8000/orderbook"
```

## Response Format

### Position Quantity Query Response
```json
{
    "target_price": 50000.0,
    "actual_price": 50001.0,
    "timestamp": 1703123456,
    "quantity": 1.234,
    "difference": 0.123,
    "is_nearest_level": false
}
```

- `target_price`: Target price for query
- `actual_price`: Actual returned price (may be nearest level)
- `timestamp`: Query timestamp
- `quantity`: Position quantity at this price point
- `difference`: Difference from position quantity 1 second ago
- `is_nearest_level`: Whether returned value is nearest level

### Nearest Level Query Response
```json
{
    "target_price": 50000.0,
    "nearest_price": 50001.0,
    "quantity": 1.234,
    "timestamp": 1703123456,
    "price_difference": 1.0
}
```

- `target_price`: Target price for query
- `nearest_price`: Nearest price level
- `quantity`: Position quantity at this price point
- `timestamp`: Query timestamp
- `price_difference`: Price difference (nearest_price - target_price)

### System Status Response
```json
{
    "symbol": "ETHUSDT",
    "is_connected": true,
    "last_update_id": 123456789,
    "bids_count": 1000,
    "asks_count": 1000,
    "history_count": 3600
}
```

## Configuration Options

You can modify the following configuration in `localorderbok.py`:

- `symbol`: Trading pair symbol (default: ETHUSDT)
- `port`: API server port (default: 8000)
- Historical data retention time (default: 24 hours)

## Notes

1. **Network Connection**: Ensure access to Binance API
2. **Memory Usage**: System saves 24 hours of historical data, pay attention to memory usage
3. **Time Synchronization**: Ensure system time is accurate for timestamp calculations
4. **Error Handling**: System automatically reconnects WebSocket and handles network exceptions

## Troubleshooting

### WebSocket Connection Failed
- Check network connection
- Confirm Binance API availability
- View log output

### Data Inaccuracy
- Check if event sequence is correct
- Confirm snapshot acquisition success
- Verify timestamp synchronization

### API No Response
- Confirm FastAPI server is started
- Check if port is occupied
- View error logs

### Program Cannot Exit Normally
- Use `./start.sh` startup script (recommended)
- Press `Ctrl+C` and wait a few seconds for graceful shutdown
- If still cannot exit, use `kill -9 <process_id>` to force terminate
- Check if other Python processes are occupying the port

### Signal Handling Issues
- Ensure using latest version of code
- Program now supports graceful shutdown, will wait for WebSocket connection to disconnect normally
- If encountering issues, can run `python test_shutdown.py` to test signal handling

## Technical Details

### Data Flow
1. WebSocket receives real-time depth updates
2. Verify event sequence and ID
3. Update local order book
4. Save historical snapshots
5. Provide API query service

### Performance Optimization
- Use dictionary to store price-quantity mapping
- Save historical snapshots by second
- Automatically clean expired data
- Asynchronous processing of WebSocket and HTTP requests

### Data Consistency
- Strictly follow Binance event processing rules
- Verify event sequence continuity
- Handle duplicate and expired events
- Automatically reinitialize on exceptions
