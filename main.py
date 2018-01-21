
import requests
from graph import Graph
from node import Node
from edge import Edge
from encodeRequest import encode
from cycleChecker import CycleChecker

base = "https://api.binance.com"
info = base + "/api/v1/exchangeInfo"
depth = base + "/api/v1/depth"
extraDepthExample = depth + "?symbol=BNBBTC"
ticket =    base + "/api/v1/ticker/24hr"
tickerPrice = base + "/api/v3/ticker/price"
makeFakeOrder = base + "/api/v3/order/test"

def printKeys(mydic):
    for key in mydic:
        print(key)

def getApiData():

    print(info)
    response = requests.get(info)
    infoResponse = response.json()
    symbols = infoResponse["symbols"]
    print(len(symbols))
    ## use symbols to get to and from

    print("")
    print("")

    print(tickerPrice)
    response = requests.get(tickerPrice)
    print(len(response.json()))
    ## array of
    #{
    #    "symbol": "ETHBTC",
    #    "price": "0.08966300"
    #},
    ## use ticker price to get edge weight

def testGraph():
    ## have a node
    ## pick and edge, follow to n2
    ## pick and edge to n3
    ## pick an edge to n
    ## given a unit -> what it unit in the end
    ## nodeID -> Edges to nodes
    node1 = Node("1")
    node2 = Node("2")
    node3 = Node("3")
    node4 = Node("4")
    node5 = Node("5")
    # To base
    edge12 = Edge("1", "2", .5)

    # L1
    edge23 = Edge("2", "3", 1)
    edge31 = Edge("3", "1", 3)

    # L1
    edge25 = Edge("2", "5", 1)
    edge51 = Edge("5", "1", 1)

    # To no where
    edge24 = Edge("2", "4", 1)
    edge45 = Edge("4", "5", 1)

    graph = Graph(
        [node1, node2, node3, node4, node5],
        [edge12, edge23, edge31, edge25, edge51, edge24, edge45]
    )
    graph.checkCyclesOfDepth(3, Node("1"))

def binanceToNode():
    #- hit the api to get the name of the ticker, the to and the from coins
    #- Enrich with current price to make 2 edges
    return 1

def doIt():
    response = requests.get(tickerPrice)
    prices = response.json()
    # {'symbol': 'ETHBTC', 'price': '0.09017900'} we can see base is ETH and quoteAsset BTC
    pricesDict = {}
    for price in prices:
        pricesDict[price["symbol"]] = price["price"]
    ## great have a dict, now lets creates 2 nodes per symbo
    response = requests.get(info)
    infoResponse = response.json()
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

    graph = Graph(nodes, edges)
    mList = []
    tradeSet = set()
    tradeSet.add("BTC")
    tradeSet.add("ETH")
    for node in nodes:
        if node.nodeId in tradeSet:
            cycleChecker = CycleChecker(3, node, graph)
            test = cycleChecker.checkCycles()
            mList.extend(test)
    maxResult = mList[0]
    for m in mList:
        if m.units > maxResult.units:
            maxResult = m
    print(maxResult.units)
    for node in maxResult.nodePath:
        print(node)


    #print("OLD")
    #mList = []
    #for node in nodes:
    #    mList.append(graph.checkCyclesOfDepth(3, node))
    #print(max(mList))

def main():
    print("fake")
    headers = {"X-MBX-APIKEY: key"}
    data = {'key':'value'}
    r = requests.post(makeFakeOrder, data=data, headers=headers)

    print(r)

def main():
    print("sketch")
    encode(
        "symbol=LTCBTC&side=BUY&type=LIMIT&timeInForce=GTC&quantity=1&price=0.1&recvWindow=5000&timestamp=1499827319559",
        "NhqPtmdSJYdKjVHjA7PZj4Mge3R5YNiP1e3UZjInClVN65XAbvqqM6A7H5fATj0j"
    )

# for making a request
# [linux]$ curl -H "X-MBX-APIKEY: vmPUZE6mv9SD5VNHk4HlWFsOr6aKE2zvsw0MuIgwCIPy6utIco14y7Ju91duEh8A" -X POST 'https://api.binance.com/api/v3/order' -d 'symbol=LTCBTC&side=BUY&type=LIMIT&timeInForce=GTC&quantity=1&price=0.1&recvWindow=6000000&timestamp=1499827319559&signature=c8db56825ae71d6d79447849e617115f4a920fa2acdcab2b053c4b2838bd6b71'


if __name__ == "__main__": main()
