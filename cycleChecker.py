from node import Node
import math

class CycleChecker:

    def __init__(self, graph):
        self.graph = graph

    def checkCycles(self, depth, startNode):
        singleCycleMetaData = SingleCycleMetaData(depth, startNode)
        cyclesFound = []
        self.checkCyclesOfDepthInternal(NodeProgress(startNode, depth, []), singleCycleMetaData, cyclesFound)
        return cyclesFound

    def checkCyclesOfDepthInternal(self, nodeProgress, singleCycleMetaData, cyclesFound):
        allEdges = self.graph.getEdgesForNode(nodeProgress.nodeToEval)

        if nodeProgress.depthRemaining == 1:
            ## Need to get back to original node
            for edge in allEdges:
                if (edge.toNodeId == singleCycleMetaData.startNode.nodeId):
                    ## Go home
                    nodeProgress = self.createNextNodeProgress(nodeProgress, edge, singleCycleMetaData)
                    cyclesFound.append(CycleResult(nodeProgress.pastEdges))
        else:
            edges = [e for e in allEdges if e.toNodeId not in singleCycleMetaData.setOfNodesAlreadyInPath]
            for edge in edges:
                nextNodeProgress = self.createNextNodeProgress(nodeProgress, edge, singleCycleMetaData)
                self.checkCyclesOfDepthInternal(nextNodeProgress, singleCycleMetaData, cyclesFound)

    def createNextNodeProgress(self, nodeProgress, edge, singleCycleMetaData):
        toNode = Node(edge.toNodeId)
        singleCycleMetaData.setOfNodesAlreadyInPath.add(edge.toNodeId)
        currentPath = self.extendEdges(edge, nodeProgress)
        return NodeProgress(toNode, nodeProgress.depthRemaining - 1, currentPath)

    def extendEdges(self, edge, nodeProgress):
        currentPath = []
        currentPath.extend(nodeProgress.pastEdges)
        currentPath.append(edge)
        return currentPath

class SingleCycleMetaData:

    def __init__(self, depth, startNode):
        self.depth = depth
        self.startNode = startNode
        self.setOfNodesAlreadyInPath = set()
        self.setOfNodesAlreadyInPath.add(startNode.nodeId)

class NodeProgress:

    def __init__(self, nodeToEval, depthRemaining, pastEdges):
        self.nodeToEval = nodeToEval
        self.depthRemaining = depthRemaining
        self.pastEdges = pastEdges

class CycleResult:

    def __init__(self, edgePath):
        self.edgePath = edgePath

    def emitExpectedTradeValueWithoutDust(self, unit):
        startUnit = unit
        for edge in self.edgePath:
            startUnit = edge.makeTrade(startUnit)
        return startUnit

    def getTradesAndEmitAndDust(self, unit):
        dust = {}
        startUnit = unit
        result = {
            "dust": dust,
            "valid": True,
            "endUnits": startUnit
        }
        for edge in self.edgePath:
            # Look at starting units, see how much can go into new exchange
            tickerInfo = edge.tickerInfo
            stepSize = tickerInfo.stepSize
            # Have to understand which way the exchange goes
            if tickerInfo.buy:
                ## We are in a base currency, going to buy a new one
                unitsInNewCurrency = edge.convertUnits(startUnit)
                if unitsInNewCurrency < stepSize:
                    ## Oh no fail, not enough money to make transaction, mark valid as false and return
                    result["valid"] = False
                    return result
                else:
                    # We have enough
                    numberOfSteps = math.floor(unitsInNewCurrency / stepSize)
                    desiredTradeUnit = numberOfSteps * stepSize
                    tradeUnit = edge.convertInvertedUnits(desiredTradeUnit)
                    newStartUnit = edge.makeTrade(tradeUnit)
                    ## DO DUST PLS
                    dustFromTrade =  startUnit - tradeUnit
                    if dustFromTrade > 0:
                        ## Will happen on non-even trades
                        dust[edge.fromNodeId] = dustFromTrade
                    startUnit = newStartUnit

            else:
                if startUnit < stepSize:
                    ## Oh no fail, not enough money to make transaction, mark valid as false and return
                    result["valid"] = False
                    return result
                else:
                    ## Ok we have enough, lets see how much we are going to transfer now
                    # Take the start and divide by step size
                    numberOfSteps = math.floor(startUnit / stepSize)
                    # Then take the number of steps and multiple it by step size to get amount to trade
                    tradeUnit = numberOfSteps * stepSize
                    ## Then make that trade and have a new startUnit
                    newStartUnit = edge.makeTrade(tradeUnit)
                    ## Before we start over, look at the dust between the 2 values
                    dustFromTrade =  startUnit - tradeUnit
                    if dustFromTrade > 0:
                        ## Will happen on non-even trades
                        dust[edge.fromNodeId] = dustFromTrade
                    startUnit = newStartUnit
        result["endUnits"] = startUnit
        return result
