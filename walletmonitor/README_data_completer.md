# Data Completer Program Usage Instructions

## Overview

The data completer program (`data_completer.py`) is used to supplement missing wallet information in the database. The program finds records in the `transactions` table where `from_wallet_id` or `to_wallet_id` is empty, gets transaction details through Web3 interface, then uses the `extract_wallet_info` method to get wallet information and update the database.

## Features

- 🔍 **Automatic Missing Data Detection**: Automatically finds transaction records in the database with missing wallet information
- 🌐 **Web3 Integration**: Gets transaction details through Ethereum node
- 🏷️ **Wallet Information Extraction**: Uses Arkham API to get wallet labels and group information
- 📊 **Batch Processing**: Supports batch processing of large numbers of transaction records
- 📝 **Detailed Logging**: Provides detailed processing logs and error information
- 🔄 **Transaction Safety**: Uses database transactions to ensure data consistency
- 🖥️ **Command Line Tool**: Provides convenient command line interface

## Usage

### 1. Command Line Tool (Recommended)

```bash
# Check number of incomplete transactions
python cli_completer.py --check

# Run data completion (default batch size 100)
python cli_completer.py --run

# Run data completion (batch size 50)
python cli_completer.py --run --batch-size 50

# Test single transaction
python cli_completer.py --test-tx 0x1234567890abcdef...

# Verbose logging
python cli_completer.py --run --verbose

# Debug mode
python cli_completer.py --run --debug

# Dry-run mode (doesn't actually update database)
python cli_completer.py --run --dry-run
```

### 2. Run Program Directly

```bash
# Run data completer program
python data_completer.py
```

### 3. Test Functionality

```bash
# Run test script
python test_data_completer.py
```

### 4. Use in Code

```python
from data_completer import DataCompleter
from config import load_config

# Load configuration
config = load_config()

# Create data completer
completer = DataCompleter(config)

# Run data completion (default batch size 100)
completer.run(batch_size=50)
```

## Command Line Tool Details

### Parameter Description

- `--check`: Check number of incomplete transactions, does not perform actual processing
- `--run`: Run data completer program
- `--test-tx HASH`: Test processing single transaction
- `--batch-size N`: Set batch size (default: 100)
- `--verbose, -v`: Verbose log output
- `--debug, -d`: Debug mode (most detailed logs)
- `--dry-run`: Dry-run mode (doesn't actually update database)

### Usage Scenarios

1. **First Use**:
   ```bash
   # First check how many incomplete transactions there are
   python cli_completer.py --check
   
   # Dry-run to confirm program works normally
   python cli_completer.py --run --dry-run --verbose
   
   # Run officially
   python cli_completer.py --run --batch-size 50
   ```

2. **Test Specific Transaction**:
   ```bash
   # Test processing single transaction
   python cli_completer.py --test-tx 0x1234567890abcdef... --verbose
   ```

3. **Debug Issues**:
   ```bash
   # Enable debug mode to get most detailed information
   python cli_completer.py --run --debug
   ```

## Configuration Requirements

Ensure the following configurations are correctly set:

1. **Database Connection**: `DATABASE_URL` environment variable or database connection string in config file
2. **Ethereum Node**: `PUBLICNODE_URL` configuration item, pointing to available Ethereum RPC node
3. **Arkham API**: Optional `ARKHAM_API_KEY` for getting wallet label information

## Program Flow

1. **Initialization**: Connect to database and Ethereum node
2. **Find Missing Data**: Query transactions where `from_wallet_id` or `to_wallet_id` is empty
3. **Get Transaction Details**: Get `from` and `to` addresses through Web3
4. **Process Wallet Address**: Call `extract_wallet_info` for each address to get wallet information
5. **Update Database**: Update wallet ID to transaction records
6. **Batch Processing**: Process in batches, provide progress information

## Output Examples

### Command Line Tool Output

```
$ python cli_completer.py --check
Found 150 transactions with missing wallet info

First 5 incomplete transactions:
  1. ID: 123, Hash: 0xabc123...
  2. ID: 124, Hash: 0xdef456...
  3. ID: 125, Hash: 0xghi789...
  4. ID: 126, Hash: 0xjkl012...
  5. ID: 127, Hash: 0xmno345...
  ... and 145 more

$ python cli_completer.py --run --batch-size 50
🚀 Starting data completer program...
2024-01-15 10:30:00 - data_completer - INFO - DataCompleter initialized successfully
2024-01-15 10:30:01 - data_completer - INFO - Found 150 transactions with missing wallet info
2024-01-15 10:30:01 - data_completer - INFO - Processing batch 1/3
...
2024-01-15 10:35:00 - data_completer - INFO - Data completion process finished:
2024-01-15 10:35:00 - data_completer - INFO -   Successfully processed: 145
2024-01-15 10:35:00 - data_completer - INFO -   Failed: 5
2024-01-15 10:35:00 - data_completer - INFO -   Total: 150
✅ Data completer program completed
```

### Test Single Transaction Output

```
$ python cli_completer.py --test-tx 0x1234567890abcdef... --verbose
Testing transaction: 0x1234567890abcdef...
✅ Transaction details retrieved:
  From: 0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6
  To: 0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b7
  Block: 12345678
  From wallet ID: 42
  To wallet ID: 43
```

## Error Handling

The program includes comprehensive error handling:

- **Network Errors**: Automatic retry and error log recording
- **Database Errors**: Transaction rollback and detailed error information
- **API Limits**: Handle Arkham API call limits
- **Invalid Data**: Skip invalid transaction hashes or addresses

## Performance Optimization

- **Batch Processing**: Default batch size is 100, can be adjusted as needed
- **Caching Mechanism**: Utilizes database manager's wallet cache
- **Connection Pool**: Uses database connection pool to improve performance
- **Progress Tracking**: Real-time display of processing progress

## Notes

1. **API Limits**: Pay attention to Arkham API call frequency limits
2. **Network Stability**: Ensure Ethereum node connection is stable
3. **Database Backup**: Recommend backing up database before running
4. **Monitor Resources**: Pay attention to memory and CPU usage when processing large amounts of data
5. **Log Files**: Program automatically creates `data_completer.log` log file

## Troubleshooting

### Common Issues

1. **Connection Failed**: Check `PUBLICNODE_URL` configuration
2. **Database Error**: Verify `DATABASE_URL` and database permissions
3. **API Error**: Check Arkham API key and network connection
4. **Out of Memory**: Reduce batch size

### Debug Mode

Enable debug logs to get more detailed information:

```bash
python cli_completer.py --run --debug
```

Or:

```python
import logging
logging.getLogger().setLevel(logging.DEBUG)
```

## Extended Features

The following features can be extended as needed:

- **Multi-chain Support**: Support other blockchain networks
- **Custom Filters**: Add transaction filter conditions
- **Parallel Processing**: Use multi-threading to improve processing speed
- **Web Interface**: Add web management interface
- **Scheduled Tasks**: Integrate into scheduled task system
