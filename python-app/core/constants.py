"""Bitcoin network and monitoring constants."""

# Bitcoin network constants
MAGIC_MAINNET = bytes.fromhex("f9beb4d9")
PROTOCOL_VERSION = 70016

# Monitoring thresholds
LARGE_TX_THRESHOLD_BTC = 100  # 100 BTC threshold for whale detection
ARBITRAGE_THRESHOLD_BTC = 5  # 5 BTC threshold for arbitrage signals
MEMPOOL_SIZE_THRESHOLD = 1000  # Mempool size threshold for arbitrage signals

# Tor proxy configuration
TOR_PROXY = "socks5h://127.0.0.1:9050"
PROXY_HOST = TOR_PROXY.split("://")[1].split(":")[0]
PROXY_PORT = int(TOR_PROXY.split(":")[-1])
