class Edge:

    def __init__(self, fromNodeId, toNodeId, rate):
        self.fromNodeId = fromNodeId
        self.toNodeId = toNodeId
        self.id = fromNodeId + toNodeId
        self.rate = rate

    def __str__(self):
        return "From " + self.fromNodeId + ", to " + self.toNodeId + " with rate " + str(self.rate)
