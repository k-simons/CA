from binanceClient import BinanceClient
from node import Node
from binanceGraphCreator import generateBinanceGraph
from cycleChecker import CycleChecker


binanceClient = BinanceClient()

def calculateNewBalanceToSee(symbol, orderId):
    order = binanceClient.getLastTradeWithOrderId(symbol, orderId)
    ## Now that we have the order, we take the qty and multiple by price
    newQuantity = float(order["qty"]) * float(order["price"])
    ## Then subtract commision
    amountToTradeLarge = newQuantity - float(order["commission"])
    ## Round to useful value
    amountToTrade = amountToTradeLarge
    return amountToTrade


def getCurrentBestPath(cycleChecker):
    cycleResults = []
    nodes = [Node("ETH")]
    for node in nodes:
        test = cycleChecker.checkCycles(3, node)
        cycleResults.extend(cycleChecker.checkCycles(3, node))
    units = .05
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
    (graph, stepSizeLookUp) = generateBinanceGraph(binanceClient)
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
    exit(1)
    for edge in edges:
        requestJson = makeTradeFromEdge(edge, startQuantity).json()
        print(requestJson)
        symbol = requestJson["symbol"]
        orderId = requestJson["orderId"]
        startQuantity = calculateNewBalanceToSee(symbol, orderId)
        print(startQuantity)


def main():
    doIt()



if __name__ == "__main__": main()
