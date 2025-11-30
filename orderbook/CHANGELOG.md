# Changelog

## v1.1.0 - Nearest Level Feature

### New Features
- ✨ Added nearest level query functionality
- ✨ Support returning current time nearest level when timestamp is not provided
- ✨ New `/nearest-level/{price}` API endpoint
- ✨ Enhanced `/quantity` API, supports optional timestamp parameter

### Bug Fixes
- 🐛 Fixed Ctrl+C unable to exit normally issue
- 🐛 Added graceful shutdown mechanism
- 🐛 Improved signal handling logic
- 🐛 Optimized WebSocket connection close flow
- 🐛 Fixed signal handling issues in async environment
- 🐛 Added simplified startup script to solve shell script signal passing issues

### Feature Description
1. **Nearest Level Query**: When the queried price doesn't exist, the system returns the nearest price level and quantity to that price
2. **Smart Price Matching**: System searches for the price with minimum distance in both bids and asks
3. **Price Difference Calculation**: Returns the distance between nearest level and target price
4. **Real-time Data**: Returns current real-time data when timestamp is not provided
5. **Graceful Shutdown**: Supports Ctrl+C normal exit, waits for WebSocket connection to close

### API Changes
- `POST /quantity` now supports optional timestamp parameter
- New `GET /nearest-level/{price}` endpoint
- Response format added `actual_price` and `is_nearest_level` fields

### Usage Examples
```bash
# Query nearest level (without timestamp)
curl -X POST "http://localhost:8000/quantity" \
     -H "Content-Type: application/json" \
     -d '{"price": 50000.0}'

# Query nearest level API
curl "http://localhost:8000/nearest-level/50000.0"
```

### File Changes
- `localorderbok.py`: Added nearest level query logic and signal handling
- `test_orderbook.py`: Updated test cases
- `client_example.py`: Updated client examples
- `demo_nearest_level.py`: New demo script
- `test_shutdown.py`: New signal handling test script
- `start.sh`: Improved startup script, added signal handling
- `README.md`: Updated documentation
- `USAGE.md`: Updated usage instructions

## v1.0.0 - Initial Version

### Basic Features
- 🔄 Real-time WebSocket connection
- 📊 Local Order Book maintenance
- 🕒 Historical data storage
- 🌐 REST API service
- 📈 Open interest difference calculation
