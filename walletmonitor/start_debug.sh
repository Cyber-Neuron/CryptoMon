#!/bin/bash

# Debug startup script for wallet monitoring
# This script runs the wallet monitor in debug mode with maximum detail

echo "=========================================="
echo "Starting Wallet Monitor in DEBUG MODE"
echo "=========================================="

# Set debug environment variables
export DEBUG_MODE=true
export DEBUG_TRANSACTION_DETAILS=true
export DEBUG_WALLET_INFO=true
export LOG_LEVEL=DEBUG
export MIN_ETH=1.0  # Lower threshold to see more transactions
export POLL_INTERVAL_SEC=30  # Shorter interval for faster feedback

echo "Debug configuration:"
echo "  DEBUG_MODE: $DEBUG_MODE"
echo "  DEBUG_TRANSACTION_DETAILS: $DEBUG_TRANSACTION_DETAILS"
echo "  DEBUG_WALLET_INFO: $DEBUG_WALLET_INFO"
echo "  LOG_LEVEL: $LOG_LEVEL"
echo "  MIN_ETH: $MIN_ETH"
echo "  POLL_INTERVAL_SEC: $POLL_INTERVAL_SEC"
echo ""

# Check if debug.log exists and backup it
if [ -f "debug.log" ]; then
    echo "Backing up existing debug.log to debug.log.bak"
    mv debug.log debug.log.bak
fi

echo "Starting debug monitor..."
echo "Logs will be written to both console and debug.log file"
echo "Press Ctrl+C to stop"
echo ""

# Run the debug version
python3 debug_main.py

echo ""
echo "Debug monitor stopped" 