# Troubleshooting Guide

## Common Issues

### 1. Ctrl+C Cannot Exit Program Normally

**Problem Description**: After pressing Ctrl+C, the program cannot exit normally and needs to be force terminated.

**Root Cause Analysis**: 
- Async tasks don't properly handle signals
- WebSocket connection doesn't close gracefully
- Main loop doesn't respond to interrupt signals
- Using traditional signal handling in async environment

**Solutions**:

#### Method 1: Use Simplified Startup Script (Recommended)
```bash
./start_simple.sh
```
The simplified startup script runs the Python program directly, signals are passed directly to the Python process.

#### Method 2: Run Program Directly
```bash
python localorderbok.py
```
The program has now fixed signal handling issues in async environment, press Ctrl+C and wait a few seconds to exit normally.

#### Method 3: Use Original Startup Script
```bash
./start.sh
```
The original startup script waits for process response, automatically force terminates if no response within 10 seconds.

#### Method 4: Force Terminate
If the program still cannot exit, you can use the following command to force terminate:
```bash
# Find Python process
ps aux | grep localorderbok.py

# Force terminate process
kill -9 <process_id>
```

### 2. Test Signal Handling Functionality

Run test script to verify signal handling works normally:
```bash
python test_shutdown.py
```

This script starts a simple async task, press Ctrl+C to test if it can exit normally.

### 3. Signal Handling Mechanism

The program now uses the following mechanism to handle signals:

1. **Signal Registration**: Register SIGINT (Ctrl+C) and SIGTERM signal handlers
2. **Graceful Shutdown**: Set shutdown event, notify all async tasks to stop
3. **WebSocket Close**: Wait for WebSocket connection to close normally
4. **Timeout Protection**: Set 5 second timeout to prevent program from hanging

### 4. Log Information

The program will output the following log information to console:
```
INFO - Received signal 2, initiating graceful shutdown...
INFO - Received shutdown signal, closing WebSocket...
INFO - WebSocket connection closed due to shutdown signal
INFO - Shutting down gracefully...
INFO - Shutdown complete
```

### 5. Startup Script Advantages

Advantages of using `./start.sh` startup script:

- **Signal Handling**: Automatically handles Ctrl+C signals
- **Process Management**: Properly manages Python processes
- **Cleanup Mechanism**: Ensures program completely exits
- **Error Handling**: Handles various exception cases

### 6. Development Environment Debugging

In development environment, you can use the following methods to debug:

```bash
# Enable verbose logging
export PYTHONPATH=.
python -u localorderbok.py

# Use pdb debugger
python -m pdb localorderbok.py
```

### 7. Production Environment Deployment

In production environment, it's recommended to use process managers:

```bash
# Use PM2
pm2 start localorderbok.py --name orderbook

# Use Supervisor
# Create config file /etc/supervisor/conf.d/orderbook.conf
```

### 8. Common Error Messages

#### "Address already in use"
Port is occupied, solution:
```bash
# Find process occupying port
lsof -i :8000

# Terminate process
kill -9 <process_id>
```

#### "Connection refused"
WebSocket connection failed, solution:
- Check network connection
- Confirm Binance API availability
- Check firewall settings

#### "Module not found"
Missing dependency packages, solution:
```bash
pip install -r requirements.txt
```

## Contact Support

If you encounter other issues, please:

1. Check log output
2. Run test scripts
3. Check system environment
4. Refer to official documentation
