
import requests
from graph import Graph
from node import Node
from edge import Edge

base = "https://api.binance.com"
info = base + "/api/v1/exchangeInfo"
depth = base + "/api/v1/depth"
extraDepthExample = depth + "?symbol=BNBBTC"
ticket =    base + "/api/v1/ticker/24hr"
tickerPrice = base + "/api/v3/ticker/price"

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

def main():
    print(tickerPrice)
    response = requests.get(tickerPrice)
    prices = response.json()
    # {'symbol': 'ETHBTC', 'price': '0.09017900'} we can see base is ETH and quoteAsset BTC
    pricesDict = {}
    for price in prices:
        pricesDict[price["symbol"]] = price["price"]
    print(pricesDict)
    ## great have a dict, now lets creates 2 nodes per symbo
    print(info)
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
    print("")
    print(len(nodes))
    print(len(edges))
    print("")
    print("START")
    for node in nodes:
        graph.checkCyclesOfDepth(3, node)


if __name__ == "__main__": main()