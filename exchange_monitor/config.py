import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL must be set in .env file")

# Exchange hot wallet addresses to monitor
ETH_ADDRESSES = [
    "0x28C6c06298d514Db089934071355E5743bf21d60",  # Binance 14
    "0xDFd5293D8e347dFe59E90eFd55b2956a1343963d",  # Binance 16, usually 14 - > 16
    "0x56Eddb7aa87536c09CCc2793473599fD21A8b17F",  # Binance 17 withdraw wallet
    "0xE69f81b825d7Dc31ee9becef4DbEab5cf30e3Abb",  # Biance large deposit account
    "bc1q8s3h3vw5xufdas890q29lpuca56r0ezqar0mvs",  # Cumberland DRW
    "0xCD531Ae9EFCCE479654c4926dec5F6209531Ca7b",  # Coinbase Hot Wallet
    "0xceB69F6342eCE283b2F5c9088Ff249B5d0Ae66ea",  # Coinbase Hot Wallet
    "0xf89d7b9c864f589bbF53a82105107622B35EaA40",  # Bybit Hot Wallet
    "0x4E5B2e1dc63F6b91cb6Cd759936495434C7e972F",  # Fixedfloat Hot Wallet
    "0x267be1C1D684F78cb4F6a176C4911b741E4Ffdc0",  # Kraken Hot Wallet
    "0x8D371bC560246Dc632C4e707707d85d2E568A832",  # OKX Hot Wallet
    "0xd01607c3C5eCABa394D8be377a08590149325722",  # Aave Hot Wallet
    "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",  # Aave Hot Wallet
]

# Token addresses
USDT_TOKEN = "0xdAC17F958D2ee523a2206206994597C13D831ec7"  # Bitfinex

# API configuration
BLOCKSCOUT_BASE_URL = "https://eth.blockscout.com/"

# Monitoring configuration
MONITOR_INTERVAL = 60  # seconds
MIN_ETH_DELTA = 100  # minimum ETH delta to track
TOR_PROXY_HOST = os.getenv("TOR_PROXY_HOST", "tor")
TOR_PROXY_PORT = int(os.getenv("TOR_PROXY_PORT", "9050"))

#
