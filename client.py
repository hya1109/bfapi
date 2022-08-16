
from urllib.parse import urlencode
import collections
import time
import hmac
import hashlib
from enum import Enum

from datetime import datetime, timedelta

from rest.rest_client import RequestStatus, RestClient

REST_HOST = "https://api.bitforex.com"

class BitforexRestApi(RestClient):
    def __init__(self):
        """"""
        super(BitforexRestApi, self).__init__()
        self.key = ""
        self.secret = ""

    
    def connect(
        self,
        key: str,
        secret: str,
        session: int,
        proxy_host: str,
        proxy_port: int,
    ):
        """
        Initialize connection to REST server.
        """
        self.key = key
        self.secret = secret.encode()

        self.connect_time = (
            int(datetime.now().strftime("%y%m%d%H%M%S"))
        )

        self.init(REST_HOST, proxy_host, proxy_port)
        self.start(session)
        self.write_log("REST API start success")

    def sign(self, request):
        """
        Generate Bitforex signature.
        """
        # Sign
        nonce = str(int(round(time.time() * 1000)))

        if not request.data:
            request.data = {}
            
        body = urlencode({'accessKey': self.key})
        request.data["nonce"] = nonce
        body += "&" + urlencode(collections.OrderedDict(sorted(request.data.items(), key=lambda t:t[0])))
        
        if 'orderIds=' in body or 'ordersData=' in body:
            body = body.replace('%2C', ',')
            body = body.replace('%5B', '[')
            body = body.replace('%5D', ']')
            body = body.replace('%7B', '{')
            body = body.replace('%22', '\'')
            body = body.replace('%3A', ':')
            body = body.replace('%7D', '}')
            body = body.replace('+', ' ')
            
        msg = request.path + "?" + body
        
        #print("msg:" + msg)
        
        signature = hmac.new(
            self.secret, msg.encode("utf8"), digestmod=hashlib.sha256
        ).hexdigest()      
        
        body += "&signData=" + signature
        #print("body:" + body)
        
        if request.method == "POST":
            request.data = body
        else:
            request.params = body
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        
        request.headers = headers
        return request
    
      
    def write_log(self, logmsg):
        print(logmsg) 

    def query_contract(self):
        """"""
        return self.send_request_sync(
            method="GET",
            path="/api/v1/market/symbols"
        )   

    def query_ticker_sync(self, symbol):
        data = {
            "symbol":symbol,
            "state":0         
        }

        request, response = self.send_request_sync(
            "GET",
            "/api/v1/market/ticker",
            data=data
        )
        if request.status == RequestStatus.success:
            if response['success']:
                return response, 0
            else:
                self.write_log(f"query {symbol} ticker error:" + response['code'] + "-" + response['message'])
                return {}, -1
        else:
            self.write_log(f"query {symbol} ticker failed:" + str(response))
            return {}, -1  
    

    def query_depth_sync(self, symbol, size = 10):
        data = {
            "symbol":symbol,
            "size":size,
            "state":0         
        }

        request, response = self.send_request_sync(
            "GET",
            "/api/v1/market/depth",
            data=data
        )
        if request.status == RequestStatus.success:
            if response['success']:
                return response, 0
            else:
                self.write_log(f"query {symbol} depth error:" + response['code'] + "-" + response['message'])
                return {}, -1
        else:
            self.write_log(f"query {symbol} depth failed:" + str(response))
            return {}, -1  
    

    def query_trades_sync(self, symbol, size):
        data = {
            "symbol":symbol,
            "size":size,
            "state":0         
        }

        request, response = self.send_request_sync(
            "GET",
            "/api/v1/market/trades",
            data=data
        )
        if request.status == RequestStatus.success:
            if response['success']:
                return response, 0
            else:
                self.write_log(f"query {symbol} trades error:" + response['code'] + "-" + response['message'])
                return {}, -1
        else:
            self.write_log(f"query {symbol} trades failed:" + str(response))
            return {}, -1  
  

    
    def query_all_open_orders_sync(self, symbol):
        data = {
            "symbol":symbol,
            "state":0         
        }

        request, response = self.send_request_sync(
            "POST",
            "/api/v1/trade/orderInfos",
            data=data
        )
        if request.status == RequestStatus.success:
            if response['success']:
                return response, 0
            else:
                self.write_log(f"query {symbol} all open order error:" + response['code'] + "-" + response['message'])
                return {}, -1
        else:
            self.write_log(f"query {symbol} all open order failed:" + str(response))
            return {}, -1  
    

    
