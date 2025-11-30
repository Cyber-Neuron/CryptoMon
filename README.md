# Trade Monitor - Comprehensive Cryptocurrency Monitoring & Analysis Platform

This is a comprehensive Python-based cryptocurrency monitoring and analysis platform that has evolved from a Bitcoin P2P network monitoring tool into a complete multi-chain trading monitoring, analysis, and visualization system.

## 🎯 Project Overview

The platform provides real-time monitoring, analysis, and visualization of cryptocurrency transactions, fund flows, order books, and market data across multiple blockchains and exchanges.

## ✨ Core Modules

### 1. **Wallet Monitor** (`walletmonitor/`)
Ethereum transaction monitoring system for tracking large transactions and fund flows.

**Features:**
- Real-time monitoring of large ETH and ERC20 token transactions
- Arkham wallet label integration
- Fund flow visualization dashboard
- ETF flow analysis with macro event markers
- Transaction records and charts
- Debug mode for detailed transaction analysis
- Data completer for missing wallet information

**Quick Start:**
```bash
cd walletmonitor
docker-compose up -d  # Start PostgreSQL
python main.py        # Start monitoring
```

**Documentation:**
- [Wallet Monitor README](walletmonitor/README.md)
- [Debug Mode Guide](walletmonitor/DEBUG_README.md)
- [Deployment Guide](walletmonitor/DEPLOYMENT_GUIDE.md)
- [Project Summary](walletmonitor/PROJECT_SUMMARY.md)

### 2. **Order Book System** (`orderbook/`)
Local order book maintenance and futures trading analysis system.

**Features:**
- Real-time Binance Futures WebSocket connection
- Local order book snapshot maintenance
- Historical data storage (24 hours)
- REST API for querying position quantities
- Nearest level price queries
- Futures trade analyzer
- Synchronized large order detection with voice alerts
- Google TTS integration for trading alerts

**Quick Start:**
```bash
cd orderbook
pip install -r requirements.txt
./start_simple.sh  # Start order book system
```

**Documentation:**
- [Order Book README](orderbook/README.md)
- [Usage Guide](orderbook/USAGE.md)
- [Troubleshooting](orderbook/TROUBLESHOOTING.md)
- [Trade Analyzer Guide](orderbook/TRADE_ANALYZER_README.md)
- [TTS Voice Alerts](orderbook/TTS_README.md)

### 3. **Exchange Monitor** (`exchange_monitor/`)
Exchange wallet balance monitoring with real-time candlestick charts.

**Features:**
- Monitors ETH and USDT balance changes for specified wallet addresses
- Real-time candlestick charts with multiple timeframes
- Supabase integration
- Next.js web interface deployed on Vercel

**Quick Start:**
```bash
cd exchange_monitor
pip install -r requirements.txt
python monitor.py  # Start monitoring
cd web && npm install && npm run dev  # Start frontend
```

**Documentation:**
- [Exchange Monitor README](exchange_monitor/README.md)

### 4. **Binance Data Collector** (`binance_data_collector/`)
Comprehensive Binance market data collection toolkit.

**Features:**
- Spot order book depth and trades
- Perpetual/Delivery contract funding rates and open interest
- Contract liquidation orders
- Options chain and IV curve snapshots
- Batch data collection

**Quick Start:**
```bash
cd binance_data_collector
pip install -r requirements.txt
# Configure API keys in config.yaml
python run_all.py  # Run all collectors
```

**Documentation:**
- [Binance Data Collector README](binance_data_collector/README.md)

### 5. **Visualization Dashboard** (`walletmonitor/vercel-app/`)
Next.js-based fund flow monitoring dashboard.

**Features:**
- Fund flow charts using TradingView Lightweight Charts
- Multi-token support (ETH, USDC, USDT, etc.)
- Time range selection (1 hour to 30 days)
- ETF flow analysis with macro events
- Transaction records and charts
- Responsive design

**Quick Start:**
```bash
cd walletmonitor/vercel-app
npm install
npm run dev  # Development
npm run build  # Production build
```

**Documentation:**
- [Flow Monitor README](walletmonitor/vercel-app/README.md)
- [ETF Analysis Guide](walletmonitor/vercel-app/ETF_README.md)
- [Transaction Charts](walletmonitor/vercel-app/TRANSACTIONS_CHART_README.md)
- [Deployment Guide](walletmonitor/DEPLOYMENT_GUIDE.md)

### 6. **Bitcoin P2P Monitor** (`exchange_monitor/`)
Original Bitcoin P2P network monitoring through Tor.

**Features:**
- Anonymous connection to Bitcoin nodes through Tor
- Support for .onion hidden service nodes
- Automatic Bitcoin P2P protocol handshake
- Large transaction monitoring (default: 100 BTC threshold)

## 🚀 System Requirements

- **Python**: 3.9+
- **Node.js**: 16+ (for frontend interfaces)
- **PostgreSQL**: Database for data storage
- **Docker & Docker Compose**: Containerized deployment
- **Tor**: For Bitcoin P2P monitoring (optional)

## 📦 Installation

