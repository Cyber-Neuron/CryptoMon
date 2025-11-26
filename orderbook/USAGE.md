# 快速开始指南

## 1. 安装依赖

```bash
cd orderbook
pip install -r requirements.txt
```

## 2. 启动系统

### 方法1：使用简化启动脚本（推荐）
```bash
./start_simple.sh
```

### 方法2：使用完整启动脚本
```bash
./start.sh
```

### 方法3：直接运行
```bash
python localorderbok.py
```

系统启动后会：
- 连接到Binance WebSocket
- 获取初始深度快照
- 启动API服务器（端口8000）
- 开始维护本地order book

## 3. 测试系统

### 运行测试脚本
```bash
python test_orderbook.py
```

### 运行客户端示例
```bash
python client_example.py
```

### 运行最近档位演示
```bash
python demo_nearest_level.py
```

## 4. API使用示例

### 查询特定价格的持仓量差值
```bash
# 查询最近档位（不传入时间戳）
curl -X POST "http://localhost:8000/quantity" \
     -H "Content-Type: application/json" \
     -d '{"price": 50000.0}'

# 查询历史数据（传入时间戳）
curl -X POST "http://localhost:8000/quantity" \
     -H "Content-Type: application/json" \
     -d '{"price": 50000.0, "timestamp": 1703123456}'
```

### 获取最近档位信息
```bash
curl "http://localhost:8000/nearest-level/50000.0"
```

### 获取系统状态
```bash
curl "http://localhost:8000/status"
```

### 获取当前order book
```bash
curl "http://localhost:8000/orderbook"
```

## 5. 配置修改

编辑 `config.py` 文件来修改配置：

```python
# 修改交易对
SYMBOL = "ETHUSDT"  # 改为其他交易对

# 修改API端口
API_PORT = 8080  # 改为其他端口

# 修改历史数据保留时间
HISTORY_RETENTION_HOURS = 12  # 改为12小时
```

## 6. 监控和调试

### 查看日志
系统会输出详细的日志信息，包括：
- WebSocket连接状态
- 事件处理情况
- 错误信息

### 检查系统状态
访问 `http://localhost:8000/status` 查看：
- 连接状态
- 数据统计
- 历史快照数量

## 7. 常见问题

### Q: WebSocket连接失败
A: 检查网络连接，确保能访问Binance API

### Q: API无响应
A: 确认系统已启动，检查端口是否被占用

### Q: 数据不准确
A: 等待系统收集足够的历史数据，检查时间戳同步

### Q: 内存使用过高
A: 减少历史数据保留时间（修改 `HISTORY_RETENTION_HOURS`）

### Q: 程序无法正常退出
A: 
- 使用 `./start.sh` 启动脚本（推荐）
- 按 `Ctrl+C` 后等待几秒钟让程序优雅关闭
- 如果仍然无法退出，使用 `kill -9 <进程ID>` 强制终止
- 运行 `python test_shutdown.py` 测试信号处理功能

## 8. 性能优化

### 减少内存使用
- 降低历史数据保留时间
- 减少快照保存频率

### 提高响应速度
- 使用SSD存储
- 增加系统内存
- 优化网络连接

## 9. 生产环境部署

### 使用进程管理器
```bash
# 使用PM2
npm install -g pm2
pm2 start localorderbok.py --name orderbook

# 使用Supervisor
# 创建配置文件 /etc/supervisor/conf.d/orderbook.conf
```

### 使用Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "localorderbok.py"]
```

### 反向代理配置
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

## 10. 扩展功能

### 添加更多交易对
修改 `config.py` 中的 `SYMBOL` 配置，或创建多个实例

### 添加数据库存储
集成Redis或PostgreSQL来持久化历史数据

### 添加监控告警
集成Prometheus和Grafana进行监控

### 添加Web界面
创建前端界面来可视化order book数据 