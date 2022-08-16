from time import sleep
from client import BitforexRestApi

bitforexapi = BitforexRestApi()
bitforexapi.connect("xx", "xxx", 3,"", "")

###print(bitforexapi.query_contract())
print(bitforexapi.query_ticker_sync("coin-usdt-eth"))
print(bitforexapi.query_depth_sync("coin-usdt-eth", 1))
print(bitforexapi.query_trades_sync("coin-usdt-eth", 1))

print(bitforexapi.query_all_open_orders_sync("coin-usdt-eth"))

 