# 更新日志

## v1.1.0 - 最近档位功能

### 新增功能
- ✨ 添加最近档位查询功能
- ✨ 支持不传入时间戳时返回当前时间最近档位
- ✨ 新增 `/nearest-level/{price}` API接口
- ✨ 增强 `/quantity` API，支持可选时间戳参数

### 修复问题
- 🐛 修复Ctrl+C无法正常退出的问题
- 🐛 添加优雅关闭机制
- 🐛 改进信号处理逻辑
- �� 优化WebSocket连接关闭流程
- 🐛 修复异步环境中的信号处理问题
- 🐛 添加简化启动脚本，解决shell脚本信号传递问题

### 功能说明
1. **最近档位查询**: 当查询的价格不存在时，系统会返回离该价格最近的一档价格和数量
2. **智能价格匹配**: 系统会在bids和asks中寻找距离最小的价格
3. **价格差值计算**: 返回最近档位与目标价格的距离
4. **实时数据**: 不传入时间戳时返回当前实时数据
5. **优雅关闭**: 支持Ctrl+C正常退出，等待WebSocket连接关闭

### API变更
- `POST /quantity` 现在支持可选的时间戳参数
- 新增 `GET /nearest-level/{price}` 接口
- 响应格式增加了 `actual_price` 和 `is_nearest_level` 字段

### 使用示例
```bash
# 查询最近档位（不传入时间戳）
curl -X POST "http://localhost:8000/quantity" \
     -H "Content-Type: application/json" \
     -d '{"price": 50000.0}'

# 查询最近档位API
curl "http://localhost:8000/nearest-level/50000.0"
```

### 文件变更
- `localorderbok.py`: 添加最近档位查询逻辑和信号处理
- `test_orderbook.py`: 更新测试用例
- `client_example.py`: 更新客户端示例
- `demo_nearest_level.py`: 新增演示脚本
- `test_shutdown.py`: 新增信号处理测试脚本
- `start.sh`: 改进启动脚本，添加信号处理
- `README.md`: 更新文档
- `USAGE.md`: 更新使用说明

## v1.0.0 - 初始版本

### 基础功能
- 🔄 实时WebSocket连接
- 📊 本地Order Book维护
- 🕒 历史数据存储
- 🌐 REST API服务
- 📈 持仓量差值计算 