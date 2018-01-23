import requests

from encodeRequest import createFullUrlAndHeaders

base = "https://api.binance.com"
exchangeInfo = base + "/api/v1/exchangeInfo"
depth = base + "/api/v1/depth"
extraDepthExample = depth + "?symbol=BNBBTC"
ticket = base + "/api/v1/ticker/24hr"
tickerPrice = base + "/api/v3/ticker/price"
getTrades = base + "/api/v3/myTrades"
getOrder = base + "/api/v3/order"
getAccountInfo = base + "/api/v3/account"
getOpenOrders = base + "/api/v3/openOrders"
makeOrder = base + "/api/v3/order"
makeFakeOrder = base + "/api/v3/order/test"

class BinanceClient:

    # Response, see allSymbolOutput.json
    def getExchangeInfo(self):
        return self.makeUnAuthedGetRequest(exchangeInfo)

    # Current market prices
    # Response is Map<String, Float> from ticker to price
    def getAllTickerPrices(self):
        prices = self.makeUnAuthedGetRequest(tickerPrice)
        # {'symbol': 'ETHBTC', 'price': '0.09017900'} array of current prices
        pricesDict = {}
        for price in prices:
            pricesDict[price["symbol"]] = float(price["price"])
        return pricesDict

    # Get account balances for every currency
    # [{'asset': 'BTC', 'free': '10.0', 'locked': '10.0'}...], for every single currency
    def getAccountBalanaces(self):
        accountInfo = self.makeAuthedGetRequest(getAccountInfo, {})
        balances = accountInfo["balances"]
        return balances

    # Get account balances for every currency that is non-zero
    # [{'asset': 'BTC', 'free': '10.0', 'locked': '10.0'}...], for every single currency
    def getNoneEmptyAccountBalanaces(self):
        balances = self.getAccountBalanaces()
        balancesWithMoney = [balance for balance in balances if float(balance["free"]) > 0 or float(balance["locked"]) > 0]
        return balancesWithMoney

    # Get last trade with order Id, or error
    # A bit awkward, but api gurantee is that given a symbol and orderId, ensure the last order matches and return details, or error out
    # Repsonse, see pastTradesResults.jsons
    def getLastTradeWithOrderId(self, symbol, orderId):
        resultArray = self.getNPastTrades(symbol, 1)
        order = next(result for result in resultArray if result["orderId"] == orderId)
        return order

    # Get trades
    # Response [{'id': 25101471, 'orderId': 60945946, 'price': '0.09159100', 'qty': '0.01000000', 'commission': '0.00000092', 'commissionAsset': 'BTC', 'time': 1516681362439, 'isBuyer': False, 'isMaker': False, 'isBestMatch': True}]
    # Most recent trade is last
    def getNPastTrades(self, symbol, limit):
        data = {
            "symbol": symbol,
            "limit": limit
        }
        return self.makeAuthedGetRequest(getTrades, data)

    ## ACTUAL TRADE ENDPOINT ##
    def makeTradeFromEdge(self, edge, quantity):
        data = {
            "symbol": edge.tickerInfo.symbol,
            "side": "BUY" if edge.tickerInfo.buy else "SELL",
            "type": "MARKET",
            "quantity": quantity,
        }
        return self.makePostRequest(makeOrder, data)


    # Not useful, but already implemented

    # Get open orders
    def getOpenOrder(self, symbol):
        data = { "symbol": symbol }
        return self.makeAuthedGetRequest(getOpenOrders, data)

    # Bleh same response after making purchase
    def getUserOrder(self, symbol, orderId):
        data = {
            "symbol": symbol,
            "orderId": orderId,
        }
        return self.makeAuthedGetRequest(getOrder, data)

    def makeUnAuthedGetRequest(self, url):
        request = requests.get(url)
        return self.turnSuccessfulRequestToJsonOrError(request)

    def makeAuthedGetRequest(self, url, data):
        (fullString, headers) = createFullUrlAndHeaders(url, data)
        request = requests.get(fullString, headers=headers)
        return self.turnSuccessfulRequestToJsonOrError(request)

    def makePostRequest(self, url, data):
        (fullString, headers) = createFullUrlAndHeaders(url, data)
        request = requests.post(fullString, headers=headers)
        return self.turnSuccessfulRequestToJsonOrError(request)

    def turnSuccessfulRequestToJsonOrError(self, response):
        if response.status_code == 200:
            ## Worked, return the json
            return response.json()
        else:
            ## Print the world
            print(response.headers)
            print(response.url)
            print(response.json())
            ## And bail right away
            raise Exception('Request failed!')
