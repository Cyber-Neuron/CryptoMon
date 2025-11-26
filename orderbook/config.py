"""
Order Book系统配置文件
"""

# 交易对配置
SYMBOL = "ETHUSDT"  # 交易对符号
SYMBOL_LOWER = SYMBOL.lower()  # 小写形式

# WebSocket配置
WEBSOCKET_URI = f"wss://fstream.binance.com/stream?streams={SYMBOL_LOWER}@depth"
SNAPSHOT_URL = f"https://fapi.binance.com/fapi/v1/depth?symbol={SYMBOL}&limit=1000"

# API服务器配置
API_HOST = "0.0.0.0"
API_PORT = 8000

# 历史数据配置
HISTORY_RETENTION_HOURS = 24  # 历史数据保留时间（小时）
HISTORY_RETENTION_SECONDS = HISTORY_RETENTION_HOURS * 3600  # 转换为秒

# 日志配置
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# 重连配置
RECONNECT_DELAY = 5  # WebSocket重连延迟（秒）

# 性能配置
MAX_HISTORY_SNAPSHOTS = 86400  # 最大历史快照数量（24小时 * 3600秒）
