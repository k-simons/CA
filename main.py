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
    return requests.get(fullString, headers=headers).json()

def calculateNewBalanceToSee(symbol, orderId):
    resultArray = getPastTrades(symbol)
    order = next(result for result in resultArray if result["orderId"] == orderId)
    ## Now that we have the order, we take the qty and multiple by price
    newQuantity = float(order["qty"]) * float(order["price"])
    ## Then subtract commision
    amountToTradeLarge = newQuantity - float(order["commission"])
    ## Round to useful value
    amountToTrade = amountToTradeLarge
    return amountToTrade

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
    stepSizeLookUp = {}
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

        for filterSet in symbol["filters"]:
            if "minQty" in filterSet:
                stepSizeLookUp[ticker] = float(filterSet["minQty"])

    nodes = []
    for key in nodeDict:
        nodes.append(Node(key))
    return (Graph(nodes, edges), stepSizeLookUp)

def getCurrentBestPath(cycleChecker):
    cycleResults = []
    nodes = [Node("ETH")]
    for node in nodes:
        test = cycleChecker.checkCycles(3, node)
        cycleResults.extend(cycleChecker.checkCycles(3, node))
    units = .109
    hmm = -1
    bestCycleResult = None
    for cycleResult in cycleResults:
        resultOfTrading = cycleResult.getTradesAndEmitAndDust(units)
        if resultOfTrading["valid"] == True and resultOfTrading["endUnits"] > hmm:
            bestCycleResult = cycleResult
            hmm = resultOfTrading["endUnits"]
    print("      ")
    print("      ")
    print("      ")
    lol = bestCycleResult.getTradesAndEmitAndDust(units)
    for edge in bestCycleResult.edgePath:
        print(edge)
    print(lol)

def doIt():
    (graph, stepSizeLookUp) = generateBinanceGraph()
    cycleChecker = CycleChecker(graph, stepSizeLookUp)
    getCurrentBestPath(cycleChecker)
    #exit(1)
    #print(maxResult.units)
    #edges = maxResult.edgePath
    #for edge in edges:
    #    print(edge)
    #if maxResult.units > 1.01  :
    #    # will not do unless .1% gain
    #    print("ENGAGED")
    #    doAllTrades(edges)
    #else:
    #    print("TOO LOW")

def doAllTrades(edges):
    startQuantity = .05
    for edge in edges:
        requestJson = makeTradeFromEdge(edge, startQuantity).json()
        print(requestJson)
        symbol = requestJson["symbol"]
        orderId = requestJson["orderId"]
        startQuantity = calculateNewBalanceToSee(symbol, orderId)
        print(startQuantity)

def makeTradeFromEdge(edge, quantity):
    print(edge.tickerInfo)
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
    return requests.post(fullString, headers=headers)


def main():
    doIt()



if __name__ == "__main__": main()
