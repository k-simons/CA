from node import Node

class CycleChecker:

    def __init__(self, depth, startNode, graph):
        self.depth = depth
        self.startNode = startNode
        self.graph = graph
        self.setOfNodesAlreadyInPath = set()
        self.setOfNodesAlreadyInPath.add(startNode.nodeId)

    def checkCycles(self):
        cyclesFound = []
        self.checkCyclesOfDepthInternal(NodeProgress(self.startNode, self.depth, 1, []), cyclesFound)
        return cyclesFound

    def checkCyclesOfDepthInternal(self, nodeProgress, cyclesFound):
        allEdges = self.graph.getEdgesForNode(nodeProgress.nodeToEval)

        if nodeProgress.depthRemaining == 1:
            ## Need to get back to original node
            for edge in allEdges:
                if (edge.toNodeId == self.startNode.nodeId):
                    ## Go home
                    nodeProgress = self.createNextNodeProgress(nodeProgress, edge)
                    cyclesFound.append(CycleResult(nodeProgress.pastNodes, nodeProgress.units))
        else:
            edges = [e for e in allEdges if e.toNodeId not in self.setOfNodesAlreadyInPath]
            for edge in edges:
                nextNodeProgress = self.createNextNodeProgress(nodeProgress, edge)
                self.checkCyclesOfDepthInternal(nextNodeProgress, cyclesFound)

    def createNextNodeProgress(self, nodeProgress, edge):
        toNode = Node(edge.toNodeId)
        newUnits = edge.makeTrade(nodeProgress.units)
        self.setOfNodesAlreadyInPath.add(edge.toNodeId)
        currentPath = []
        currentPath.extend(nodeProgress.pastNodes)
        currentPath.append(nodeProgress.nodeToEval)
        return NodeProgress(toNode, nodeProgress.depthRemaining - 1, newUnits, currentPath)

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