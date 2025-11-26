# Bitcoin P2P Network Monitor (trade_monitor)

This is a Python-based Bitcoin P2P network monitoring tool that connects to Bitcoin nodes through the Tor network to monitor and analyze large transactions. The project has been extended into a complete trading monitoring and analysis platform.

## Features

- Anonymous connection to Bitcoin nodes through the Tor network
- Support for connecting to .onion hidden service nodes
- Automatic Bitcoin P2P protocol handshake completion
- Monitor and analyze large transactions (default threshold: 100 BTC)
- Detailed logging and error handling
- Support for parallel multi-node connections
- New features:
  - Arkham wallet label tracking
  - Transaction data visualization
  - Smart contract analysis
  - Multi-chain data monitoring
  - Real-time price tracking
  - Whale transaction monitoring
  - Institutional trading analysis

## System Requirements

- Python 3.9+
- Docker and Docker Compose
- Tor service
- Node.js 16+ (for frontend interface)
- PostgreSQL database

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Cyber-Neuron/trade_monitor.git
cd trade_monitor
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install frontend dependencies:
```bash
cd exchange_monitor/web
npm install
```

4. Configure the database:
```bash
# Create PostgreSQL database
createdb trade_monitor
# Import database schema
psql trade_monitor < visualization/crawler/database/db.sql
```

5. Configure Tor:
- Ensure Tor service is installed and running
- Default SOCKS5 proxy: `socks5h://127.0.0.1:9050`

## Usage

1. Start Tor service:
```bash
docker-compose up -d tor
```

2. Start monitoring service:
```bash
python exchange_monitor/monitor.py
```

3. Start frontend interface:
```bash
cd exchange_monitor/web
npm run dev
```

The program will automatically:
- Wait for Tor network to be ready
- Test Tor connection
- Fetch node list from Bitnodes
- Connect to Bitcoin nodes
- Start monitoring transactions
- Analyze and display transaction data

## Configuration

Main configuration parameters (in `exchange_monitor/config.py`):

```python
# Bitcoin network constants
MAGIC_MAINNET = bytes.fromhex("f9beb4d9")
PROTOCOL_VERSION = 70016
LARGE_TX_THRESHOLD_BTC = 100  # Large transaction threshold

# Tor proxy configuration
TOR_PROXY = os.getenv("TOR_PROXY", "socks5h://127.0.0.1:9050")

# Database configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "trade_monitor")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
```

## New Features

### Arkham Integration
- Wallet label tracking support
- Automatic wallet information updates
- Transaction history analysis

### Visualization Features
- Real-time transaction charts
- Whale transaction tracking
- Institutional trading analysis
- Price trend charts

### Smart Contract Analysis
- Contract code auditing
- Transaction pattern recognition
- Risk warning system

## Logging

The program uses Python's logging module to record logs, including:
- Connection status
- Message exchange
- Transaction analysis
- Error messages
- Performance metrics
- System status

Log format:
```
Timestamp - Log Level - Module Name - Message Content
```

## Notes

1. Ensure Tor service is running normally
2. The program requires network connection
3. Large transaction threshold can be adjusted as needed
4. It is recommended to test in a test environment first
5. Regularly backup the database
6. Pay attention to API call limits

## Troubleshooting

1. Tor connection issues:
   - Check Tor service status
   - Verify proxy configuration
   - View detailed logs

2. Node connection issues:
   - Check network connection
   - Verify node address format
   - Check connection timeout settings

3. Database issues:
   - Check database connection configuration
   - Verify database permissions
   - View database logs

4. Frontend issues:
   - Check Node.js version
   - Verify dependency installation
   - Check browser console

## Contributing

Welcome to submit Issues and Pull Requests to improve the project. Please ensure:
1. Code follows project standards
2. Add necessary tests
3. Update relevant documentation
4. Follow commit message conventions

## License

MIT License
