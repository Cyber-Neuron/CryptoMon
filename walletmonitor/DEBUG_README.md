# Wallet Monitor Debug Mode

This document explains how to use walletmonitor's debug mode to observe transaction processing details.

## Overview

Debug mode provides detailed log information, allowing you to observe:
- Block processing procedures
- Detailed analysis of each transaction
- Identification of ETH and ERC20 token transfers
- Wallet information extraction process
- Database storage operations

## Quick Start

### Method 1: Use Debug Startup Script (Recommended)

```bash
# Navigate to walletmonitor directory
cd walletmonitor

# Run debug startup script
./start_debug.sh
```

### Method 2: Run Debug Main Program Directly

```bash
# Set environment variables
export DEBUG_MODE=true
export DEBUG_TRANSACTION_DETAILS=true
export DEBUG_WALLET_INFO=true
export LOG_LEVEL=DEBUG
export MIN_ETH=1.0
export POLL_INTERVAL_SEC=30

# Run debug program
python3 debug_main.py
```

### Method 3: Use Regular Main Program with Debug Enabled

```bash
# Set debug environment variables
export DEBUG_MODE=true
export DEBUG_TRANSACTION_DETAILS=true
export DEBUG_WALLET_INFO=true
export LOG_LEVEL=DEBUG

# Run regular main program
python3 main.py
```

## Debug Configuration Options

### Environment Variables

| Variable Name | Default Value | Description |
|---------------|---------------|-------------|
| `DEBUG_MODE` | `true` | Enable debug mode |
| `DEBUG_TRANSACTION_DETAILS` | `true` | Show transaction processing details |
| `DEBUG_WALLET_INFO` | `true` | Show wallet information extraction details |
| `LOG_LEVEL` | `DEBUG` | Log level |
| `MIN_ETH` | `1.0` | Minimum ETH threshold (lower to see more transactions) |
| `POLL_INTERVAL_SEC` | `30` | Polling interval (seconds) |

### Configuration Files

- `debug_config.py` - Debug-specific configuration
- `config.py` - Standard configuration (debug options added)

## Debug Log Details

### 1. Startup Information

```
====================================================================================================
DEBUG WALLET MONITOR STARTING
====================================================================================================
Logging level: DEBUG
Debug mode: True
Debug transaction details: True
Debug wallet info: True
Minimum ETH threshold: 1.0
Poll interval: 30 seconds
====================================================================================================
```

### 2. Monitoring Address Retrieval

```
============================================================
FETCHING WATCH ADDRESSES
============================================================
Retrieved 10 total wallets from database
WATCH ADDRESSES:
  0x1234... -> Binance Hot Wallet (BINANCE)
  0x5678... -> Coinbase Hot Wallet (COINBASE)
============================================================
```

### 3. Block Processing

```
Fetching recent blocks from last 10 minutes...
Current block number: 18500000
Current timestamp: 1703123456
Target timestamp: 1703122856 (looking back 10 minutes)
  Checking block 18500000 (1/100)
    Block 18500000 timestamp: 1703123456
    Added block 18500000 with 150 transactions
```

### 4. Transaction Processing Details

#### ETH Transfer

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

#### ERC20 Transfer

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

### 5. Wallet Information Extraction

```
Extracting wallet info for address: 0x1234...
Arkham API response for 0x1234...: {'arkhamEntity': {'name': 'Binance Hot Wallet', 'id': 'BINANCE', 'type': 'exchange'}}
Created wallet info: Binance Hot Wallet (BINANCE) for 0x1234...
```

### 6. Processing Summary

```
Processing 5 blocks with 10 watch addresses
ETH price: $2500.00
Minimum ETH threshold: 1.0 ETH
Processing block 18500000 (1/5) with 150 transactions
  Block timestamp: 1703123456
  Block hash: 18500000
    Processing transaction 1/150: 0xabcd...
    Found 1 relevant transactions
  Block 18500000 summary: 1 relevant transactions

Creating exchange flows from transactions...
  Creating flow 1/3 for tx: 0xabcd...
    Created flow: Binance Hot Wallet -> Unknown Wallet

Transaction summary:
  0xabcd...: Binance Hot Wallet -> Unknown Wallet (1.0 ETH)
  0xefgh...: Coinbase Hot Wallet -> Binance Hot Wallet (5000.0 USDT)
```

## Log Files

Debug mode outputs to both:
- Console (real-time viewing)
- `debug.log` file (persistent storage)

Each startup automatically backs up the old `debug.log` as `debug.log.bak`.

## Performance Tuning

### Reduce Log Verbosity

If logs are too verbose and affect performance, you can adjust:

```bash
# Only show transaction details, not wallet info
export DEBUG_WALLET_INFO=false

# Only show basic information
export LOG_LEVEL=INFO
export DEBUG_MODE=false
```

### Adjust Monitoring Parameters

```bash
# Increase minimum threshold to reduce number of processed transactions
export MIN_ETH=10.0

# Increase polling interval to reduce processing frequency
export POLL_INTERVAL_SEC=60
```

## Troubleshooting

### Common Issues

1. **Log File Too Large**
   - Regularly clean up `debug.log` file
   - Adjust log level to INFO

2. **Slow Processing Speed**
   - Increase `MIN_ETH` threshold
   - Reduce `DEBUG_WALLET_INFO` output
   - Increase `POLL_INTERVAL_SEC`

3. **High Memory Usage**
   - Reduce number of blocks processed
   - Disable unnecessary debug options

### Monitoring Recommendations

- Use debug mode in development/test environments
- Production environment should use INFO level
- Regularly check log file size
- Adjust debug options based on actual needs

## Example Output

For complete debug output examples, see the `debug.log` file, which contains:
- Detailed information for each processing step
- Complete transaction data parsing
- Wallet information extraction process
- Database operation details
- Complete stack traces for errors and exceptions