### 1. Clone Repository
```bash
git clone https://github.com/Cyber-Neuron/trade_monitor.git
cd trade_monitor
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install Frontend Dependencies
```bash
# For exchange monitor web interface
cd exchange_monitor/web
npm install

# For wallet monitor dashboard
cd walletmonitor/vercel-app
npm install
```

### 4. Database Setup
```bash
# Create PostgreSQL database
createdb trade_monitor

# Import schemas (if available)
psql trade_monitor < visualization/crawler/database/db.sql
```

### 5. Configuration
Each module has its own configuration file. See individual module READMEs for details:
- `walletmonitor/config.py` - Wallet monitoring configuration
- `exchange_monitor/config.py` - Exchange monitoring configuration
- `orderbook/config.py` - Order book configuration
- `binance_data_collector/config.yaml` - Binance API keys

## 🎮 Usage Examples

### Wallet Monitoring
```bash
cd walletmonitor
docker-compose up -d  # Start database
python main.py        # Start monitoring
```

### Order Book System
```bash
cd orderbook
./start_simple.sh     # Start order book
# In another terminal
python future_trade_analyzer.py  # Start trade analyzer
```

### Fund Flow Dashboard
```bash
cd walletmonitor/vercel-app
npm run dev
# Visit http://localhost:3000
```

### Binance Data Collection
```bash
cd binance_data_collector
python run_all.py  # Collect all data types
```

## 📊 Key Features

### Real-time Monitoring
- Real-time transaction monitoring across multiple blockchains
- WebSocket connections for live data streams
- Automatic reconnection and error recovery

### Data Analysis
- Fund flow analysis and visualization
- Order book depth analysis
- Futures trading pattern detection
- Synchronized large order identification
- ETF flow correlation with macro events

### Visualization
- TradingView Lightweight Charts integration
- Interactive candlestick charts
- Fund flow bar charts
- Transaction timeline visualization
- Responsive web dashboards

### Alerting
- Google TTS voice alerts for trading events
- Synchronized large order alerts
- Price anomaly detection
- Custom alert rules

## 🏗️ Architecture

```
trade_monitor/
├── walletmonitor/          # Ethereum wallet monitoring
│   ├── main.py            # Main monitoring service
│   ├── vercel-app/        # Next.js dashboard
│   └── ...
├── orderbook/              # Order book system
│   ├── localorderbok.py   # Order book maintenance
│   ├── future_trade_analyzer.py  # Trade analysis
│   └── ...
├── exchange_monitor/       # Exchange monitoring
│   ├── monitor.py         # Balance monitoring
│   └── web/               # Frontend interface
├── binance_data_collector/ # Binance data collection
│   ├── binance_spot.py
│   ├── binance_futures.py
│   └── binance_options.py
└── visualization/          # Visualization tools
```

## 📚 Documentation

Each module has comprehensive documentation:

- **Wallet Monitor**: [README](walletmonitor/README.md) | [Debug Guide](walletmonitor/DEBUG_README.md) | [Deployment](walletmonitor/DEPLOYMENT_GUIDE.md)
- **Order Book**: [README](orderbook/README.md) | [Usage](orderbook/USAGE.md) | [Troubleshooting](orderbook/TROUBLESHOOTING.md)
- **Exchange Monitor**: [README](exchange_monitor/README.md)
- **Binance Collector**: [README](binance_data_collector/README.md)
- **Dashboard**: [Flow Monitor](walletmonitor/vercel-app/README.md) | [ETF Analysis](walletmonitor/vercel-app/ETF_README.md)

## 🔧 Configuration

### Environment Variables
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/trade_monitor

# Ethereum Node
PUBLICNODE_URL=https://eth-mainnet.g.alchemy.com/v2/your-api-key

# Arkham API (optional)
ARKHAM_API_KEY=your-arkham-api-key

# Binance API (for data collector)
BINANCE_API_KEY=your-api-key
BINANCE_API_SECRET=your-api-secret
```

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check PostgreSQL is running
   - Verify `DATABASE_URL` environment variable
   - Check database permissions

2. **WebSocket Connection Issues**
   - Verify network connectivity
   - Check API endpoint availability
   - Review connection logs

3. **Module Import Errors**
   - Ensure all dependencies are installed
   - Check Python path configuration
   - Verify virtual environment activation

4. **Frontend Build Errors**
   - Check Node.js version (16+)
   - Clear `node_modules` and reinstall
   - Verify environment variables

See individual module troubleshooting guides for more details.

## 🤝 Contributing

Welcome to submit Issues and Pull Requests to improve the project. Please ensure:

1. Code follows project standards
2. Add necessary tests
3. Update relevant documentation
4. Follow commit message conventions

## 📝 License

MIT License

## 🔗 Related Projects

- [TradingView Lightweight Charts](https://www.tradingview.com/lightweight-charts/)
- [Arkham Intelligence](https://www.arkhamintelligence.com/)
- [Binance API](https://binance-docs.github.io/apidocs/)

## 📧 Support

For issues and questions:
- Check module-specific README files
- Review troubleshooting guides
- Open an issue on GitHub

---

**Note**: This project is actively maintained and continuously evolving. Check individual module documentation for the latest features and updates.
