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
    for symbol in infoResponse["symbols"]:
        ticker = symbol["symbol"]
        startAsset = symbol["baseAsset"]
        goingAsset = symbol["quoteAsset"]
        nodeDict[startAsset] = True
        nodeDict[goingAsset] = True
        minQty = None
        for filterSet in symbol["filters"]:
            if "minQty" in filterSet:
                minQty = float(filterSet["minQty"])
        if minQty == None:
            raise Exception('MinQty not found')
        edge = Edge(
            TickerInfo(ticker, False, minQty),
            startAsset,
            goingAsset,
            float(prices[ticker])
        )
        edgeInverse = Edge(
            TickerInfo(ticker, True, minQty),
            goingAsset,
            startAsset,
            1 / float(prices[ticker]),
        )
        edges.append(edge)
        edges.append(edgeInverse)

    nodes = []
    for key in nodeDict:
        nodes.append(Node(key))
    return Graph(nodes, edges)
