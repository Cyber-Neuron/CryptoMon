from decimal import Decimal

from web3 import Web3

w3 = Web3(
    Web3.HTTPProvider("https://ethereum-rpc.publicnode.com")
)  # 或 Infura、Alchemy 等

USDC_ADDRESS = (
    "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"  # 以太坊主网上 USDC 合约地址
)
USDT_ADDRESS = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
ERC20_ABI = '[{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"type":"function"}]'

usdc_contract = w3.eth.contract(address=USDC_ADDRESS, abi=ERC20_ABI)
usdt_contract = w3.eth.contract(address=USDT_ADDRESS, abi=ERC20_ABI)

wallet = "0x28C6c06298d514Db089934071355E5743bf21d60"
block_number = w3.eth.block_number - 50  # 10分钟前的安全区块

usdc_balance = usdc_contract.functions.balanceOf(wallet).call(
    block_identifier=block_number
) / Decimal("1e6")
usdt_balance = usdt_contract.functions.balanceOf(wallet).call(
    block_identifier=block_number
) / Decimal("1e6")
print(usdc_balance)
print(usdt_balance)
