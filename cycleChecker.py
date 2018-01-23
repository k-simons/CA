from node import Node
import math

class CycleChecker:

    def __init__(self, graph, stepSizeLookUp):
        self.graph = graph
        self.stepSizeLookUp = stepSizeLookUp

    def checkCycles(self, depth, startNode):
        singleCycleMetaData = SingleCycleMetaData(depth, startNode)
        cyclesFound = []
        self.checkCyclesOfDepthInternal(NodeProgress(startNode, depth, 1, []), singleCycleMetaData, cyclesFound)
        return cyclesFound

    def checkEdgePath(self, edges):
        startUnit = 1
        for edge in edges:
            startUnit = edge.makeTrade(startUnit)
        print(startUnit)

    def checkCyclesOfDepthInternal(self, nodeProgress, singleCycleMetaData, cyclesFound):
        allEdges = self.graph.getEdgesForNode(nodeProgress.nodeToEval)

        if nodeProgress.depthRemaining == 1:
            ## Need to get back to original node
            for edge in allEdges:
                if (edge.toNodeId == singleCycleMetaData.startNode.nodeId):
                    ## Go home
                    nodeProgress = self.createNextNodeProgress(nodeProgress, edge, singleCycleMetaData)
                    cyclesFound.append(CycleResult(nodeProgress.pastEdges, nodeProgress.units, self.stepSizeLookUp))
        else:
            edges = [e for e in allEdges if e.toNodeId not in singleCycleMetaData.setOfNodesAlreadyInPath]
            for edge in edges:
                nextNodeProgress = self.createNextNodeProgress(nodeProgress, edge, singleCycleMetaData)
                self.checkCyclesOfDepthInternal(nextNodeProgress, singleCycleMetaData, cyclesFound)

    def createNextNodeProgress(self, nodeProgress, edge, singleCycleMetaData):
        toNode = Node(edge.toNodeId)
        newUnits = edge.makeTrade(nodeProgress.units)
        singleCycleMetaData.setOfNodesAlreadyInPath.add(edge.toNodeId)
        currentPath = self.extendEdges(edge, nodeProgress)
        return NodeProgress(toNode, nodeProgress.depthRemaining - 1, newUnits, currentPath)

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

    def __init__(self, nodeToEval, depthRemaining, units, pastEdges):
        self.nodeToEval = nodeToEval
        self.depthRemaining = depthRemaining
        self.units = units
        self.pastEdges = pastEdges

class CycleResult:

    def __init__(self, edgePath, units, stepSizeLookUp):
        self.edgePath = edgePath
        self.units = units
        self.stepSizeLookUp = stepSizeLookUp

    def getTradesAndEmitAndDust(self, unit):
        dust = {}
        startUnit = unit
        result = {
            "dust": dust,
            "valid": True,
            "endUnits": startUnit
        }
        for edge in self.edgePath:
            symbol = edge.tickerInfo.symbol
            nextUnit = edge.makeTrade(startUnit)
            stepSize = self.stepSizeLookUp[edge.tickerInfo.symbol]
            if nextUnit < stepSize:
                ## Oh no fail
                result["valid"] = False
                return result
            else:
                numberOfSteps = math.floor(nextUnit / stepSize)
                startUnit = numberOfSteps * stepSize
                dust[symbol] = nextUnit - startUnit
        result["endUnits"] = startUnit
        return result
