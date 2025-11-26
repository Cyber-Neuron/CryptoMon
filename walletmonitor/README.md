# Wallet Monitor - Refactored Version

## Overview

This is a refactored ETH transaction monitoring system for monitoring large transactions on the Ethereum blockchain and tracking fund flows of wallet addresses. The system uses Docker containerized deployment and includes a local PostgreSQL database.

## Key Features

### 🚀 Performance Optimization
- **Batch database operations**: Reduce database read/write operations
- **Caching mechanism**: Avoid duplicate queries
- **Optimized indexes**: Improve query performance

### 🏗️ Code Structure
- **Data models**: Use `@dataclass` for type safety
- **Modular design**: Separation of concerns, easy to maintain
- **Object-oriented**: Clear class structure

### 🐳 Containerized Deployment
- **Docker Compose**: One-click startup of complete environment
- **Local database**: PostgreSQL + pgAdmin
- **Health checks**: Automatic service status monitoring

## Quick Start

### 1. Start Database

```bash
# Start PostgreSQL and pgAdmin
docker-compose up -d

# Check service status
docker-compose ps
```

### 2. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt
```

### 3. Configure Environment

Edit the `config.py` file to set your configuration:

```python
# Database configuration (use environment variables)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/walletmonitor")

# Ethereum node configuration (replace with your API key)
PUBLICNODE_URL = "https://eth-mainnet.g.alchemy.com/v2/your-api-key"

# Monitoring configuration
MIN_ETH = 10.0  # Minimum monitoring amount (ETH)
POLL_INTERVAL_SEC = 60  # Polling interval (seconds)
```

### 4. Run Tests

```bash
# Test data models and database connection
python test.py
```

### 5. Start Monitoring

```bash
# Start wallet monitoring service
python main.py
```

## Database Access

### pgAdmin Web Interface
- **URL**: http://localhost:8080
- **Email**: Check environment variable `PGADMIN_EMAIL`
- **Password**: Check environment variable `PGADMIN_PASSWORD`

### Direct Connection
```bash
# Connect to PostgreSQL
# Use database credentials from environment variables
psql -h localhost -p 5432 -U ${DB_USER} -d ${DB_NAME}
```

## Data Models

### Wallet
```python
@dataclass
class Wallet:
    address: str                    # Wallet address
    chain_id: str = "ethereum"      # Chain ID
    friendly_name: Optional[str]    # Friendly name
    grp_type: Optional[str]         # Group type (Hot/Cold, etc.)
    grp_name: Optional[str]         # Group name (binance/coinbase, etc.)
```

### Transaction
```python
@dataclass
class Transaction:
    hash: str                       # Transaction hash
    block_number: int               # Block number
    from_address: str               # Sender address
    to_address: str                 # Receiver address
    amount: Decimal                 # Amount
    token: str                      # Token symbol
    timestamp: int                  # Timestamp
    usd_value: Optional[Decimal]    # USD value
```

### ExFlow (Fund Flow)
```python
@dataclass
class ExFlow:
    timestamp: int                  # Timestamp
    token: str                      # Token
    from_grp_name: Optional[str]    # Sender group name
    to_grp_name: Optional[str]      # Receiver group name
    amount: Optional[Decimal]       # Amount
    usd_value: Optional[Decimal]    # USD value
    tx_hash: Optional[str]          # Transaction hash
```

## Monitoring Process

1. **Get monitoring addresses**: Get wallet addresses to monitor from database
2. **Get latest blocks**: Get blocks from last 10 minutes
3. **Extract transactions**: Extract transaction hashes from blocks
4. **Filter transactions**: Filter large transactions based on amount
5. **Get wallet information**: Get wallet labels through Arkham API
6. **Store data**: Batch store transactions and fund flow data

## File Structure

```
walletmonitor/
├── docker-compose.yml     # Docker orchestration file
├── init.sql              # Database initialization script
├── main.py               # Main program entry
├── test.py               # Test script
├── config.py             # Configuration file
├── models.py             # Data models
├── database.py           # Database manager
├── block_processor.py    # Block processor
├── arkham.py             # Arkham API client
├── requirements.txt      # Python dependencies
└── README.md             # Documentation
```

## Database Schema

### chains (Chains)
- Stores supported blockchain information

### tokens (Tokens)
- Stores token information (ETH, USDT, USDC, etc.)

### wallets (Wallets)
- Stores wallet addresses and label information

### transactions (Transactions)
- Stores transaction records

### ex_flows (Fund Flows)
- Stores fund flow data

## Performance Optimization

### Database Optimization
- Batch insert operations
- Caching mechanism
- Optimized indexes
- Connection pool management

### Network Optimization
- ETH price caching (1 minute)
- Wallet information caching
- Batch API calls

### Memory Optimization
- Use Decimal for precise numerical values
- Timely cache cleanup
- Optimize data structures

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   ```bash
   # Check Docker container status
   docker-compose ps
   
   # Restart services
   docker-compose restart
   ```

2. **Dependency Installation Failed**
   ```bash
   # Upgrade pip
   pip install --upgrade pip
   
   # Reinstall dependencies
   pip install -r requirements.txt --force-reinstall
   ```

3. **API Key Issues**
   - Ensure correct Ethereum node URL is set in `config.py`
   - Check if API key is valid

### View Logs

```bash
# View application logs
python main.py

# View database logs
docker-compose logs postgres

# View pgAdmin logs
docker-compose logs pgadmin
```

## Development Guide

### Adding New Token Support
1. Add token contract address in `block_processor.py`
2. Add token record in `init.sql`
3. Update token decimal handling logic

### Extending Monitoring Features
1. Add new data models in `models.py`
2. Add corresponding database operations in `database.py`
3. Add processing logic in `block_processor.py`

## License

MIT License
