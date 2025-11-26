curl https://eth.tinynn.com/v1/mainnet \
-X POST \
-H 'Content-Type: application/json' \
-H 'authorization: Bearer VRiK2mIl27hmIEW1kdJyd-VRvMuUgy8wnIHQqGdG' \
--data '
  {
    "jsonrpc":"2.0",
    "method":"eth_getBalance",
    "params":[ "0xB38e8c17e38363aF6EbdCb3dAE12e0243582891D","latest"],
  "id": 1
}'
