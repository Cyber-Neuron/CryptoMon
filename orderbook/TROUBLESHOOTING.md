# 故障排除指南

## 常见问题

### 1. Ctrl+C 无法正常退出程序

**问题描述**: 按下 Ctrl+C 后程序无法正常退出，需要强制终止。

**原因分析**: 
- 异步任务没有正确处理信号
- WebSocket连接没有优雅关闭
- 主循环没有响应中断信号
- 在异步环境中使用传统的信号处理方式

**解决方案**:

#### 方法1：使用简化启动脚本（推荐）
```bash
./start_simple.sh
```
简化启动脚本直接运行Python程序，信号会直接传递给Python进程。

#### 方法2：直接运行程序
```bash
python localorderbok.py
```
现在程序已经修复了异步环境中的信号处理问题，按 Ctrl+C 后等待几秒钟即可正常退出。

#### 方法3：使用原启动脚本
```bash
./start.sh
```
原启动脚本会等待进程响应，如果10秒内没有响应会自动强制终止。

#### 方法4：强制终止
如果程序仍然无法退出，可以使用以下命令强制终止：
```bash
# 查找Python进程
ps aux | grep localorderbok.py

# 强制终止进程
kill -9 <进程ID>
```

### 2. 测试信号处理功能

运行测试脚本验证信号处理是否正常工作：
```bash
python test_shutdown.py
```

这个脚本会启动一个简单的异步任务，按 Ctrl+C 测试是否能正常退出。

### 3. 信号处理机制

程序现在使用以下机制处理信号：

1. **信号注册**: 注册 SIGINT (Ctrl+C) 和 SIGTERM 信号处理器
2. **优雅关闭**: 设置关闭事件，通知所有异步任务停止
3. **WebSocket关闭**: 等待WebSocket连接正常关闭
4. **超时保护**: 设置5秒超时，防止程序卡死

### 4. 日志信息

程序会在控制台输出以下日志信息：
```
INFO - Received signal 2, initiating graceful shutdown...
INFO - Received shutdown signal, closing WebSocket...
INFO - WebSocket connection closed due to shutdown signal
INFO - Shutting down gracefully...
INFO - Shutdown complete
```

### 5. 启动脚本的优势

使用 `./start.sh` 启动脚本的优势：

- **信号处理**: 自动处理 Ctrl+C 信号
- **进程管理**: 正确管理Python进程
- **清理机制**: 确保程序完全退出
- **错误处理**: 处理各种异常情况

### 6. 开发环境调试

在开发环境中，可以使用以下方法调试：

```bash
# 启用详细日志
export PYTHONPATH=.
python -u localorderbok.py

# 使用pdb调试
python -m pdb localorderbok.py
```

### 7. 生产环境部署

在生产环境中，建议使用进程管理器：

```bash
# 使用PM2
pm2 start localorderbok.py --name orderbook

# 使用Supervisor
# 创建配置文件 /etc/supervisor/conf.d/orderbook.conf
```

### 8. 常见错误信息

#### "Address already in use"
端口被占用，解决方案：
```bash
# 查找占用端口的进程
lsof -i :8000

# 终止进程
kill -9 <进程ID>
```

#### "Connection refused"
WebSocket连接失败，解决方案：
- 检查网络连接
- 确认Binance API可用性
- 查看防火墙设置

#### "Module not found"
依赖包缺失，解决方案：
```bash
pip install -r requirements.txt
```

## 联系支持

如果遇到其他问题，请：

1. 查看日志输出
2. 运行测试脚本
3. 检查系统环境
4. 参考官方文档 