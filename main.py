import requests
from graph import Graph
from node import Node
from edge import Edge, TickerInfo
from encodeRequest import createFullUrlAndHeaders
from cycleChecker import CycleChecker
import time
import os

base = "https://api.binance.com"
info = base + "/api/v1/exchangeInfo"
depth = base + "/api/v1/depth"
extraDepthExample = depth + "?symbol=BNBBTC"
ticket =    base + "/api/v1/ticker/24hr"
tickerPrice = base + "/api/v3/ticker/price"
getTrades = base + "/api/v3/myTrades"
getOrder = base + "/api/v3/order"
getAccountInfo = base + "/api/v3/account"
getOpenOrders = base + "/api/v3/openOrders"
makeOrder = base + "/api/v3/order"
makeFakeOrder = base + "/api/v3/order/test"

# Get account info
def getAccountBalanace():
    data = {}
    (fullString, headers) = createFullUrlAndHeaders(getAccountInfo, data)
    accountInfo = requests.get(fullString, headers=headers).json()
    balances = accountInfo["balances"]
    balancesWithMoney = [balance for balance in balances if float(balance["free"]) > 0 or float(balance["locked"]) > 0]
    print(balancesWithMoney)

# Get trades
def getPastTrades(symbol):
    data = {
        "symbol": symbol,
        "limit": 5
    }
    (fullString, headers) = createFullUrlAndHeaders(getTrades, data)
    print(fullString)
    print(requests.get(fullString, headers=headers).json())

# Get open orders
def getOpenOrder(symbol):
    data = {
        "symbol": symbol,
    }
    (fullString, headers) = createFullUrlAndHeaders(getOpenOrders, data)
    print(requests.get(fullString, headers=headers).json())

# Bleh same response after making purchase
def getUserOrder(symbol, orderId):
    data = {
        "symbol": symbol,
        "orderId": orderId,
    }
    (fullString, headers) = createFullUrlAndHeaders(getOrder, data)
    print(requests.get(fullString, headers=headers).json())

def generateBinanceGraph():
    ## Do this first so the market is most up to date
    infoResponse = requests.get(info).json()
    # Then get market data
    prices = requests.get(tickerPrice).json()
    # {'symbol': 'ETHBTC', 'price': '0.09017900'} array of current prices
    pricesDict = {}
    for price in prices:
        pricesDict[price["symbol"]] = price["price"]
    ## great have a dict, now lets creates 2 edges per ticker
    edges = []
    nodeDict = {}
    for symbol in infoResponse["symbols"]:
        ticker = symbol["symbol"]
        startAsset = symbol["baseAsset"]
        goingAsset = symbol["quoteAsset"]
        nodeDict[startAsset] = True
        nodeDict[goingAsset] = True
        edge = Edge(
            TickerInfo(ticker, False),
            startAsset,
            goingAsset,
            float(pricesDict[ticker])
        )
        edgeInverse = Edge(
            TickerInfo(ticker, True),
            goingAsset,
            startAsset,
            1 / float(pricesDict[ticker]),
        )
        edges.append(edge)
        edges.append(edgeInverse)
    nodes = []
    for key in nodeDict:
        nodes.append(Node(key))
    return Graph(nodes, edges)

def getCurrentBestPath(cycleChecker):
    mList = []
    nodes = [Node("ETH")]
    for node in nodes:
        test = cycleChecker.checkCycles(3, node)
        mList.extend(test)
    maxResult = mList[0]
    for m in mList:
        if m.units > maxResult.units:
            maxResult = m
    return maxResult

def doIt():
    graph = generateBinanceGraph()
    cycleChecker = CycleChecker(graph)
    maxResult = getCurrentBestPath(cycleChecker)
    print(maxResult.units)
    edges = maxResult.edgePath
    for edge in edges:
        print(edge)
    if maxResult.units > 1.01  :
        # will not do unless .1% gain
        print("ENGAGED")
        ohShit(edges[0])
    else:
        print("TOO LOW")

def doAllTrades(edges):
    startQuantity = .01
    for edge in edges:
        print(edge)

def ohShit(edge):
    startQuantity = .01
    r = makeTradeFromEdge(edge, startQuantity)
    print(" REQUEST JSON: ")
    print(r)
    print(r.json())

def makeTradeFromEdge(edge, quantity):
    print(edge.tickerInfo)
    exit(1)
    data = {
        "symbol": edge.tickerInfo.symbol,
        "side": "BUY" if edge.tickerInfo.buy else "SELL",
        "type": "MARKET",
        "quantity": quantity,
    }
    return makeRequestFromDataBlob(data)

def makeRequestFromDataBlob(data):
    (fullString, headers) = createFullUrlAndHeaders(makeOrder, data)
    print("FINAL STRING")
    print(fullString)
    exit(1)
    return requests.post(fullString, headers=headers)


def main():
    getAccountBalanace()

if __name__ == "__main__": main()
