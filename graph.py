from edge import Edge
from node import Node

class Graph:

    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges
        ## give me edges for node in constant time. Edges are 1 way and are indexed by nodeFrom
        self.edgeMapping = {}
        for edge in edges:
            fromNodeId = edge.fromNodeId
            if fromNodeId not in self.edgeMapping:
                self.edgeMapping[fromNodeId] = []
            self.edgeMapping[fromNodeId].append(edge)
        self.maxV = 0

    def getEdgesForNode(self, node):
        return self.edgeMapping[node.nodeId]

    def getEdgeFromNodeToNode(self, nodeFrom, nodeTo):
        for edge in self.edgeMapping[nodeFrom.nodeId]:
            if edge.toNodeId == nodeTo.nodeId:
                return edge
        raise Exception('Could not find edges')

def createTestGraph():
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
