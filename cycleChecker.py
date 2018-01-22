from node import Node

class CycleChecker:

    def __init__(self, graph):
        self.graph = graph

    def checkCycles(self, depth, startNode):
        singleCycleMetaData = SingleCycleMetaData(depth, startNode)
        cyclesFound = []
        self.checkCyclesOfDepthInternal(NodeProgress(startNode, depth, 1, []), singleCycleMetaData, cyclesFound)
        return cyclesFound

    def checkNodePath(self, nodePath):
        startUnit = 1
        for i in range(len(nodePath) - 1):
            node = nodePath[i]
            edge = self.graph.getEdgeFromNodeToNode(node, nodePath[i + 1])
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
                    fullPath = []
                    fullPath.extend(nodeProgress.pastNodes)
                    fullPath.append(singleCycleMetaData.startNode)
                    cyclesFound.append(CycleResult(fullPath, nodeProgress.units))
        else:
            edges = [e for e in allEdges if e.toNodeId not in singleCycleMetaData.setOfNodesAlreadyInPath]
            for edge in edges:
                nextNodeProgress = self.createNextNodeProgress(nodeProgress, edge, singleCycleMetaData)
                self.checkCyclesOfDepthInternal(nextNodeProgress, singleCycleMetaData, cyclesFound)

    def createNextNodeProgress(self, nodeProgress, edge, singleCycleMetaData):
        toNode = Node(edge.toNodeId)
        newUnits = edge.makeTrade(nodeProgress.units)
        singleCycleMetaData.setOfNodesAlreadyInPath.add(edge.toNodeId)
        currentPath = []
        currentPath.extend(nodeProgress.pastNodes)
        currentPath.append(nodeProgress.nodeToEval)
        return NodeProgress(toNode, nodeProgress.depthRemaining - 1, newUnits, currentPath)

class SingleCycleMetaData:

    def __init__(self, depth, startNode):
        self.depth = depth
        self.startNode = startNode
        self.setOfNodesAlreadyInPath = set()
        self.setOfNodesAlreadyInPath.add(startNode.nodeId)

class NodeProgress:

    def __init__(self, nodeToEval, depthRemaining, units, pastNodes):
        self.nodeToEval = nodeToEval
        self.depthRemaining = depthRemaining
        self.units = units
        self.pastNodes = pastNodes

class CycleResult:

    def __init__(self, nodePath, units):
        self.nodePath = nodePath
        self.units = units