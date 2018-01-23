from node import Node
from graph import Graph
from edge import Edge, TickerInfo

def generateBinanceGraph(binanceClient):

    ## Do this first so the market is most up to date
    infoResponse = binanceClient.getExchangeInfo()
    # Then get market data
    prices = binanceClient.getAllTickerPrices()
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
            float(prices[ticker])
        )
        edgeInverse = Edge(
            TickerInfo(ticker, True),
            goingAsset,
            startAsset,
            1 / float(prices[ticker]),
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