import requests
from graph import Graph
from node import Node
from edge import Edge
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
makeFakeOrder = base + "/api/v3/order/test"


def generateBinanceGraph():
    prices = requests.get(tickerPrice).json()
    # {'symbol': 'ETHBTC', 'price': '0.09017900'} array of current prices
    pricesDict = {}
    for price in prices:
        pricesDict[price["symbol"]] = price["price"]
    ## great have a dict, now lets creates 2 edges per ticker
    infoResponse = requests.get(info).json()
    edges = []
    nodeDict = {}
    for symbol in infoResponse["symbols"]:
        ticker = symbol["symbol"]
        startAsset = symbol["baseAsset"]
        goingAsset = symbol["quoteAsset"]
        nodeDict[startAsset] = True
        nodeDict[goingAsset] = True
        edge = Edge(startAsset, goingAsset, float(pricesDict[ticker]))
        edgeInverse = Edge(goingAsset, startAsset, 1 / float(pricesDict[ticker]))
        edges.append(edge)
        edges.append(edgeInverse)
    nodes = []
    for key in nodeDict:
        nodes.append(Node(key))
    return Graph(nodes, edges)

def getCurrentBestPath(cycleChecker):
    mList = []
    nodes = [Node("BTC"), Node("ETH")]
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
    for node in maxResult.nodePath:
        print(node)
    print("check price")

    timesToCheck = 10
    while timesToCheck > 0:
        time.sleep(2)
        graph = generateBinanceGraph()
        cycleChecker = CycleChecker(graph)
        cycleChecker.checkNodePath(maxResult.nodePath)
        timesToCheck = timesToCheck - 1


def sketch():
    timestamp = int(round(time.time() * 1000))
    data = {
        "symbol": "LTCBTC",
        "side": "BUY",
        "type": "MARKET",
        "quantity": 1,
        "timestamp": timestamp,
    }
    body = ""
    for key, value in data.items():
        body = body + key + "=" + str(value) + "&"
    body = body[:-1]
    tup = generateApiKeyAndSignature(body, "../keys.json")
    headers = {"X-MBX-APIKEY": tup[0]}
    makeFakeOrderFinal = makeFakeOrder + "?" + body + "&signature=" + tup[1]

    r = requests.post(makeFakeOrderFinal, headers=headers)
    print(" REQUEST JSON: ")
    print(r)
    print(r.json())
    exit(1)
    #r.raise_for_status()

def create_test_order(**params):
    print(params)

def main():
    doIt()

if __name__ == "__main__": main()
