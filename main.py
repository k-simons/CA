import requests
from graph import Graph
from node import Node
from edge import Edge, TickerInfo
from encodeRequest import generateApiKeyAndSignature
from cycleChecker import CycleChecker
import time
import os

base = "https://api.binance.com"
info = base + "/api/v1/exchangeInfo"
depth = base + "/api/v1/depth"
extraDepthExample = depth + "?symbol=BNBBTC"
ticket =    base + "/api/v1/ticker/24hr"
tickerPrice = base + "/api/v3/ticker/price"
makeOrder = base + "/api/v3/order"
makeFakeOrder = base + "/api/v3/order/test"


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

def ohShit(edge):
    startQuantity = .01
    r = makeTradeFromEdge(edge, startQuantity)
    print(" REQUEST JSON: ")
    print(r)
    print(r.json())

def makeTradeFromEdge(edge, quantity):
    print(edge.tickerInfo)
    exit(1)
    timestamp = int(round(time.time() * 1000))
    side = "BUY" if edge.tickerInfo.buy else "SELL"
    data = {
        "symbol": edge.tickerInfo.symbol,
        "side": side,
        "type": "MARKET",
        "quantity": quantity,
        "timestamp": timestamp,
    }
    return makeRequestFromDataBlob(data)

def makeRequestFromDataBlob(data):
    body = ""
    for key, value in data.items():
        body = body + key + "=" + str(value) + "&"
    body = body[:-1]
    tup = generateApiKeyAndSignature(body, "../keys.json")
    headers = {"X-MBX-APIKEY": tup[0]}
    makeOrderFinal = makeOrder + "?" + body + "&signature=" + tup[1]
    print("FINAL ORDER STRING")
    print(makeOrderFinal)
    return requests.post(makeOrderFinal, headers=headers)

def main():
    doIt()

if __name__ == "__main__": main()
