from node import Node

class Graph:

    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges
        ## give me edges for node in constant time. Edges are 1 way
        self.edgeMapping = {}
        for edge in edges:
            fromNodeId = edge.fromNodeId
            if fromNodeId not in self.edgeMapping:
                self.edgeMapping[fromNodeId] = []
            self.edgeMapping[fromNodeId].append(edge)
        self.maxV = 0

    def getEdgesForNode(self, node):
        return self.edgeMapping[node.nodeId]

    def checkCyclesOfDepth(self, depth, startNode):
        self.maxV = 0
        self.checkCyclesOfDepthInternal(depth, set(), 1, startNode, startNode)
        return self.maxV

    def checkCyclesOfDepthInternal(self,
                                   depth,
                                   setOfNodesAlreadyInPath,
                                   units,
                                   nodeToEval,
                                   startNode):
        edges = filter(lambda e: e.toNodeId not in setOfNodesAlreadyInPath, self.getEdgesForNode(nodeToEval))
        if depth == 1:
            ## Need to get back to original node
            for edge in edges:
                if (edge.toNodeId == startNode.nodeId):
                    ## Go home
                    newUnits = edge.makeTrade(units)
                    self.maxV = max(self.maxV, newUnits)
        else:
            for edge in edges:
                toNode = Node(edge.toNodeId)
                newUnits = edge.makeTrade(units)
                setOfNodesAlreadyInPath.add(edge.toNodeId)
                self.checkCyclesOfDepthInternal(depth - 1, setOfNodesAlreadyInPath, newUnits, toNode, startNode)
