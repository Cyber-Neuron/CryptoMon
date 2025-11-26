# 期货交易数据分析程序配置

# API配置
LOCAL_API_BASE_URL = "http://localhost:8000"
WEBSOCKET_URL = "wss://fstream.binance.com/ws/ethusdt@aggTrade"  # 改为小写
SYMBOL = "ETHUSDT"

# 交易分析配置
MIN_QUANTITY_THRESHOLD = 10.0  # 最小交易数量阈值
ANALYSIS_WINDOW_SECONDS = 5  # 分析时间窗口（秒）
PRICE_TOLERANCE = 0.1  # 价格容差（百分比）

# 缓冲区配置
BUFFER_SIZE = 100  # 交易缓冲区大小
ANALYSIS_INTERVAL = 1.0  # 分析间隔（秒）
STATS_INTERVAL = 10  # 统计信息打印间隔（秒）

# 日志配置
LOG_LEVEL = "INFO"  # 设置为DEBUG级别以显示详细信息
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%H:%M:%S"

# WebSocket配置
RECONNECT_DELAY = 5  # 重连延迟（秒）
CONNECTION_TIMEOUT = 30  # 连接超时（秒）

# API调用配置
API_TIMEOUT = 5  # API调用超时（秒）
MAX_RETRIES = 3  # 最大重试次数

# 显示配置
ENABLE_COLORS = True  # 启用颜色显示
SHOW_DETAILED_ANALYSIS = True  # 显示详细分析
SHOW_STATISTICS = True  # 显示统计信息

# 调试配置
DEBUG_MODE = True  # 启用调试模式
DEBUG_MESSAGE_LIMIT = 200  # 调试消息显示长度限制
DEBUG_MESSAGE_COUNT = 5  # 测试时接收的消息数量
