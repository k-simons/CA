
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
