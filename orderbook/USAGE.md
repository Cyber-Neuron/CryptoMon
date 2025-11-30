# Quick Start Guide

## 1. Install Dependencies

```bash
cd orderbook
pip install -r requirements.txt
```

## 2. Start System

### Method 1: Use Simplified Startup Script (Recommended)
```bash
./start_simple.sh
```

### Method 2: Use Full Startup Script
```bash
./start.sh
```

### Method 3: Run Directly
```bash
python localorderbok.py
```

After system startup:
- Connects to Binance WebSocket
- Gets initial depth snapshot
- Starts API server (port 8000)
- Begins maintaining local order book

## 3. Test System

### Run Test Script
```bash
python test_orderbook.py
```

### Run Client Example
```bash
python client_example.py
```

### Run Nearest Level Demo
```bash
python demo_nearest_level.py
```

## 4. API Usage Examples

### Query Position Quantity Difference at Specific Price
```bash
# Query nearest level (without timestamp)
curl -X POST "http://localhost:8000/quantity" \
     -H "Content-Type: application/json" \
     -d '{"price": 50000.0}'

# Query historical data (with timestamp)
curl -X POST "http://localhost:8000/quantity" \
     -H "Content-Type: application/json" \
     -d '{"price": 50000.0, "timestamp": 1703123456}'
```

### Get Nearest Level Information
```bash
curl "http://localhost:8000/nearest-level/50000.0"
```

### Get System Status
```bash
curl "http://localhost:8000/status"
```

### Get Current Order Book
```bash
curl "http://localhost:8000/orderbook"
```

## 5. Configuration Modifications

Edit `config.py` file to modify configuration:

```python
# Modify trading pair
SYMBOL = "ETHUSDT"  # Change to other trading pair

# Modify API port
API_PORT = 8080  # Change to other port

# Modify historical data retention time
HISTORY_RETENTION_HOURS = 12  # Change to 12 hours
```

## 6. Monitoring and Debugging

### View Logs
The system outputs detailed log information, including:
- WebSocket connection status
- Event handling situation
- Error messages

### Check System Status
Visit `http://localhost:8000/status` to view:
- Connection status
- Data statistics
- Number of historical snapshots

## 7. Common Questions

### Q: WebSocket Connection Failed
A: Check network connection, ensure access to Binance API

### Q: API No Response
A: Confirm system has started, check if port is occupied

### Q: Data Inaccurate
A: Wait for system to collect enough historical data, check timestamp synchronization

### Q: High Memory Usage
A: Reduce historical data retention time (modify `HISTORY_RETENTION_HOURS`)

### Q: Program Cannot Exit Normally
A: 
- Use `./start.sh` startup script (recommended)
- Press `Ctrl+C` and wait a few seconds for program to gracefully close
- If still cannot exit, use `kill -9 <process_id>` to force terminate
- Run `python test_shutdown.py` to test signal handling functionality

## 8. Performance Optimization

### Reduce Memory Usage
- Lower historical data retention time
- Reduce snapshot save frequency

### Improve Response Speed
- Use SSD storage
- Increase system memory
- Optimize network connection

## 9. Production Environment Deployment

### Use Process Manager
```bash
# Use PM2
npm install -g pm2
pm2 start localorderbok.py --name orderbook

# Use Supervisor
# Create config file /etc/supervisor/conf.d/orderbook.conf
```

### Use Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "localorderbok.py"]
```

### Reverse Proxy Configuration
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 10. Extended Features

### Add More Trading Pairs
Modify `SYMBOL` configuration in `config.py`, or create multiple instances

### Add Database Storage
Integrate Redis or PostgreSQL to persist historical data

### Add Monitoring Alerts
Integrate Prometheus and Grafana for monitoring

### Add Web Interface
Create frontend interface to visualize order book data
