import requests

url = "https://www.deribit.com/api/v2/public/ticker"
params = {"instrument_name": "ETH-11JUL25-2600-C"}
url = "https://www.deribit.com/api/v2/public/get_last_trades_by_instrument"
params = {"instrument_name": "ETH-11JUL25-2700-C", "count": 100}
res = requests.get(url, params=params).json()
print(res["result"])
