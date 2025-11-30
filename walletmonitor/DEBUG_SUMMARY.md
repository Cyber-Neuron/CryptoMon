# Wallet Monitor Debug Feature Summary

## Overview

I have added comprehensive debug functionality to the walletmonitor project, allowing you to observe transaction processing details. These features include detailed logging, configurable debug options, and specialized debug tools.

## New Files

### 1. Configuration Files
- **`debug_config.py`** - Debug-specific configuration class, inherits from Config
- **`config.py`** - Updated with debug-related configuration options

### 2. Main Program Files
- **`debug_main.py`** - Debug version of the main program, providing maximum debugging information
- **`main.py`** - Updated to support debug mode

### 3. Core Processing Files
- **`block_processor.py`** - Updated with detailed transaction processing debug information

### 4. Tools and Scripts
- **`start_debug.sh`** - Debug mode startup script
- **`test_debug.py`** - Debug functionality test script
- **`DEBUG_README.md`** - Detailed usage documentation

## Main Features

### 1. Configurable Debug Options

```python
# New configuration items in config.py
DEBUG_MODE: bool = True                    # Enable debug mode
DEBUG_TRANSACTION_DETAILS: bool = True     # Show transaction processing details
DEBUG_WALLET_INFO: bool = True             # Show wallet information extraction details
```

### 2. Environment Variable Support

```bash
export DEBUG_MODE=true
export DEBUG_TRANSACTION_DETAILS=true
export DEBUG_WALLET_INFO=true
export LOG_LEVEL=DEBUG
export MIN_ETH=1.0
export POLL_INTERVAL_SEC=30
```

### 3. Detailed Logging

#### Block Processing Logs
```
Fetching recent blocks from last 10 minutes...
Current block number: 18500000
Current timestamp: 1703123456
Target timestamp: 1703122856 (looking back 10 minutes)
  Checking block 18500000 (1/100)
    Block 18500000 timestamp: 1703123456
    Added block 18500000 with 150 transactions
```

#### Transaction Processing Logs
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

#### ERC20 Transfer Logs
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

#### Wallet Information Extraction Logs
```
Extracting wallet info for address: 0x1234...
Arkham API response for 0x1234...: {'arkhamEntity': {'name': 'Binance Hot Wallet', 'id': 'BINANCE', 'type': 'exchange'}}
Created wallet info: Binance Hot Wallet (BINANCE) for 0x1234...
```

### 4. Multiple Startup Methods

#### Method 1: Use Debug Startup Script (Recommended)
```bash
./start_debug.sh
```

#### Method 2: Run Debug Main Program Directly
```bash
python3 debug_main.py
```

#### Method 3: Use Regular Main Program with Debug Enabled
```bash
export DEBUG_MODE=true
export DEBUG_TRANSACTION_DETAILS=true
export DEBUG_WALLET_INFO=true
export LOG_LEVEL=DEBUG
python3 main.py
```

### 5. Log File Management

- Debug mode outputs to both console and `debug.log` file
- Each startup automatically backs up old log file as `debug.log.bak`
- Supports real-time viewing and persistent storage

### 6. Performance Optimization Options

```bash
# Reduce log verbosity
export DEBUG_WALLET_INFO=false
export LOG_LEVEL=INFO

# Adjust monitoring parameters
export MIN_ETH=10.0
export POLL_INTERVAL_SEC=60
```

## Debug Information Coverage

### 1. Startup Phase
- Configuration information display
- Component initialization status
- Connection test results

### 2. Monitoring Address Retrieval
- Database query details
- Address filtering process
- Wallet information display

### 3. Block Processing
- Block retrieval process
- Time range calculation
- Transaction count statistics

### 4. Transaction Processing
- Detailed analysis of each transaction
- ETH transfer identification and processing
- ERC20 transfer parsing
- Amount conversion and threshold checking
- Wallet information extraction

### 5. Data Storage
- Database operation details
- Transaction and flow data statistics
- Storage result confirmation

### 6. Error Handling
- Detailed exception information
- Stack traces
- Error recovery process

## Usage Recommendations

### Development/Test Environment
- Use debug mode for development and testing
- Set lower `MIN_ETH` threshold to see more transactions
- Use shorter polling intervals for quick feedback

### Production Environment
- Use INFO level logging
- Disable debug options to improve performance
- Regularly check log file size

### Performance Tuning
- Adjust debug options based on actual needs
- Monitor memory and CPU usage
- Regularly clean up log files

## Test Verification

Run test script to verify debug functionality:
```bash
python3 test_debug.py
```

Test content includes:
- Configuration loading tests
- Logging functionality tests
- Environment variable tests
- Wallet information extraction tests

## Summary

With these debug features, you can now:

1. **Observe Transaction Processing** - Each transaction has detailed processing logs
2. **Monitor Wallet Information Extraction** - Understand Arkham API calls and responses
3. **Track Block Processing** - View detailed process of block retrieval and parsing
4. **Analyze Performance Bottlenecks** - Identify performance issues through detailed logs
5. **Debug Configuration Issues** - Verify that configurations are loaded correctly
6. **Troubleshoot Errors** - Get complete error information and stack traces

These features will help you gain deep insights into walletmonitor's working mechanism and quickly locate and resolve issues.
